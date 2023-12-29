"""Advisobot actions."""

import traceback

from selenium.webdriver.common.keys import Keys

from bot.driver                     import BotDriver
from utils                          import LOGGER

# Initialize bot driver
driver =    BotDriver()

# Initialize registrat logger
logger = LOGGER.getChild('registrar')

# REGISTRATION ====================================================================================

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

        print(courses)

        # Register courses
        for course, info in courses.items():

            # Ensure required information is present
            if any(item == None for item in info.values()):
                raise ValueError(f"Course expected to have name, number, and section, got {course}:{info}")

            # Extract individual course information
            logger.info(f"Registering for {info['subject']} {info['number']}, Section {info['section']}")

            # Enter subject & course number and click "Search"
            driver.clear_subject_input()
            driver.send_keys_by_id("s2id_autogen5", info['subject'])
            driver.send_keys_by_id("s2id_autogen5", Keys.ENTER, wait=1)
            driver.send_keys_by_id("txt_courseNumber", info['number'], clear_first=True)
            driver.click_by_id("search-go")

            # Return to course search
            driver.click_by_id("search-again-button")

        # Log out of ULink
        driver.logout()

    except Exception as e:
        # Report errors
        logger.error(f"An error occurred: {e}")
        traceback.print_exc()

    finally:
        # Kill driver
        driver.kill()


def register_crns(crns: list, term: str) -> None:
    """Register by CRNs.

    Args:
        crns (list): List of CRNs
        term (str): Term for which courses will be registered
    """
    try:
        logger.info(f"CRNs: {crns}")

    except Exception as e:
        # Report errors
        logger.error(f"An error occured during CRN registration: {e}")
        traceback.print_exc()

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
        traceback.print_exc()

# VERIFICATION ====================================================================================
        
def verify(target: str, term: str = None, courses: dict = None, plan_name: str = None) -> None:
    """Verify credentials, term, 

    Args:
        target (list): Verification target
        term (str): Term for which courses will be registered for
        courses (dict): Dictionary list of courses
        plan_name (str): Plan name
        crns (list): List of CRNs
    """
    logger.info(f"Verifying: {target}")
    try:
        # Log into ULink
        if driver.login() and target == 'credentials':
            logger.info("Credentials verified")

        # Access registration dashboard
        driver.access_registration_dashboard(term)

        if target == 'term':
            logger.info("Term verified")

        # Match target:
        match target:

            case 'courses':
                for course, info in courses.items():

                    # Ensure required information is present
                    if any(item == None for item in info.values()):
                        raise ValueError(f"Course expected to have name, number, and section, got {course}:{info}")

                    # Enter subject & course number and click "Search"
                    driver.clear_subject_input()
                    driver.send_keys_by_id("s2id_autogen5", info['subject'])
                    driver.send_keys_by_id("s2id_autogen5", Keys.ENTER, wait=1)
                    driver.send_keys_by_id("txt_courseNumber", info['number'], clear_first=True)
                    driver.click_by_id("search-go")

                    # Locate specified section number
                    if driver.xpath_is_present(f"//table[@id=\'table1\']/tbody/tr/td[contains(text(), {info['section']})]"):
                        logger.info(f"Course verified: {course, info}")

                    # Return to course search
                    driver.click_by_id("search-again-button")

            case 'plan':

                # Switch to "Plans" tab
                driver.click_by_id("loadPlans-tab")

                # Ensure specified plan exists and click "Add All"
                if driver.xpath_is_present(f"//span[contains(text(), \'Plan: {plan_name}\')]"):

                    logger.info(f"Plan verified: {plan_name}")

                else:
                    raise ValueError(f"{plan_name} does not exist in user's plans list")

            case 'crns':
                raise NotImplementedError("Verification of CRNs not yet implemented")

    except Exception as e:
        # Report errors
        logger.error(f"An error occured during verification: {e}")
        traceback.print_exc()

    finally:
        # Kill driver
        driver.kill()