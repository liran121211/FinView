import logging
import os

# Get the current script path
CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))

# Traverse up one level to reach the main folder
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_FILE_PATH, ".."))

logging.basicConfig(
    filemode='w',  # Use 'w' to override the existing log file
    level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Specify the log message format
)
# Create file handlers and set their log levels
FILE_HANDLER = logging.FileHandler(os.path.join(PROJECT_ROOT, os.path.join('DataParser', 'DataParser.log')))
FILE_HANDLER.setLevel(logging.DEBUG)

# Create a formatter and set the formatter for the handlers
FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Defines
INVALID_INDEX = -1
