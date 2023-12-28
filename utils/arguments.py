"""Command line argument utilities."""

import argparse

# Initialize parser
parser = argparse.ArgumentParser(
    prog =          "advisobot",
    description =   "Automated course registration (for University of Louisiana - Lafyette)."
)

actions = parser.add_subparsers(
    dest =          "action",
    description =   "Advisobot actions"
)

###################################################################################################
# BEGIN ARGUMENTS                                                                                 #
###################################################################################################

# UNIVERSAL =======================================================================================

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

# CONFIG ----------------------------------------
config =            parser.add_argument_group("config")

config.add_argument(
    "--browser",
    type =          str,
    choices =       ["chrome", "firefox"],
    default =       "firefox",
    help =          "Choice of browser"
)

config.add_argument(
    "--credentials_path",
    type =          str,
    default =       "./conf/credentials.ini",
    help =          "Path to credentials file. Defaults to \'./conf/credentials.ini\'."
)

config.add_argument(
    "--config_key",
    type =          str,
    default =       "./conf/aes.key",
    help =          "Path to configuration decryption key. Defaults to \'./conf/aes.key\'."
)

config.add_argument(
    "--courses_path",
    type =          str,
    default =       "./conf/courses.yaml",
    help =          "Path to courses file. Defaults to \'./conf/ccourses.yaml\'."
)

config.add_argument(
    "--drivers_path",
    type =          str,
    default =       "./conf/drivers.yaml",
    help =          "Path to drivers file. Defaults to \'./conf/drivers.yaml\'"
)

# ACTIONS =========================================================================================

# REGISTER --------------------------------------
register = actions.add_parser(
    "register",
    description =   "Register by course information or plan"
)

axis = register.add_subparsers(
    dest =          "axis"
)

# COURSES ______________
courses = axis.add_parser(
    "courses",
    description =   "Register from courses list"
)

# PLANS
plans = axis.add_parser(
    "plan",
    description =   "Register from plan"
)

plans.add_argument(
    "plan_name",
    type =          str,
    help =          "Plan name"
)

###################################################################################################
# ENDARGUMENTS                                                                                    #
###################################################################################################

# Parse arguments
ARGS =              parser.parse_args()