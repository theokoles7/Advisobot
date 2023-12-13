"""Advisobot actions."""

from bot.driver import BotDriver
from utils      import LOGGER

def register_courses(courses: dict) -> None:
    """Register provided list of courses.

    Args:
        courses (dict): Dictionary list of courses
    """
    # Initialize driver & logger
    driver = BotDriver()
    logger = LOGGER.getChild('registrar')

    try:
        # Log into ULink
        driver.login()

        # Register courses
        for course in courses:

            # Extract individual course information
            course = courses[course]
            logger.info(f"Registering for {course['subject']} {course['number']} ({course['crn']})")

            # IMPLEMENT REGISTRATION PROCESS

        # Log out of ULink
        driver.logout()

    except Exception as e:
        # Report errors
        logger.error(f"An error occurred: {e}")

    finally:
        # Kill driver
        driver.kill()
