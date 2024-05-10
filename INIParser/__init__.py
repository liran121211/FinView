# Get the current script path
import logging
import os

CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))

# Traverse up one level to reach the main folder
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_FILE_PATH, ".."))
# Configure the logging module

# Create a formatter and set the formatter for the handlers
FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Create file handlers and set their log levels
FILE_HANDLER = logging.FileHandler(os.path.join(PROJECT_ROOT, os.path.join('INIParser', 'INIParser.log')))
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)

# init scope level Logger.
Logger = logging.getLogger(__name__)
Logger.addHandler(FILE_HANDLER)
Logger.setLevel(logging.DEBUG)

INVALID_CONFIG_FILE = -1