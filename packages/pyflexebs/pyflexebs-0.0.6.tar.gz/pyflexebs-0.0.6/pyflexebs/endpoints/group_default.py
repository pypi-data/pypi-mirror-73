"""
The default group of operations that pyflexebs has
"""
import logging
import time

import psutil as psutil
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
    logger = logging.getLogger(__name__)
    while True:
        logger.info("checking disk utilization")
        for p in psutil.disk_partitions():
            logger.info("checking {} {}".format(
                p.device,
                p.mountpoint,
            ))
            if psutil.disk_usage(p.mountpoint).percent >= ConfigAlgo.watermark_max:
                logger.info("max watermark detected at disk {} mountpoint {}".format(
                    p.device,
                    p.mountpoint,
                ))
            if psutil.disk_usage(p.mountpoint).percent <= ConfigAlgo.watermark_min:
                logger.info("min watermark detected at disk {} mountpoint {}".format(
                    p.device,
                    p.mountpoint,
                ))
        time.sleep(ConfigAlgo.interval)
