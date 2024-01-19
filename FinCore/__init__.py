import logging
import os
from RDBMS.PostgreSQL import PostgreSQL

# Get the current script path
CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))

# Traverse up one level to reach the main folder
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_FILE_PATH, ".."))

# Create a formatter and set the formatter for the handlers
FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Create file handlers and set their log levels
FILE_HANDLER = logging.FileHandler(os.path.join(PROJECT_ROOT, os.path.join('FinCore', 'FinCore.log')))
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)

# init scope level Logger.
Logger = logging.getLogger(__name__)
Logger.addHandler(FILE_HANDLER)
Logger.setLevel(logging.DEBUG)

# SQL instance
PostgreSQL_DB = PostgreSQL()

# Defines
RECORD_EXIST = 0
SQL_QUERY_FAILED = -1
SINGLE_LIST = 0
SINGLE_TUPLE = 0