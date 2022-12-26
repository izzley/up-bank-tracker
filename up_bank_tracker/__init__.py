import sys
from configparser import RawConfigParser
from pathlib import Path

from loguru import logger

# Project paths
ROOT_PATH = Path(__file__).parents[1].absolute()
CONF_PATH = ROOT_PATH / "conf.ini"
SRC_PATH = ROOT_PATH / "up_bank_tracker"
UNITTEST_PATH = ROOT_PATH / "unit_tests"
FIXTURE_PATH = UNITTEST_PATH / "fixtures"

# Logging
# Log levels: DEBUG < INFO < WARNING < ERROR < CRITICAL < ERROR
# Set Log Level to return logs >= LOG_LEVEL
# LOG_LEVEL = "INFO" will not return any "DEBUG" logs
LOG_LEVEL = "DEBUG"
DEBUG_LOGPATH = ROOT_PATH / "logs/debug.log"


if not CONF_PATH.exists():
    raise FileNotFoundError(
        "conf.ini file not found. Does the file exist?\n"
        "If not, make one: async-example/conf.ini.\n"
        """
            [MOATA]
            username=<username>
            password=<password>
            userid=<userid>
        """
    )

# loguru logger configuration
config = {
    "handlers": [
        {
            "sink": sys.stdout,
            # engueue exposes async logs. False hides them.
            "enqueue": True,
            "level": LOG_LEVEL,
            "format": "<yellow>{time:YYYY-MM-DD at HH:mm:ss}</> | <level>{level}</level>    | <green>{module}</>:<green>{function}</>:<green>{line}</> - <blue>{message}</> | {elapsed.seconds}",
        },
        # {"sink": serial_logloc, "serialize": False},
        {
            "sink": DEBUG_LOGPATH,
            # enque True required for async
            "enqueue": True,
            "level": LOG_LEVEL,
            "format": "<yellow>{time:YYYY-MM-DD at HH:mm:ss}</> | <level>{level}</level>    | <green>{module}</>:<green>{function}</>:<green>{line}</> - <blue>{message}</> | {elapsed.seconds}",
        },
    ],
    "extra": {"user": "izzley"},
}

# global logger instance
logger.configure(**config)


def read_config(path: Path) -> RawConfigParser:
    """
    read secretes from ini file and return section dict.
    """
    config_path = path.absolute()
    # create parser which is able to read percent
    parser = RawConfigParser()
    # preserve case sensitive
    parser.optionxform = str
    # read file into instance
    parser.read(config_path)
    return parser


def read_section_items(section: str) -> dict:
    """
    return all items in config section
    """
    settings = read_config(path=CONF_PATH)
    logger.info(f"Reading section: {section}")
    return {param[0]: param[1] for param in settings.items(section)}
