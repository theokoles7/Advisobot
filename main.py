"""Drive advisobot application."""

from utils  import BANNER, Config, LOGGER

try:
    # Initiate logging with banner
    LOGGER.info(BANNER)

    # Read in configuration files
    CONFIG = Config()

except Exception as e:
    # Report any wildcard errors
    LOGGER.error(f"An error occurred: {e}")

finally:
    # Report exit
    LOGGER.info("Exiting...")