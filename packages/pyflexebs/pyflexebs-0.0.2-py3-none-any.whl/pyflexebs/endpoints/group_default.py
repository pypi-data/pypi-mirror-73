"""
The default group of operations that pyflexebs has
"""
import logging
import time

from pytconf.config import register_endpoint, register_function_group

import pyflexebs
import pyflexebs.version
from pyflexebs.configs import ConfigInterval

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
)
def daemon() -> None:
    """
    Run daemon and monitor disk utilization
    """
    logger = logging.getLogger(__name__)
    while True:
        time.sleep(ConfigInterval.interval)
        logger.info("checking disk utilization")
