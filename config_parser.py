from configparser import ConfigParser
from os import path

def parse_configuration(config_file: str = f"{path.dirname(path.abspath(__file__))}/config.ini") -> str:
    """Parse credentials to authenticate with Discord bot token.

    Parameters
    ----------
    config_file : str, optional
        The config file location, by default "config.ini"

    Returns
    -------
    str
        Discord bot token
    """
    config = ConfigParser()

    config.read(config_file)

    token = config["Keys"]["token"]

    return token