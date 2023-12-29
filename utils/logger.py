"""Logging utilities."""

import logging, os, sys

from utils.arguments    import ARGS

# Initialize logger
LOGGER =            logging.getLogger('advisobot')

# Set logging level
LOGGER.setLevel(ARGS.logging_level)

# Ensure that logging path exists
os.makedirs(ARGS.logging_path, exist_ok=True)

# Define console handler
stdout_handler =    logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(ARGS.logging_level)
stdout_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s'))
LOGGER.addHandler(stdout_handler)

# Define file handler
file_handler =      logging.FileHandler(f"{ARGS.logging_path}/advisobot_{ARGS.action}.log")
file_handler.setLevel(ARGS.logging_level)
file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s'))
LOGGER.addHandler(file_handler)