import logging
import os
from FinCore.Core import Application

FIN_CORE = Application()


# Get the current script path
CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))

# Traverse up one level to reach the main folder
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_FILE_PATH, ".."))
# Configure the logging module

# Create a formatter and set the formatter for the handlers
FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Create file handlers and set their log levels
FILE_HANDLER = logging.FileHandler(os.path.join(PROJECT_ROOT, os.path.join('FinWebApp', 'FinWebApp.log')))
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)

# init scope level Logger.
Logger = logging.getLogger(__name__)
Logger.addHandler(FILE_HANDLER)
Logger.setLevel(logging.DEBUG)

# Define
FIRST_IDX =              0
INVALID_ANSWER =        -1
INVALID_KEY             = 'None'
FILE_UPLOAD_SUCCESS =   200
FILE_SIZE_TOO_BIG =     201
FILE_WRONG_TYPE =       202
FILE_VALIDATION_ERROR = 203
FILE_UPLOAD_ERROR =     204
FILE_WRONG_STRUCTURE =  210

