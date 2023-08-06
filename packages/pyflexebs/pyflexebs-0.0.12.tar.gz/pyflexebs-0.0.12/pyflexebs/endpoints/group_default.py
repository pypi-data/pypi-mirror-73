"""
The default group of operations that pyflexebs has
"""
import logging
import time
from pprint import pprint

import boto3
import ec2_metadata
import psutil as psutil
from pyfakeuse.pyfakeuse import fake_use
from pytconf.config import register_endpoint, register_function_group

import pyflexebs
import pyflexebs.version
from pyflexebs.configs import ConfigAlgo

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
    configs=[ConfigAlgo],
)
def daemon() -> None:
    """
    Run daemon and monitor disk utilization
    """
    metadata = ec2_metadata.ec2_metadata
    instance_id = metadata.instance_id
    ec2 = boto3.resource('ec2')
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
    configs=[ConfigAlgo],
)
def print_volumes() -> None:
    """
    Print volume information
    """
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
        pprint(vars(v))
