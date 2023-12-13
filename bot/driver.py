"""Advisobot driver and utilities."""

import os

from selenium                           import webdriver
from selenium.webdriver.common.by       import By
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

        # Click "Sign Out"
        self.click_by_xpath("//a[contains(text(), 'Sign Out')]")

        # Verify success
        self.id_is_present("username")

        # Report success
        self.logger.info("Logout successful")

    def send_keys_by_id(self, id: str, text: str) -> None:
        """Locate text field element and insert provided text.

        Args:
            id (str): Text field element ID
            text (str): Text to be inserted
        """
        try:
            WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.ID, id))
            ).send_keys(text)

        except Exception as e:
            self.logger.error(f"An error occured: {e}")