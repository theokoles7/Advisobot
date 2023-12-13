"""Drive advisobot application."""

from bot    import register_courses
from utils  import BANNER, Config, LOGGER

try:
    # Initiate logging with banner
    LOGGER.info(BANNER)

    # Read in configuration files
    CONFIG = Config()

    # Register courses provided
    register_courses(CONFIG.get_courses())

except Exception as e:
    # Report any wildcard errors
    LOGGER.error(f"An error occurred: {e}")

finally:
    # Report exit
    LOGGER.info("Exiting...")