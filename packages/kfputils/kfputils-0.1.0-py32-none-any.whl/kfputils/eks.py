"""AWS EKS KFP helpers."""
from typing import Dict
from kfp import Client
import boto3
import yaml
from pathlib import Path
from awscli.customizations.eks.get_token import TokenGenerator, STSClientFactory
import botocore.session


def KFPClientFactory(cluster_name: str, cluster_region: str, namespace: str):
    """Generate KFP client authed for AWS EKS.

    Args:
        cluster_name (str): cluster name
        cluster_region (str): cluster region
        namespace (str): k8 namespace

    Returns:
        kfp.Client: authenticated instance of kfp client
    """
    eks = boto3.client("eks", region_name=cluster_region)
    kube_config = _get_kube_config(eks, cluster_name)
    kube_token = _get_token(cluster_name, cluster_region)
    kube_config["users"][0]["user"]["token"] = kube_token
    _save_kube_config(kube_config)
    return Client(namespace=namespace)


def _save_kube_config(config: Dict) -> str:
    filepath = f"{str(Path.home())}/.kube/config"
    with open(filepath, "w") as f:
        yaml.dump(config, f, default_flow_style=False)
    return filepath


def _get_kube_config(eks, cluster_name) -> Dict:
    cluster = eks.describe_cluster(name=cluster_name)
    cluster_cert = cluster["cluster"]["certificateAuthority"]["data"]
    cluster_ep = cluster["cluster"]["endpoint"]
    cluster_config = {
        "apiVersion": "v1",
        "kind": "Config",
        "clusters": [
            {
                "cluster": {
                    "server": str(cluster_ep),
                    "certificate-authority-data": str(cluster_cert),
                },
                "name": "kubernetes",
            }
        ],
        "contexts": [
            {"context": {"cluster": "kubernetes", "user": "aws"}, "name": "aws"}
        ],
        "current-context": "aws",
        "preferences": {},
        "users": [{"name": "aws", "user": {}}],
    }
    return cluster_config


def _get_token(
    cluster_name, cluster_region,
):
    client_factory = STSClientFactory(botocore.session.get_session())
    sts_client = client_factory.get_sts_client(region_name=cluster_region,)
    return TokenGenerator(sts_client).get_token(cluster_name)
