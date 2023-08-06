"""
All configurations for pyflexebs
"""


from pytconf.config import Config, ParamCreator


class ConfigAlgo(Config):
    """
    Parameters for interval monitors
    """
    interval = ParamCreator.create_int(
        default=20,
        help_string="interval to monitor",
    )
    watermark_max = ParamCreator.create_int(
        default=70,
        help_string="max watermark for disk utilization",
    )
    watermark_min = ParamCreator.create_int(
        default=20,
        help_string="min watermark for disk utilization",
    )
    disregard = ParamCreator.create_list_str(
        default="/",
        help_string="what mount points to disregard",
    )
    file_systems = ParamCreator.create_list_str(
        default="ext4",
        help_string="what file systems to check",
    )

