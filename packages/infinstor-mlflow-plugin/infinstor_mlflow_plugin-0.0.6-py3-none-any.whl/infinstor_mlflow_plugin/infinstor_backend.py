import hashlib
import json
import yaml
import os
import sys
import shutil
from six.moves import urllib
import subprocess
import tempfile
import logging
import posixpath
import docker
import platform
from os.path import expanduser
from os.path import sep as separator
import requests
from requests.exceptions import HTTPError
import boto3
from urllib.parse import urlparse

from mlflow.projects.backend.abstract_backend import AbstractBackend
import mlflow.projects.databricks
from mlflow.projects import _get_or_create_conda_env, _get_conda_command, _run_entry_point,\
        _get_entry_point_command
import mlflow.tracking as tracking
from mlflow.entities import RunStatus
from mlflow.exceptions import ExecutionException, MlflowException
from mlflow.projects.submitted_run import LocalSubmittedRun, SubmittedRun
from mlflow.projects.utils import (
    _get_storage_dir, fetch_and_validate_project, get_or_create_run, load_project,
    _MLFLOW_LOCAL_BACKEND_RUN_ID_CONFIG
)
from mlflow.projects.backend import loader
from mlflow.tracking.context.git_context import _get_git_commit
from mlflow.tracking.fluent import _get_experiment_id
from mlflow.store.artifact.artifact_repository_registry import get_artifact_repository
from mlflow.store.artifact.azure_blob_artifact_repo import AzureBlobArtifactRepository
from mlflow.store.artifact.gcs_artifact_repo import GCSArtifactRepository
from mlflow.store.artifact.hdfs_artifact_repo import HdfsArtifactRepository
from mlflow.store.artifact.local_artifact_repo import LocalArtifactRepository
from mlflow.store.artifact.s3_artifact_repo import S3ArtifactRepository
from mlflow.utils import databricks_utils, file_utils, process
from mlflow.utils.file_utils import path_to_local_sqlite_uri, path_to_local_file_uri
from mlflow.utils.mlflow_tags import (
    MLFLOW_PROJECT_ENV, MLFLOW_DOCKER_IMAGE_URI, MLFLOW_DOCKER_IMAGE_ID, MLFLOW_PROJECT_BACKEND,
)
from mlflow.utils.uri import get_db_profile_from_uri, is_databricks_uri

from infinstor_mlflow_plugin.cognito_auth_rest_store import CognitoAuthenticatedRestStore

class InfinStorSubmittedRun(SubmittedRun):
    """
    A run that just does nothing
    """

    def __init__(self, run_id):
        self._run_id = run_id

    def wait(self):
        return True

    def get_status(self):
        return RunStatus.FINISHED

    def cancel(self):
        pass

    @property
    def run_id(self):
        return self._run_id



def upload_objects(bucket_name, path_in_bucket, local_path):
    if (path_in_bucket[0] == '/'):
        path_in_bucket = path_in_bucket[1:]
    print('upload_objects: Entered. bucket=' + bucket_name + ', path_in_bucket=' + path_in_bucket\
            + ', local_path=' + local_path)
    # s3_resource = boto3.resource("s3", region_name="us-east-1")
    s3_resource = boto3.resource("s3")

    try:
        my_bucket = s3_resource.Bucket(bucket_name)

        for path, subdirs, files in os.walk(local_path):
            path = path.replace("\\","/")
            directory_name = path.replace(local_path, "")
            for onefile in files:
                print("111111111111 file=" + onefile + ", directory_name=" + directory_name)
                src_path = os.path.join(path, onefile)
                dst_path = path_in_bucket + directory_name + '/' + onefile
                print(">>>>>>>>>> Uploading " + src_path + " to " + dst_path)
                my_bucket.upload_file(src_path, dst_path)
    except Exception as err:
        print(err)

class PluginInfinStorProjectBackend(AbstractBackend):
    def run(self, project_uri, entry_point, params,
            version, backend_config, experiment_id, tracking_store_uri):

        print("PluginInfinStorProjectBackend: Entered. project_uri=" + str(project_uri)\
                + ", entry_point=" + str(entry_point)\
                + ", params=" + str(params)\
                + ", version=" + str(version)\
                + ", backend_config=" + str(backend_config)\
                + ", experiment_id=" + str(experiment_id)\
                + ", tracking_store_uri=" + str(tracking_store_uri))

        work_dir = fetch_and_validate_project(project_uri, version, entry_point, params)
        active_run = get_or_create_run(None, project_uri, experiment_id, work_dir, version,
                                       entry_point, params)

        print('active_run=' + str(active_run))
        print('active_run.info=' + str(active_run.info))

        artifact_uri = active_run.info.artifact_uri
        run_id = active_run.info.run_id

        tags = active_run.data.tags
        if (tags['mlflow.source.type'] != 'PROJECT'):
            raise ValueError('mlflow.source_type must be PROJECT. Instead it is '\
                    + tags['mlflow.source.type'])

        pdst = urlparse(artifact_uri)
        bucket_name = pdst.netloc
        if (pdst.path[0] == '/'):
            path_in_bucket = pdst.path[1:] + '/' + run_id + '/project_files'
        else:
            path_in_bucket = pdst.path + '/' + run_id + '/project_files'
        upload_objects(bucket_name, path_in_bucket, tags['mlflow.source.name'])

        project = load_project(work_dir)
        tracking.MlflowClient().set_tag(active_run.info.run_id, MLFLOW_PROJECT_BACKEND, "infinstor")

        body = dict()
        body['project_files_bucket'] = bucket_name
        body['project_files_path_in_bucket'] = path_in_bucket
        body['params'] = params
        body['run_id'] = run_id
        home = expanduser("~")
        tokfile = expanduser("~") + separator + '.infinstor' + separator + '/token'
        data = open(tokfile, "r").read()
        body['dot_infinstor_contents'] = data

        print(">>>>>>>>>>>> " + json.dumps(body))

        cog = CognitoAuthenticatedRestStore()
        headers = {
                'Content-Type': 'application/x-amz-json-1.1',
                'Authorization' : 'Bearer ' + cog.get_token_string()
                }
        url = 'https://mlflow.' + cog.get_service() + '.com/api/2.0/mlflow/projects/run-project'

        try:
            response = requests.post(url, data=json.dumps(body), headers=headers)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            raise
        except Exception as err:
            print(f'Other error occurred: {err}')
            raise
        else:
            print('>>>>>>>>>>>>>>>>>>>>> Success!')
            return InfinStorSubmittedRun(active_run.info.run_id)

