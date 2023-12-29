"""Drive advisobot application."""

from bot    import register_courses, register_crns, register_plan, verify
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

                case "crns":     register_crns(CONFIG.get_crns(), CONFIG.get_term())

                case "plan":    register_plan(ARGS.plan_name, CONFIG.get_term())

        case "verify":

            # Match target
            match ARGS.target:

                case "credentials": verify(target="credentials")

                case "term": verify(target="term", term=CONFIG.get_term())

                case "courses": verify(target="courses", term=CONFIG.get_term(), courses=CONFIG.get_courses())

                case "plan": verify(target="plan", term=CONFIG.get_term(), plan_name=ARGS.plan_name)
    

except Exception as e:
    # Report any wildcard errors
    LOGGER.error(f"An error occurred: {e}")

finally:
    # Report exit
    LOGGER.info("Exiting...")