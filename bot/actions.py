"""Advisobot actions."""

import traceback

from selenium.webdriver.common.keys import Keys

from bot.driver                     import BotDriver
from utils                          import LOGGER

# Initialize bot driver
driver =    BotDriver()

# Initialize registrat logger
logger = LOGGER.getChild('registrar')

def register_courses(courses: dict, term: str) -> None:
    """Register provided list of courses.

    Args:
        courses (dict): Dictionary list of courses
        term (str): Term for which courses will be registered for (Season Year)
    """
    try:
        # Log into ULink
        driver.login()

        # Access registration dashboard
        driver.access_registration_dashboard(term)

        # Register courses
        for course in courses:

            # Extract individual course information
            course = courses[course]
            logger.info(f"Registering for {course['subject']} {course['number']} ({course['crn']})")

            # Enter subject & course number and click "Search"
            driver.clear_subject_input()
            driver.send_keys_by_id("s2id_autogen5", course['subject'])
            driver.send_keys_by_id("s2id_autogen5", Keys.ENTER, wait=1)
            driver.send_keys_by_id("txt_courseNumber", course['number'], clear_first=True)
            driver.click_by_id("search-go")

            # Return to course search
            driver.click_by_id("search-again-button")

        # Log out of ULink
        driver.logout()

    except Exception as e:
        # Report errors
        logger.error(f"An error occurred: {e}")

    finally:
        # Kill driver
        driver.kill()


def register_plan(plan_name: str, term: str) -> None:
    """Register saved plan.

    Args:
        plan_name (str): Plan name, as saved in ULink
        term (str): Term for which courses will be registered for (Season Year)
    """
    try:
        # Log into ULink
        driver.login()

        # Access registration dashboard
        driver.access_registration_dashboard(term)

        # Switch to "Plans" tab
        driver.click_by_id("loadPlans-tab")

        # Ensure specified plan exists and click "Add All"
        if driver.xpath_is_present(f"//span[contains(text(), \'Plan: {plan_name}\')]"):

            logger.info(f"Registering all courses in {plan_name}")

            driver.click_by_xpath(
                f"//span[contains(text(), \'Plan: {plan_name}\')]/../.."
                f"/div[@class=\'right\']/button[text()=\'Add All\']"
            )

        else:
            raise ValueError(f"{plan_name} does not exist in user's plans list")
        
        # Communicate registration errors
        for error in driver.check_for_errors(): logger.error(error)

        # Click "Submit"
        driver.click_by_id("saveButton")

        # Communicate completion of task
        logger.info("Plan registration complete")

        # Provide summary report
        report_summary()

        # Log out of ULink
        driver.logout()

    except Exception as e:
        # Report errors
        logger.error(f"An error occured during plan registration: {e}")
        traceback.print_exc()

    finally:
        # Kill driver
        driver.kill()


def report_summary() -> None:
    """Read and communicate summary report."""
    try:
        logger.info("Summary:")
        logger.info("+" + ("-"*112) + "+")
        logger.info(f"| {'TITLE':40} | {'COURSE/SECTION':15} | {'HOURS':5} | {'CRN':5} | {'TYPE':15} | {'STATUS':15} |")
        logger.info("+" + ("-"*112) + "+")

        for course in driver.get_summary_report():
            logger.info(
                f"| {course['title']:40} |"
                f" {course['details']:15} |"
                f" {course['hours']:5} |"
                f" {course['crn']:5} |"
                f" {course['type']:15} |"
                f" {course['status']:15} |"
            )
            logger.info("+" + ("-"*112) + "+")
    except Exception as e:
        logger.error(f"Error occured while producing summary report: {e}")