"""Configuration utilities."""

import os, yaml

from configparser       import MissingSectionHeaderError
from configparser_crypt import ConfigParserCrypt

from utils              import ARGS

class Config():
    """Configuration class."""

    def __init__(self):
        """Initialize Config object."""

        # Parse and store credentials & courses
        self.__credentials =    self.parse_credentials()
        self.__courses =        self.parse_yaml(ARGS.courses_path)
        self.__drivers =        self.parse_yaml(ARGS.drivers_path)

    def get_clid(self) -> str:
        """Provide CLID from credentials.

        Returns:
            str: CLID
        """
        return self.__credentials['clid']
    
    def get_courses(self) -> dict:
        """Provide dictionary of courses.

        Returns:
            dict: Dictionary format of courses
        """
        return self.__courses
    
    def get_driver(self, driver: str) -> str:
        """Provide dictionary of driver paths.

        Args:
            driver (str): Browser driver being requested (chrome/firefox)

        Returns:
            str: Driver path
        """
        return self.__drivers[driver]
    
    def get_pswd(self) -> str:
        """Provide password from credentials.

        Returns:
            str: Password
        """
        return self.__credentials['pswd']
    
    def parse_yaml(self, path: str) -> dict:
        """Parse courses.yaml file.

        Args:
            path (str): Path to YAML file

        Returns:
            dict: Dictionary format of courses
        """
        try:
            # Open courses.yaml
            with open(path, 'r') as file_in:

                # Initialize parser & read file
                return dict(yaml.safe_load(file_in))

        except FileNotFoundError:
            raise FileNotFoundError(f"{path} not found. Please ensure there exists an .yaml file containing course choices.")

    def parse_credentials(self) -> dict:
        """Parse credential.ini file.

        Returns:
            dict: Dictionary format of credentials
        """
        # Initialize parser
        parser = ConfigParserCrypt()

        # Fetch/generate key
        if os.path.exists(ARGS.config_key):
            parser.aes_key =  open(ARGS.config_key, 'rb').read()
        else:
            parser.generate_key()
            with open(ARGS.config_key, 'wb') as key_file:
                key_file.write(parser.aes_key)

        # Read .ini file (properties)
        try:
            parser.read(ARGS.credentials_path)

        except MissingSectionHeaderError:
            parser.read_encrypted(ARGS.credentials_path)

        except FileNotFoundError:
            raise FileNotFoundError(f"{ARGS.credentials_path} not found. Please ensure there exists an .ini file containing student credentials.")

        # Encrypt & write back
        finally:
            with open(ARGS.credentials_path, 'wb') as file_out:
                parser.write_encrypted(file_out)

            return dict(parser.items("credentials"))