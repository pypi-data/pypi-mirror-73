"""
All configurations for pyflexebs
"""


from pytconf.config import Config, ParamCreator


class ConfigInterval(Config):
    """
    Parameters for interval monitors
    """
    filenames = ParamCreator.create_int(
    )
