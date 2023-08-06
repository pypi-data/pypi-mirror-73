"""
The default group of operations that pyflexebs has
"""
import logging
import os
import time

import boto3
import ec2_metadata
import psutil as psutil
from pyfakeuse.pyfakeuse import fake_use
from pylogconf.core import create_pylogconf_file
from pytconf.config import register_endpoint, register_function_group

import pyflexebs
import pyflexebs.version
from pyflexebs.configs import ConfigAlgo, ConfigProxy

GROUP_NAME_DEFAULT = "default"
GROUP_DESCRIPTION_DEFAULT = "all pyflexebs commands"


def register_group_default():
    """
    register the name and description of this group
    """
    register_function_group(
        function_group_name=GROUP_NAME_DEFAULT,
        function_group_description=GROUP_DESCRIPTION_DEFAULT,
    )


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
)
def version() -> None:
    """
    Print version
    """
    print(pyflexebs.version.VERSION_STR)


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
    configs=[ConfigAlgo, ConfigProxy],
)
def daemon() -> None:
    """
    Run daemon and monitor disk utilization
    """
    configure_proxy()
    metadata = ec2_metadata.ec2_metadata
    instance_id = metadata.instance_id
    ec2 = boto3.resource('ec2', region_name=metadata.region)
    instance = ec2.Instance(instance_id)
    volumes = instance.volumes.all()

    logger = logging.getLogger(__name__)
    while True:
        logger.info("checking disk utilization")
        for p in psutil.disk_partitions():
            if p.mountpoint in ConfigAlgo.disregard:
                continue
            if p.fstype not in ConfigAlgo.file_systems:
                continue
            logger.info("checking {} {} {}".format(
                p.device,
                p.mountpoint,
                p.fstype,
            ))
            if psutil.disk_usage(p.mountpoint).percent >= ConfigAlgo.watermark_max:
                logger.info("max watermark detected at disk {} mountpoint {}".format(
                    p.device,
                    p.mountpoint,
                ))
                enlarge_volume(metadata, p, volumes)
            if psutil.disk_usage(p.mountpoint).percent <= ConfigAlgo.watermark_min:
                logger.info("min watermark detected at disk {} mountpoint {}".format(
                    p.device,
                    p.mountpoint,
                ))
        time.sleep(ConfigAlgo.interval)


def enlarge_volume(metadata, p, volumes):
    fake_use(metadata)
    fake_use(p)
    fake_use(volumes)


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
    configs=[ConfigAlgo, ConfigProxy],
)
def print_volumes() -> None:
    """
    Print volume information
    """
    configure_proxy()
    metadata = ec2_metadata.ec2_metadata
    # check that we have attached an IAM role to the machine
    # we need this for credentials
    if metadata.iam_info is None:
        print("No IAM role attached to instance. Please fix instance configuration.")
        return
    print("Found iam_info, good...")
    instance_id = metadata.instance_id
    session = boto3.session.Session(region_name=metadata.region)
    ec2 = session.resource('ec2')
    instance = ec2.Instance(instance_id)
    print("instance is [{}]".format(instance_id))
    volumes = instance.volumes.all()
    for v in volumes:
        dump(v)


def dump(obj):
    for attr in dir(obj):
        if attr.startswith("__"):
            continue
        print("obj.%s = %r" % (attr, getattr(obj, attr)))


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
)
def create_pylogconf() -> None:
    """
    create a pylogconf configuration file
    """
    create_pylogconf_file()


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
    configs=[ConfigProxy],
)
def show_policies() -> None:
    """
    Show policies that are configured for your role
    """
    configure_proxy()
    metadata = ec2_metadata.ec2_metadata
    # check that we have attached an IAM role to the machine
    # we need this for credentials
    if metadata.iam_info is None:
        print("No IAM role attached to instance. Please fix instance configuration.")
        return
    print("Found iam_info, good...")
    print("found [{}]".format(metadata.iam_info))
    instance_profile_arn = metadata.iam_info["InstanceProfileArn"]
    print("instance_profile_arn [{}]".format(instance_profile_arn))
    name = instance_profile_arn.split("/")[1]
    print("name [{}]".format(name))
    session = boto3.session.Session(region_name=metadata.region)
    iam = session.resource('iam')
    policy_list = iam.list_attached_role_policies(RoleName=name)
    for policy in policy_list:
        print(policy)


def configure_proxy():
    if ConfigProxy.http_proxy is not None:
        os.environ['http_proxy'] = ConfigProxy.http_proxy
        os.environ['HTTP_PROXY'] = ConfigProxy.http_proxy
    if ConfigProxy.https_proxy is not None:
        os.environ['https_proxy'] = ConfigProxy.https_proxy
        os.environ['HTTPS_PROXY'] = ConfigProxy.https_proxy
    if ConfigProxy.no_proxy is not None:
        os.environ['no_proxy'] = ConfigProxy.no_proxy
        os.environ['NO_PROXY'] = ConfigProxy.no_proxy
