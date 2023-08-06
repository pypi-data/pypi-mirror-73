"""
The default group of operations that pyflexebs has
"""
import logging
import os
import subprocess
import sys
import time

import boto3
import ec2_metadata
import psutil as psutil
from pylogconf.core import create_pylogconf_file
from pytconf.config import register_endpoint, register_function_group

import pyflexebs
import pyflexebs.version
from pyflexebs.configs import ConfigAlgo, ConfigProxy

import pypathutil.common

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
    check_tools()
    metadata = ec2_metadata.ec2_metadata
    instance_id = metadata.instance_id
    ec2_resource = boto3.resource('ec2', region_name=metadata.region)
    instance = ec2_resource.Instance(instance_id)
    volumes = instance.volumes.all()
    device_to_volume = dict()
    for volume in volumes:
        for a in volume.attachments:
            device = normalize_device(a["Device"])
            device_to_volume[device] = volume
    ec2_client = boto3.client('ec2', region_name=metadata.region)

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
            if ConfigAlgo.watermark_max is not None:
                if psutil.disk_usage(p.mountpoint).percent >= ConfigAlgo.watermark_max:
                    logger.info("max watermark detected at disk {} mountpoint {}".format(
                        p.device,
                        p.mountpoint,
                    ))
                    logger.info("percent is {}, total is {}, used is {}".format(
                        psutil.disk_usage(p.mountpoint).percent,
                        psutil.disk_usage(p.mountpoint).total,
                        psutil.disk_usage(p.mountpoint).used,
                    ))
                    enlarge_volume(p, device_to_volume, ec2_client)
            if ConfigAlgo.watermark_min is not None:
                if psutil.disk_usage(p.mountpoint).percent <= ConfigAlgo.watermark_min:
                    logger.info("min watermark detected at disk {} mountpoint {}".format(
                        p.device,
                        p.mountpoint,
                    ))
                    logger.info("percent is {}, total is {}, used is {}".format(
                        psutil.disk_usage(p.mountpoint).percent,
                        psutil.disk_usage(p.mountpoint).total,
                        psutil.disk_usage(p.mountpoint).used,
                    ))
        time.sleep(ConfigAlgo.interval)


def normalize_device(dev: str) -> str:
    """
    turns /dev/sdb to /dev/xvdb (if needed)
    """
    last_part = dev.split("/")[2]
    if last_part.startswith("sd"):
        drive = last_part[2:]
        return "/dev/xvd{}".format(drive)
    return dev


def enlarge_volume(p, device_to_volume, ec2):
    if p.device not in device_to_volume:
        print("Cannot find device [{}]. Not resizing".format(p.device))
        return
    volume = device_to_volume[p.device]
    volume_id = volume.id
    # volume_size = volume.size
    volume_size = psutil.disk_usage(p.mountpoint).total
    volume_size_float = float(volume_size)
    volume_size_float /= 100
    volume_size_float *= (100+ConfigAlgo.increase_percent)
    new_size = int(volume_size_float)
    if volume.size < new_size:
        print("trying to increase size to [{}]".format(new_size))
        # noinspection PyBroadException
        try:
            result = ec2.modify_volume(
                DryRun=ConfigAlgo.dryrun,
                VolumeId=volume_id,
                Size=new_size,
            )
            print("Success in increasing size [{}]".format(result))
        except Exception as e:
            print("Failure in increasing size [{}]".format(e))
    # resize the file system
    print("doing [{}] extension", format(p.fstype))
    if p.fstype == "ext4":
        subprocess.check_call([
            "resize2fs",
            p.device,
        ])
    if p.fstype == "xfs":
        print("doing ext4 extension")
        subprocess.check_call([
            "xfs_growfs",
            "-d",
            p.mountpoint,
        ])


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
    iam = session.client('iam')
    policy_list = iam.list_attached_role_policies(RoleName=name)
    # pprint(policy_list)
    for policy in policy_list["AttachedPolicies"]:
        policy_name = policy["PolicyName"]
        policy_arn = policy["PolicyArn"]
        print("policy_name: [{}]".format(policy_name))
        print("policy_arn: [{}]".format(policy_arn))


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


def check_tools():
    """
    Check that the command line tools we need are available
    """
    problems = False
    for app in ["xfs_growfs", "resize2fs"]:
        if pypathutil.common.find_in_standard_path(app) is None:
            problems = True
            print("please install executable [{}]".format(app))
    if problems:
        sys.exit(1)
