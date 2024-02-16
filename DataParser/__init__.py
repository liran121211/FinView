import logging
import os

# Get the current script path
CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))

# Traverse up one level to reach the main folder
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_FILE_PATH, ".."))

# Create a formatter and set the formatter for the handlers
FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Create file handlers and set their log levels
FILE_HANDLER = logging.FileHandler(os.path.join(PROJECT_ROOT, os.path.join('DataParser', 'DataParser.log')))
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)

# Init scope level Logger.
Logger = logging.getLogger(__name__)
Logger.addHandler(FILE_HANDLER)
Logger.setLevel(logging.DEBUG)

# Defines
INVALID_INDEX = -1
BANK_DUMMY_ACCOUNT_NUMBER = '000-0000/00'
CREDIT_CARD_DUMMY_LAST_4_DIGITS = 0000

# Transaction Types
REGULAR_PAYMENT = 'עסקה רגילה'
CREDIT_PAYMENT = 'עסקת תשלומים'
DIRECT_DEBIT = 'הוראת קבע'
UNDETERMINED_PAYMENT_TYPE = 'סוג עסקה לא ידוע'
