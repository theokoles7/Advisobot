"""Drive advisobot application."""

from bot    import register_courses, register_plan
from utils  import ARGS, BANNER, Config, LOGGER

try:
    # Initiate logging with banner
    LOGGER.info(BANNER)

    # Read in configuration files
    CONFIG = Config()

    # Match action
    match ARGS.action:

        case "register":

            # Match axis
            match ARGS.axis:

                case "courses": register_courses(CONFIG.get_courses(), CONFIG.get_term())

                case "plan":    register_plan(ARGS.plan_name, CONFIG.get_term())
    

except Exception as e:
    # Report any wildcard errors
    LOGGER.error(f"An error occurred: {e}")

finally:
    # Report exit
    LOGGER.info("Exiting...")