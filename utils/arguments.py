"""Command line argument utilities."""

import argparse

# Initialize parser
parser = argparse.ArgumentParser(
    prog =          "advisobot",
    description =   "Automated course registration (for University of Louisiana - Lafyette)."
)

# BEGIN ARGUMENTS =================================================================================

# Config ----------------------------------------
config =            parser.add_argument_group("config")

config.add_argument(
    "--credentials_path",
    type =          str,
    default =       "./conf/credentials.ini",
    help =          "Path to credentials file. Defaults to \'./conf/credentials.ini\'."
)

config.add_argument(
    "--courses_path",
    type =          str,
    default =       "./conf/courses.yaml",
    help =          "Path to courses file. Defaults to \'./conf/ccourses.yaml\'."
)

config.add_argument(
    "--config_key",
    type =          str,
    default =       "./conf/aes.key",
    help =          "Path to configuration decryption key. Defaults to \'./conf/aes.key\'."
)

# LOGGING ---------------------------------------
logging =           parser.add_argument_group("Logging")

logging.add_argument(
    "--logging_path",
    type =          str,
    default =       "./logs",
    help =          "Logging destination path. Defaults to \'./logs/\'."
)

logging.add_argument(
    "--logging_level",
    type =          str,
    choices =       ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    default =       "INFO",
    help =          "Minimum logging level (DEBUG < INFO < WARNING < ERROR < CRITICAL). Defaults to \'INFO\'."
)

# END ARGUMENTS ===================================================================================

# Parse arguments
ARGS =              parser.parse_args()