"""Advisobot actions."""

from bot.driver import BotDriver
from utils      import LOGGER

def register_courses(courses: dict, term: str) -> None:
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

            # Proceed to term selection
            driver.get("https://reg-prod.ec.louisiana.edu/StudentRegistrationSsb/ssb/registration")
            driver.click_by_id("registerLink")

            # Open drop down and select term
            driver.click_by_id("s2id_txt_term")
            driver.click_by_xpath(f"//div[contains(text(), \'{term}\')]")
            driver.click_by_id("term-go")

            # Enter subject & course number and click "Search"
            driver.send_keys_by_id("s2id_txt_subject", course['subject'])
            driver.send_keys_by_id("txt_courseNumber", course['number'])
            driver.click_by_id("search-go")

        # Log out of ULink
        driver.logout()

    except Exception as e:
        # Report errors
        logger.error(f"An error occurred: {e}")

    finally:
        # Kill driver
        driver.kill()
