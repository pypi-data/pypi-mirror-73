"""Pipeline helpers."""
from kfp import Client

# from kfp_server_api.models.api_pipeline_version import ApiPipelineVersion
from typing import Dict
from yaml import safe_load

from yaml import Loader, Dumper  # noqa:F401

# try:
#     from yaml import CLoader as Loader, CDumper as Dumper
# except ImportError:
#     from yaml import Loader, Dumper  # noqa:F401
import pathlib
import os
import json


def upload_pipeline(
    client,
    pipeline_name: str,
    package_file: str,
    pipeline_version: str = ""
    # ):
) -> (Dict, bool):
    """Upload a pipeline package.

    Returns:
        Dict: pipeline info (id etc),
        bool: indicates whether the pipeline was created (as opposed to updated)
    """
    # if first time create new pipeline
    latest_pipeline = get_latest_pipeline_version(client, pipeline_name)
    if not latest_pipeline:
        return (
            client.pipeline_uploads.upload_pipeline(
                os.path.join(package_file), name=pipeline_name
            ),
            True,
        )
    # else update existing pipeline with new version
    else:
        return (
            client.pipeline_uploads.upload_pipeline_version(
                package_file, name=pipeline_version, pipelineid=latest_pipeline.id
            ),
            False,
        )


def get_latest_pipeline_version(
    client: Client,
    pipeline_name: str,
    page_size: int = 100
    # ) -> ApiPipelineVersion:
):
    """Return object containing info on most recent version of pipeline."""
    # https://www.kubeflow.org/docs/pipelines/reference/api/kubeflow-pipeline-api-spec/#/definitions/apiListPipelinesResponse
    first_run = True
    next_page_token = None
    # i = 0
    # import pprint

    while first_run or next_page_token is not None:
        if first_run:
            next_page_token = ""
        # i += 1
        # pprint.pprint(f"i = {i}")
        first_run = False
        response = client.list_pipelines(
            page_size=page_size, sort_by="created_at desc", page_token=next_page_token,
        )
        next_page_token = response.next_page_token
        print("next_page_token")
        print(next_page_token)
        # next_page_token = response["next_page_token"]
        # pprint.pprint(response)
        # print("---------------------")
        # pprint.pprint(f"next_page_token = {next_page_token}")
        if len(response.pipelines) > 0:
            pipeline = _filter_pipeline(response.pipelines, pipeline_name)
            # pprint.pprint(f"_filter_pipeline res: {pipeline}")
            if pipeline is not None:
                return pipeline

    return None
    print(f"could not find pipeline: {pipeline_name}")


def _filter_pipeline(pipelines, name: str):
    # def _filter_pipeline(pipelines, name: str) -> ApiPipelineVersion:
    # https://www.kubeflow.org/docs/pipelines/reference/api/kubeflow-pipeline-api-spec/#/definitions/apiPipelineVersion
    for p in pipelines:
        if p.name == name:
            return p


def _extract_pipeline_name(package_file: str) -> str:
    data = safe_load(pathlib.Path(package_file).read_text())
    annotations = data["metadata"]["annotations"]
    pipeline_spec = json.loads(annotations["pipelines.kubeflow.org/pipeline_spec"])
    pipeline_name = pipeline_spec["name"]
    return pipeline_name
