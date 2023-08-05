import os
import pickle
import time

import boto3
from botocore.exceptions import ClientError
from dagster_aws.emr import EmrJobRunner, emr_step_main
from dagster_aws.utils.mrjob.log4j import parse_hadoop_log4j_records
from dagster_pyspark.utils import build_pyspark_zip
from dagster_spark.configs_spark import spark_config as get_spark_config
from dagster_spark.utils import flatten_dict, format_for_cli

from dagster import Field, StringSource, check, resource, seven
from dagster.core.definitions.step_launcher import StepLauncher
from dagster.core.events import log_step_event
from dagster.core.execution.plan.external_step import (
    PICKLED_EVENTS_FILE_NAME,
    PICKLED_STEP_RUN_REF_FILE_NAME,
    step_context_to_step_run_ref,
)

# On EMR, Spark is installed here
EMR_SPARK_HOME = '/usr/lib/spark/'

CODE_ZIP_NAME = 'code.zip'


@resource(
    {
        'spark_config': get_spark_config(),
        'cluster_id': Field(
            StringSource, description='Name of the job flow (cluster) on which to execute'
        ),
        'region_name': Field(StringSource),
        'action_on_failure': Field(str, is_required=False, default_value='CANCEL_AND_WAIT'),
        'staging_bucket': Field(
            StringSource,
            is_required=True,
            description='S3 bucket to use for passing files between the plan process and EMR '
            'process.',
        ),
        'staging_prefix': Field(
            StringSource,
            is_required=False,
            default_value='emr_staging',
            description='S3 key prefix inside the staging_bucket to use for files passed the plan '
            'process and EMR process',
        ),
        'wait_for_logs': Field(
            bool,
            is_required=False,
            default_value=False,
            description='If set, the system will wait for EMR logs to appear on S3. Note that logs '
            'are copied every 5 minutes, so enabling this will add several minutes to the job '
            'runtime.',
        ),
        'local_pipeline_package_path': Field(
            StringSource,
            is_required=True,
            description='Absolute path to the package that contains the pipeline definition(s) '
            'whose steps will execute remotely on EMR. This is a path on the local fileystem of '
            'the process executing the pipeline. The expectation is that this package will also be '
            'available on the python path of the launched process running the Spark step on EMR, '
            'either deployed on step launch via the deploy_pipeline_package option, referenced on '
            's3 via the s3_pipeline_package_path option, or installed on the cluster via bootstrap '
            'actions.',
        ),
        'deploy_local_pipeline_package': Field(
            bool,
            default_value=False,
            is_required=False,
            description='If set, before every step run, the launcher will zip up all the code in '
            'local_pipeline_package_path, upload it to s3, and pass it to spark-submit\'s '
            '--py-files option. This gives the remote process access to up-to-date user code. '
            'If not set, the assumption is that some other mechanism is used for distributing code '
            'to the EMR cluster. If this option is set to True, s3_pipeline_package_path should '
            'not also be set.',
        ),
        's3_pipeline_package_path': Field(
            StringSource,
            is_required=False,
            description='If set, this path will be passed to the --py-files option of spark-submit. '
            'This should usually be a path to a zip file.  If this option is set, '
            'deploy_local_pipeline_package should not be set to True.',
        ),
    }
)
def emr_pyspark_step_launcher(context):
    return EmrPySparkStepLauncher(**context.resource_config)


class EmrPySparkStepLauncher(StepLauncher):
    def __init__(
        self,
        region_name,
        staging_bucket,
        staging_prefix,
        wait_for_logs,
        action_on_failure,
        cluster_id,
        spark_config,
        local_pipeline_package_path,
        deploy_local_pipeline_package,
        s3_pipeline_package_path=None,
    ):
        self.region_name = check.str_param(region_name, 'region_name')
        self.staging_bucket = check.str_param(staging_bucket, 'staging_bucket')
        self.staging_prefix = check.str_param(staging_prefix, 'staging_prefix')
        self.wait_for_logs = check.bool_param(wait_for_logs, 'wait_for_logs')
        self.action_on_failure = check.str_param(action_on_failure, 'action_on_failure')
        self.cluster_id = check.str_param(cluster_id, 'cluster_id')
        self.spark_config = spark_config

        check.invariant(
            not deploy_local_pipeline_package or not s3_pipeline_package_path,
            'If deploy_local_pipeline_package is set to True, s3_pipeline_package_path should not '
            'also be set.',
        )

        self.local_pipeline_package_path = check.str_param(
            local_pipeline_package_path, 'local_pipeline_package_path'
        )
        self.deploy_local_pipeline_package = check.bool_param(
            deploy_local_pipeline_package, 'deploy_local_pipeline_package'
        )
        self.s3_pipeline_package_path = check.opt_str_param(
            s3_pipeline_package_path, 's3_pipeline_package_path'
        )

        self.emr_job_runner = EmrJobRunner(region=self.region_name)

    def _post_artifacts(self, log, step_run_ref, run_id, step_key):
        '''
        Synchronize the step run ref and pyspark code to an S3 staging bucket for use on EMR.

        For the zip file, consider the following toy example:

            # Folder: my_pyspark_project/
            # a.py
            def foo():
                print(1)

            # b.py
            def bar():
                print(2)

            # main.py
            from a import foo
            from b import bar

            foo()
            bar()

        This will zip up `my_pyspark_project/` as `my_pyspark_project.zip`. Then, when running
        `spark-submit --py-files my_pyspark_project.zip emr_step_main.py` on EMR this will
        print 1, 2.
        '''

        with seven.TemporaryDirectory() as temp_dir:
            s3 = boto3.client('s3', region_name=self.region_name)

            # Upload step run ref
            def _upload_file_to_s3(local_path, s3_filename):
                key = self._artifact_s3_key(run_id, step_key, s3_filename)
                s3_uri = self._artifact_s3_uri(run_id, step_key, s3_filename)
                log.debug(
                    'Uploading file {local_path} to {s3_uri}'.format(
                        local_path=local_path, s3_uri=s3_uri
                    )
                )
                s3.upload_file(Filename=local_path, Bucket=self.staging_bucket, Key=key)

            # Upload main file.
            # The remote Dagster installation should also have the file, but locating it there
            # could be a pain.
            main_local_path = self._main_file_local_path()
            _upload_file_to_s3(main_local_path, self._main_file_name())

            if self.deploy_local_pipeline_package:
                # Zip and upload package containing pipeline
                zip_local_path = os.path.join(temp_dir, CODE_ZIP_NAME)
                build_pyspark_zip(zip_local_path, self.local_pipeline_package_path)
                _upload_file_to_s3(zip_local_path, CODE_ZIP_NAME)

            # Create step run ref pickle file
            step_run_ref_local_path = os.path.join(temp_dir, PICKLED_STEP_RUN_REF_FILE_NAME)
            with open(step_run_ref_local_path, 'wb') as step_pickle_file:
                pickle.dump(step_run_ref, step_pickle_file)

            _upload_file_to_s3(step_run_ref_local_path, PICKLED_STEP_RUN_REF_FILE_NAME)

    def launch_step(self, step_context, prior_attempts_count):
        step_run_ref = step_context_to_step_run_ref(
            step_context, prior_attempts_count, self.local_pipeline_package_path
        )

        run_id = step_context.pipeline_run.run_id
        log = step_context.log

        step_key = step_run_ref.step_key
        self._post_artifacts(log, step_run_ref, run_id, step_key)

        emr_step_def = self._get_emr_step_def(run_id, step_key, step_context.solid.name)
        emr_step_id = self.emr_job_runner.add_job_flow_steps(log, self.cluster_id, [emr_step_def])[
            0
        ]

        s3 = boto3.resource('s3', region_name=self.region_name)
        for event in self.wait_for_completion(log, s3, run_id, step_key, emr_step_id):
            log_step_event(step_context, event)
            yield event

        if self.wait_for_logs:
            self._log_logs_from_s3(log, emr_step_id)

    def wait_for_completion(self, log, s3, run_id, step_key, emr_step_id, check_interval=15):
        ''' We want to wait for the EMR steps to complete, and while that's happening, we want to
        yield any events that have been written to S3 for us by the remote process.
        After the the EMR steps complete, we want a final chance to fetch events before finishing
        the step.
        '''
        done = False
        all_events = []
        while not done:
            time.sleep(check_interval)  # AWS rate-limits us if we poll it too often
            done = self.emr_job_runner.is_emr_step_complete(log, self.cluster_id, emr_step_id)

            all_events_new = self.read_events(s3, run_id, step_key)
            if len(all_events_new) > len(all_events):
                for i in range(len(all_events), len(all_events_new)):
                    yield all_events_new[i]
                all_events = all_events_new

    def read_events(self, s3, run_id, step_key):
        events_s3_obj = s3.Object(  # pylint: disable=no-member
            self.staging_bucket, self._artifact_s3_key(run_id, step_key, PICKLED_EVENTS_FILE_NAME)
        )

        try:
            events_data = events_s3_obj.get()['Body'].read()
            return pickle.loads(events_data)
        except ClientError as ex:
            # The file might not be there yet, which is fine
            if ex.response['Error']['Code'] == 'NoSuchKey':
                return []
            else:
                raise ex

    def _log_logs_from_s3(self, log, emr_step_id):
        '''Retrieves the logs from the remote PySpark process that EMR posted to S3 and logs
        them to the given log.'''
        stdout_log, stderr_log = self.emr_job_runner.retrieve_logs_for_step_id(
            log, self.cluster_id, emr_step_id
        )
        # Since stderr is YARN / Hadoop Log4J output, parse and reformat those log lines for
        # Dagster's logging system.
        records = parse_hadoop_log4j_records(stderr_log)
        for record in records:
            log._log(  # pylint: disable=protected-access
                record.level, record.logger + ': ' + record.message, {}
            )
        log.info(stdout_log)

    def _get_emr_step_def(self, run_id, step_key, solid_name):
        '''From the local Dagster instance, construct EMR steps that will kick off execution on a
        remote EMR cluster.
        '''
        action_on_failure = self.action_on_failure

        # Execute Solid via spark-submit
        conf = dict(flatten_dict(self.spark_config))
        conf['spark.app.name'] = conf.get('spark.app.name', solid_name)

        check.invariant(
            conf.get('spark.master', 'yarn') == 'yarn',
            desc='spark.master is configured as %s; cannot set Spark master on EMR to anything '
            'other than "yarn"' % conf.get('spark.master'),
        )

        command = (
            [
                EMR_SPARK_HOME + 'bin/spark-submit',
                '--master',
                'yarn',
                '--deploy-mode',
                conf.get('spark.submit.deployMode', 'client'),
            ]
            + format_for_cli(list(flatten_dict(conf)))
            + [
                '--py-files',
                self._artifact_s3_uri(run_id, step_key, CODE_ZIP_NAME),
                self._artifact_s3_uri(run_id, step_key, self._main_file_name()),
                self.staging_bucket,
                self._artifact_s3_key(run_id, step_key, PICKLED_STEP_RUN_REF_FILE_NAME),
            ]
        )

        return EmrJobRunner.construct_step_dict_for_command(
            'Execute Solid %s' % solid_name, command, action_on_failure=action_on_failure
        )

    def _main_file_name(self):
        return os.path.basename(self._main_file_local_path())

    def _main_file_local_path(self):
        return emr_step_main.__file__

    def _artifact_s3_uri(self, run_id, step_key, filename):
        key = self._artifact_s3_key(run_id, step_key, filename)
        return 's3://{bucket}/{key}'.format(bucket=self.staging_bucket, key=key)

    def _artifact_s3_key(self, run_id, step_key, filename):
        return '/'.join([self.staging_prefix, run_id, step_key, os.path.basename(filename)])
