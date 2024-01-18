import logging
import os

# Get the current script path
CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))

# Traverse up one level to reach the main folder
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_FILE_PATH, ".."))
# Configure the logging module

logging.basicConfig(
    filemode='w',  # Use 'w' to override the existing log file
    level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Specify the log message format
)

# Create file handlers and set their log levels
FILE_HANDLER = logging.FileHandler(os.path.join(PROJECT_ROOT, os.path.join('RDBMS', 'RDBMS.log')))
FILE_HANDLER.setLevel(logging.DEBUG)

# Create a formatter and set the formatter for the handlers
FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# SQL Server Configuration
DATABASE_NAME = "FinView"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "12456622"
DATABASE_HOST = "localhost"
DATABASE_PORT = "5432"

# Defines

YES = 1
NO = 0

CONNECTED = 1
NOT_CONNECTED = 0

VALUE_EXIST = 1
VALUE_NOT_EXIST = 0

DEFAULT_KEY = "NONE"
SQL_ERROR = -1

