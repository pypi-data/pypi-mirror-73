"""
All configurations for pyflexebs
"""


from pytconf.config import Config, ParamCreator


class ConfigInterval(Config):
    """
    Parameters for interval monitors
    """
    interval = ParamCreator.create_int(
        default=20,
        help_string="interval to monitor",
    )

