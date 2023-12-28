"""Advisobot driver and utilities."""

import os, time

from selenium                           import webdriver
from selenium.webdriver.common.by       import By
from selenium.webdriver.common.keys     import Keys
from selenium.webdriver.support.wait    import WebDriverWait
from selenium.webdriver.support         import expected_conditions  as EC
from selenium.webdriver.chrome.service  import Service              as firefox_service
from selenium.webdriver.firefox.service import Service              as chrome_service

from utils      import ARGS, LOGGER, Config

class BotDriver(webdriver.Firefox if ARGS.browser == 'firefox' else webdriver.Chrome):
    """Advisobot driver."""

    config = Config()
    logger = LOGGER.getChild('driver')

    def __init__(self):
        """Initialize bot webdriver object."""
        super().__init__(
            service =   (
                chrome_service(self.config.get_driver(ARGS.browser)) 
                if ARGS.browser == 'chrome' 
                else firefox_service(self.config.get_driver(ARGS.browser))
            )
        )

    def access_registration_dashboard(self, term: str) -> None:
        """Navigate to registration dashboard and select apropriate term.

        Args:
            term (str): Term for which courses will be registered
        """
        # Navigate to "Registration"
        self.get("https://reg-prod.ec.louisiana.edu/StudentRegistrationSsb/ssb/registration")

        # Click "Register for Classes"
        self.click_by_id("registerLink")

        # Open drop down and select term
        self.click_by_id("s2id_txt_term")
        self.click_by_xpath(f"//div[contains(text(), \'{term}\')]")
        self.click_by_id("term-go")

    def check_for_errors(self) -> list:
        """Get list of errors present.

        Returns:
            list: List of errors
        """
        # If notification center is visible...
        if self.id_is_present("notification-center"):

            # And errors are present...
            while self.xpath_is_present("//ul[@class=\'error-container\']/li"):

                # Notification window may need to be reopened
                if self.xpath_is_present("//div[contains(@class, \'notification-center-flyout-hidden\')]"):
                    self.click_by_id("notification-center")

                # Yield error message
                yield WebDriverWait(self, 10).until(
                    EC.presence_of_element_located((
                        By.XPATH, 
                        "//ul[@class=\'error-container\']/li/div/a"
                    ))
                ).text

                # And close error message
                self.click_by_xpath("//ul[@class=\'error-container\']/li/div/button[text()=\'Ok\']")

    def clear_subject_input(self) -> None:
        """Clear previously searched subjects from input."""
        try:
            for e in WebDriverWait(self, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "select2-search-choice-close"))
            ): e.click()

        except Exception as e:
            return

    def click_by_id(self, id: str) -> None:
        """Click element located by xpath.

        Args:
            id (str): ID of element
        """
        try:
            WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.ID, id))
            ).click()

        except Exception as e:
            self.logger.error(f"An error occured: {e}")

    def click_by_xpath(self, xpath: str) -> None:
        """Click element located by xpath.

        Args:
            xpath (str): Xpath location of element
        """
        try:
            WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            ).click()

        except Exception as e:
            self.logger.error(f"An error occured: {e}")

    def get_summary_report(self) -> list:
        """Provide summary report.

        Returns:
            list: List of course registration statuses
        """

        for e in WebDriverWait(self, 10).until(
            EC.presence_of_all_elements_located((
            By.XPATH, 
            "//div[@id=\'summaryBody\']/div/div/table/tbody/tr"
        ))):
            yield {
                "title":    e.find_element(By.XPATH, ".//td[1]").text,
                "details":  e.find_element(By.XPATH, ".//td[2]").text,
                "hours":    e.find_element(By.XPATH, ".//td[3]").text,
                "crn":      e.find_element(By.XPATH, ".//td[4]").text,
                "type":     e.find_element(By.XPATH, ".//td[5]").text,
                "status":   e.find_element(By.XPATH, ".//td[6]/span").text,
            }

    def id_is_present(self, id: str) -> bool:
        """Indicate presence of element possessing specified ID.

        Args:
            id (str): Element ID

        Returns:
            bool: True if located, False otheriwse
        """
        try:
            # If element is present...
            WebDriverWait(self, 3).until(
                EC.presence_of_element_located((By.ID, id))
            )

            return True

        except Exception as e:
            return False


    def kill(self) -> None:
        """Close and quit webdriver."""
        # Close browser window and quit process
        self.logger.info("Killing driver...")
        self.close()
        self.quit()

    def login(self) -> None:
        """Log into ULink."""
        self.logger.info("Logging into ULink")

        # Navigate to ULink
        self.get("https://lum-prod.ec.louisiana.edu/")

        # Enter username (CLID) and password
        self.send_keys_by_id("username", self.config.get_clid())
        self.send_keys_by_id("password", self.config.get_pswd())

        # Click "SIGN IN"
        self.click_by_xpath("//button[contains(text(), 'Sign In')]")

        # Confirm absence of error
        if self.id_is_present("error-msg"):
            self.logger.critical("Credentials appear to be invalid. Please verify that they are correct before proceeding.")
            exit(1)

        # Report success
        self.logger.info("Login successful")

    def logout(self) -> None:
        """Logout of ULink."""
        self.logger.info("Logging out of ULink")

        # Navigate back to main page
        self.get("https://lum-prod.ec.louisiana.edu/")

        # Click "Sign Out"
        self.click_by_xpath("//a[contains(text(), 'Sign Out')]")

        # Verify success
        self.id_is_present("username")

        # Report success
        self.logger.info("Logout successful")

    def send_keys_by_id(self, id: str, text: str, clear_first: bool = False, wait: int = None) -> None:
        """Locate text field element and insert provided text.

        Args:
            id (str): Text field element ID
            text (str): Text to be inserted
            clear_first (bool): Clear input field before sending keys
            wait (int): Wait seconds before sending keys
        """
        try:
            if wait: time.sleep(wait)

            if clear_first:
                WebDriverWait(self, 10).until(
                    EC.presence_of_element_located((By.ID, id))
                ).send_keys(Keys.CONTROL + "a")

                WebDriverWait(self, 10).until(
                    EC.presence_of_element_located((By.ID, id))
                ).send_keys(Keys.DELETE)

            WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.ID, id))
            ).send_keys(text)

        except Exception as e:
            self.logger.error(f"An error occured: {e}")

    def xpath_is_present(self, xpath: str) -> bool:
        """Indicate presence of element possessing specified ID.

        Args:
            xpath (str): Element XPATH

        Returns:
            bool: True if located, False otheriwse
        """
        try:
            # If element is present...
            WebDriverWait(self, 3).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )

            return True

        except Exception as e:
            return False