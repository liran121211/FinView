import logging
import os
from INIParser.INIFileHandler import BusinessesCategoriesINI

CREDIT_CARD_TRANSACTIONS_CATEGORIES = {
    '1': 'ביטוח',
    '2': 'מזון וצריכה',
    '3': 'שרותי תקשורת',
    '4': 'רפואה וקוסמטיקה',
    '5': 'מחשבים, תוכנות וחשמל',
    '6': 'פנאי ובידור',
    '7': 'עירייה וממשלה',
    '8': 'תחבורה',
    '9': 'שונות',
}


BANK_TRANSACTIONS_CATEGORIES = {
    '1': 'הכנסה',
    '2': 'הוצאה',
    '3': 'חיסכון והשקעות',
    '4': 'הלוואות',
    '5': 'עמלות',
    '6': 'העברות ומשיכות',
    '7': 'מיסים',
    '8': 'שונות',
    '9': 'כרטיסי אשראי',
}


# Get the current script path
CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))

# Traverse up one level to reach the main folder
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_FILE_PATH, ".."))
# Configure the logging module

# Create a formatter and set the formatter for the handlers
FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Create file handlers and set their log levels
FILE_HANDLER = logging.FileHandler(os.path.join(PROJECT_ROOT, os.path.join('AI', 'AI.log')))
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)

# init scope level Logger.
Logger = logging.getLogger(__name__)
Logger.addHandler(FILE_HANDLER)
Logger.setLevel(logging.DEBUG)

# INI Parser instance
BusinessesCategoriesINIParser = BusinessesCategoriesINI('BusinessesCategories.ini')
BusinessesCategoriesINIParser.read_ini()