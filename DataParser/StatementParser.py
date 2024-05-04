import locale

import pandas as pd
import datetime
import os.path
import re
from abc import ABC, abstractmethod
from typing import AnyStr, Any

from PyPDF2 import PdfReader
from openpyxl.reader.excel import load_workbook
from openpyxl.utils.exceptions import InvalidFileException
from DataParser import *


class Parser:
    def __init__(self, file_path: AnyStr):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(FILE_HANDLER)
        self.filename = os.path.basename(file_path)
        self.file_absolute_path = os.path.join(PROJECT_ROOT, file_path)

        # validate xlsx file before init instance
        if self.is_xlsx_file(self.file_absolute_path):
            self.__df = pd.read_excel(self.file_absolute_path, engine='openpyxl')
            self.is_valid = True

        # validate pdf file before init instance
        elif self.is_pdf_file(self.file_absolute_path):
            # collect data from pdf into dataframe from class method: extract_base_data
            self.__df = pd.DataFrame()
            self.is_valid = True
        else:
            self.is_valid = False

    @staticmethod
    def extract_text_from_pdf(file_path: AnyStr) -> AnyStr:
        pdf_text = ""
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            num_pages = len(reader.pages)
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                pdf_text += page.extract_text()

        return pdf_text

    @staticmethod
    def is_xlsx_file(file_path: AnyStr) -> bool:
        try:
            # Try to load the file with openpyxl
            load_workbook(file_path)
            return True
        except InvalidFileException:
            return False

    @staticmethod
    def is_pdf_file(file_path: AnyStr) -> bool:
        with open(file_path, 'rb') as file:
            header = file.read(4)  # Read the first 4 bytes
            return header.startswith(b'%PDF')

    @abstractmethod
    def parse(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def extract_base_data(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def validate_file_structure(self):
        pass

    @property
    def data(self):
        return self.__df


class LeumiParser(Parser, ABC):
    def __init__(self, file_path: AnyStr):
        super().__init__(file_path)

    def retrieve_first_index(self) -> int:
        # Check if the required columns exist in the DataFrame
        required_columns = {'תאריך העסקה', 'שם בית העסק', 'סכום חיוב'}

        for idx, values in self.data.iterrows():
            col_values = set(v[1] for v in values.items())
            if len(required_columns & col_values) > 0:
                return int(str(idx)) + 1

        self.logger.exception(f"LeumiParser - Could not retrieve first index from file.")
        return INVALID_INDEX

    def retrieve_last_index(self, start_idx) -> int:
        date_of_transaction, business_name, total_amount = 0, 1, 5
        for idx, values in self.data.iloc[start_idx:].iterrows():
            if pd.isna(values.iloc[date_of_transaction]) or pd.isna(values.iloc[business_name]) or pd.isna(values.iloc[total_amount]):
                return idx

        self.logger.exception(f"LeumiParser - Could not retrieve last index from file.")
        return INVALID_INDEX

    def extract_base_data(self) -> pd.DataFrame:
        if not self.is_valid:
            self.logger.critical(f"Provided file: {self.filename} is not a valid xlsx/pdf")
            return pd.DataFrame(columns=['date_of_transaction', 'business_name', 'charge_amount', 'total_amount', 'transaction_type', 'transaction_provider', 'last_4_digits', 'card_type', 'category'])

        # extract last 4 digits
        last_4_digits = CREDIT_CARD_DUMMY_LAST_4_DIGITS
        for _tuple in self.data[self.data.keys()[0]].items():
            for val in _tuple:
                if not isinstance(val, datetime.datetime):
                    matches = re.findall(r'\b\d{4}\b', str(val))
                    if len(matches) > 0 and 'לכרטיס' in val.split():
                        last_4_digits = matches[0]

        temp_df = pd.DataFrame(columns=['date_of_transaction', 'business_name', 'charge_amount', 'total_amount', 'transaction_type', 'transaction_provider', 'last_4_digits', 'card_type', 'category'])
        date_of_transaction_idx, business_name_idx, charge_amount_idx, transaction_type_idx, total_amount_idx = 0, 1, 2, 3, 5
        first_idx = self.retrieve_first_index()
        last_idx = self.retrieve_last_index(first_idx)
        current_df = self.data.iloc[first_idx: last_idx]

        # avoid invalid data fetched from selected first/last indexes of xlsx.
        if first_idx == INVALID_INDEX or last_idx == INVALID_INDEX:
            return temp_df

        for idx, column in current_df.iterrows():
            try:
                if pd.to_datetime(column.iloc[date_of_transaction_idx], dayfirst=True):
                    if pd.isna(column.iloc[date_of_transaction_idx]) or pd.isnull(column.iloc[date_of_transaction_idx]):
                        continue

                if pd.isna(column.iloc[business_name_idx]) or pd.isnull(column.iloc[business_name_idx]):
                    continue

                if pd.isna(column.iloc[charge_amount_idx]) or pd.isnull(column.iloc[charge_amount_idx]):
                    continue

                if pd.isna(column.iloc[transaction_type_idx]) or pd.isnull(column.iloc[transaction_type_idx]):
                    continue

                if pd.isna(column.iloc[total_amount_idx]) or pd.isnull(column.iloc[total_amount_idx]):
                    continue

                data = {
                    'date_of_transaction':  pd.to_datetime(column.iloc[date_of_transaction_idx], dayfirst=True),
                    'business_name':        column.iloc[business_name_idx],
                    'charge_amount':        column.iloc[charge_amount_idx],
                    'transaction_type':     self.extract_transaction_type(column.iloc[transaction_type_idx]),
                    'total_amount':         column.iloc[total_amount_idx],
                    'last_4_digits':        last_4_digits,
                    'transaction_provider': 'Leumi',
                    'card_type':            'Unknown',
                }
                temp_df.loc[len(temp_df)] = pd.Series(data)

            except ValueError:
                continue

        return temp_df.iloc[first_idx: last_idx]

    def extract_transaction_type(self, transaction_type: AnyStr) -> AnyStr:
        if transaction_type == REGULAR_PAYMENT:
            return REGULAR_PAYMENT

        if 'תשלומים' in transaction_type:
            return CREDIT_PAYMENT

        if 'קבע' in transaction_type:
            return DIRECT_DEBIT

        return UNDETERMINED_PAYMENT_TYPE

    def parse(self) -> pd.DataFrame:
        return self.extract_base_data().reset_index(drop=True)

    def validate_file_structure(self):
        valid_statement = True

        try:
            if 'בנק לאומי' not in self.data.columns[0]:
                valid_statement = False
            if "מס' חשבון" not in self.data.iat[0, 0]:
                valid_statement = False

        except ValueError:
            Logger.critical('Invalid date string in LeumiParser: validate_file_structure().')
        except IndexError:
            Logger.critical('Invalid data indexes in LeumiParser: validate_file_structure().')

        date_of_transaction_idx, business_name_idx, charge_amount_idx = 0, 1, 2
        transaction_type_idx, transaction_note_idx, total_amount_idx = 3, 4, 5

        try:
            columns_idx = 9
            if not self.data.iat[columns_idx, date_of_transaction_idx] == 'תאריך העסקה':
                valid_statement = False
            if not self.data.iat[columns_idx, business_name_idx] == 'שם בית העסק':
                valid_statement = False
            if not self.data.iat[columns_idx, charge_amount_idx] == 'סכום העסקה':
                valid_statement = False
            if not self.data.iat[columns_idx, transaction_type_idx] == 'סוג העסקה':
                valid_statement = False
            if not self.data.iat[columns_idx, transaction_note_idx] == 'פרטים':
                valid_statement = False
            if not self.data.iat[columns_idx, total_amount_idx] == 'סכום חיוב':
                valid_statement = False

        except IndexError:
            return False

        return valid_statement


class CalOnlineParser(Parser, ABC):
    def __init__(self, file_path: AnyStr):
        super().__init__(file_path)

    def extract_base_data(self) -> pd.DataFrame:
        if not self.is_valid:
            self.logger.critical(f"Provided file: {self.filename} is not a valid xlsx/pdf")
            return pd.DataFrame(columns=['date_of_transaction', 'business_name', 'charge_amount', 'total_amount', 'transaction_type', 'transaction_provider', 'last_4_digits', 'card_type' 'category'])

        # Check if the required columns exist in the DataFrame
        info_rows = pd.DataFrame(columns=['date_of_transaction', 'business_name', 'charge_amount', 'total_amount', 'transaction_type', 'transaction_provider', 'last_4_digits', 'card_type', 'category'])
        date_of_transaction_idx, business_name_idx, charge_amount_idx, transaction_type_idx, total_amount_idx = 0, 1, 3, 4, 2

        # assume data not found at first.
        last_4_digits = CREDIT_CARD_DUMMY_LAST_4_DIGITS
        card_type = 'Unknown'

        # extract last 4 card digits from file
        if len(self.data.keys()) > 0:
            last_4_digits = re.findall(r'\b\d{4}\b', self.data.keys()[0])
            card_type = 'Visa' if 'ויזה' in self.data.keys()[0] else 'MasterCard' if 'מסטרקארד' in self.data.keys()[0] else 'Unknown'

            if len(last_4_digits) > 0 and last_4_digits[0].isdigit():
                last_4_digits = last_4_digits[0]
            else:
                last_4_digits = CREDIT_CARD_DUMMY_LAST_4_DIGITS

        for idx, column in self.data.iterrows():
            try:
                if pd.to_datetime(column.iloc[date_of_transaction_idx], dayfirst=True):
                    if pd.isna(column.iloc[date_of_transaction_idx]) or pd.isnull(column.iloc[date_of_transaction_idx]):
                        continue

                if pd.isna(column.iloc[business_name_idx]) or pd.isnull(column.iloc[business_name_idx]):
                    continue

                if pd.isna(column.iloc[charge_amount_idx]) or pd.isnull(column.iloc[charge_amount_idx]):
                    continue

                if pd.isna(column.iloc[transaction_type_idx]) or pd.isnull(column.iloc[transaction_type_idx]):
                    continue

                if pd.isna(column.iloc[total_amount_idx]) or pd.isnull(column.iloc[total_amount_idx]):
                    continue

                data = {
                    'date_of_transaction':  pd.to_datetime(column.iloc[date_of_transaction_idx], dayfirst=True),
                    'business_name':        column.iloc[business_name_idx],
                    'charge_amount':        column.iloc[charge_amount_idx],
                    'transaction_type':     self.extract_transaction_type(column.iloc[transaction_type_idx]),
                    'total_amount':         column.iloc[total_amount_idx],
                    'last_4_digits':        last_4_digits,
                    'card_type':            card_type,
                    'transaction_provider': 'Cal Online',
                }
                info_rows.loc[len(info_rows)] = pd.Series(data)

            except ValueError:
                continue

        return info_rows

    def parse(self) -> pd.DataFrame:
        return self.extract_base_data().reset_index(drop=True)

    def extract_transaction_type(self, transaction_type: AnyStr) -> AnyStr:
        if 'רגילה' in transaction_type:
            return REGULAR_PAYMENT

        if 'תשלומים' in transaction_type:
            return CREDIT_PAYMENT

        if 'קבע' in transaction_type:
            return DIRECT_DEBIT

        return UNDETERMINED_PAYMENT_TYPE

    def validate_file_structure(self):
        valid_statement = True

        try:
            if 'פירוט עסקאות לחשבו' not in self.data.columns[0]:
                valid_statement = False

            date_of_transaction_idx, business_name_idx, charge_amount_idx, transaction_type_idx = 0, 1, 3, 4
            total_amount_idx, transaction_category_idx, transaction_note_idx = 2, 5, 6
            columns_idx = 0
            if not self.data.iat[columns_idx, date_of_transaction_idx] == 'תאריך עסקה':
                valid_statement = False
            if not self.data.iat[columns_idx, business_name_idx] == 'שם בית עסק':
                valid_statement = False
            if not self.data.iat[columns_idx, charge_amount_idx] == 'סכום חיוב':
                valid_statement = False
            if not self.data.iat[columns_idx, total_amount_idx] == 'סכום עסקה':
                valid_statement = False
            if not self.data.iat[columns_idx, transaction_type_idx] == 'סוג עסקה':
                valid_statement = False
            if not self.data.iat[columns_idx, transaction_category_idx] == 'ענף':
                valid_statement = False
            if not self.data.iat[columns_idx, transaction_note_idx] == 'הערות':
                valid_statement = False

        except IndexError:
            return False

        return valid_statement


class MaxParser(Parser, ABC):
    def __init__(self, file_path: AnyStr):
        super().__init__(file_path)

    def extract_base_data(self) -> pd.DataFrame:
        if not self.is_valid:
            self.logger.critical(f"Provided file: {self.filename} is not a valid xlsx/pdf")
            return pd.DataFrame(columns=['date_of_transaction', 'business_name', 'charge_amount', 'total_amount', 'transaction_type', 'transaction_provider', 'last_4_digits', 'card_type', 'category'])

        # Check if the required columns exist in the DataFrame
        info_rows = pd.DataFrame(columns=['date_of_transaction', 'business_name', 'charge_amount', 'total_amount', 'transaction_type', 'transaction_provider', 'last_4_digits', 'card_type', 'category'])
        date_of_transaction_idx, business_name_idx, last_4_digits, charge_amount_idx, transaction_type_idx, total_amount_idx = 0, 1, 3, 5, 10, 7

        for idx, column in self.data.iterrows():
            try:
                if pd.to_datetime(column.iloc[date_of_transaction_idx], dayfirst=True):
                    if pd.isna(column.iloc[date_of_transaction_idx]) or pd.isnull(column.iloc[date_of_transaction_idx]):
                        continue

                if pd.isna(column.iloc[business_name_idx]) or pd.isnull(column.iloc[business_name_idx]):
                    continue

                if pd.isna(column.iloc[last_4_digits]) or pd.isnull(column.iloc[last_4_digits]):
                    continue

                if pd.isna(column.iloc[charge_amount_idx]) or pd.isnull(column.iloc[charge_amount_idx]):
                    continue

                if pd.isna(column.iloc[transaction_type_idx]) or pd.isnull(column.iloc[transaction_type_idx]):
                    continue

                if pd.isna(column.iloc[total_amount_idx]) or pd.isnull(column.iloc[total_amount_idx]):
                    continue

                data = {
                    'date_of_transaction':  pd.to_datetime(column.iloc[date_of_transaction_idx], dayfirst=True),
                    'business_name':        column.iloc[business_name_idx],
                    'last_4_digits':        column.iloc[last_4_digits],
                    'charge_amount':        column.iloc[charge_amount_idx],
                    'transaction_type':     self.extract_transaction_type(column.iloc[transaction_type_idx]),
                    'total_amount':         column.iloc[total_amount_idx],
                    'transaction_provider': 'Max',
                    'card_type':            'Unknown',
                }
                info_rows.loc[len(info_rows)] = pd.Series(data)

            except ValueError:
                continue

        return info_rows

    def parse(self) -> pd.DataFrame:
        return self.extract_base_data().reset_index(drop=True)

    def extract_transaction_type(self, transaction_type: AnyStr) -> AnyStr:
        if 'רגילה' in transaction_type:
            return REGULAR_PAYMENT

        if 'תשלום' in transaction_type:
            return CREDIT_PAYMENT

        if 'קבע' in transaction_type:
            return DIRECT_DEBIT

        return UNDETERMINED_PAYMENT_TYPE

    def validate_file_structure(self):
        valid_statement = True

        try:
            if not pd.to_datetime(self.data.iat[1, 0], format='%m/%Y') or pd.isna(self.data.iat[1, 0]):
                valid_statement = False
        except ValueError:
            Logger.critical('Invalid date string in MaxParser: validate_file_structure().')
        except IndexError:
            Logger.critical('Invalid data indexes in MaxParser: validate_file_structure().')

        try:
            date_of_transaction_idx, business_name_idx, transaction_category_idx, last_4_digits_idx = 0, 1, 2, 3
            transaction_type_idx, charge_amount_idx, total_amount_idx, transaction_note_idx = 4, 5, 7, 10
            columns_idx = 2
            if not self.data.iat[columns_idx, date_of_transaction_idx] == 'תאריך עסקה':
                valid_statement = False
            if not self.data.iat[columns_idx, business_name_idx] == 'שם בית העסק':
                valid_statement = False
            if not self.data.iat[columns_idx, charge_amount_idx] == 'סכום חיוב':
                valid_statement = False
            if not self.data.iat[columns_idx, total_amount_idx] == 'סכום עסקה מקורי':
                valid_statement = False
            if not self.data.iat[columns_idx, transaction_type_idx] == 'סוג עסקה':
                valid_statement = False
            if not self.data.iat[columns_idx, transaction_category_idx] == 'קטגוריה':
                valid_statement = False
            if not self.data.iat[columns_idx, transaction_note_idx] == 'הערות':
                valid_statement = False

        except IndexError:
            return False

        return valid_statement


class IsracardParser(Parser, ABC):
    def __init__(self, file_path: AnyStr):
        super().__init__(file_path)

    def extract_base_data(self) -> pd.DataFrame:
        if not self.is_valid:
            self.logger.critical(f"Provided file: {self.filename} is not a valid xlsx/pdf")
            return pd.DataFrame(columns=['date_of_transaction', 'business_name', 'charge_amount', 'total_amount', 'transaction_type', 'transaction_provider', 'last_4_digits', 'card_type' 'category'])

        # Check if the required columns exist in the DataFrame
        info_rows = pd.DataFrame(columns=['date_of_transaction', 'business_name', 'charge_amount', 'total_amount', 'transaction_type', 'transaction_provider', 'last_4_digits', 'card_type', 'category'])
        date_of_transaction_idx, business_name_idx, charge_amount_idx, total_amount_idx = 0, 1, 4, 2

        # assume data not found first.
        last_4_digits = CREDIT_CARD_DUMMY_LAST_4_DIGITS
        card_type = 'Unknown'

        # extract last 4 card digits from file
        if len(self.data.keys()) > 0:
            first_col_name = self.data.columns[0]

            if len(self.data[first_col_name]) >= 2:
                last_4_digits_cell = self.data[first_col_name].iloc[2]
                last_4_digits = re.findall(r'\b\d{4}\b', last_4_digits_cell)
                card_type = 'Visa' if 'ויזה' in self.data.keys()[0] else 'MasterCard' if 'מסטרקארד' in last_4_digits_cell else 'Unknown'

                if len(last_4_digits) > 0 and last_4_digits[0].isdigit():
                    last_4_digits = last_4_digits[0]
                else:
                    last_4_digits = CREDIT_CARD_DUMMY_LAST_4_DIGITS

        for idx, column in self.data.iterrows():
            try:
                if column.iloc[0] == 'עסקאות בחו˝ל':
                    date_of_transaction_idx, business_name_idx, charge_amount_idx, total_amount_idx = 0, 2, 5, 5

                if pd.to_datetime(column.iloc[date_of_transaction_idx], dayfirst=True):
                    if pd.isna(column.iloc[date_of_transaction_idx]) or pd.isnull(column.iloc[date_of_transaction_idx]):
                        continue

                if pd.isna(column.iloc[business_name_idx]) or pd.isnull(column.iloc[business_name_idx]):
                    continue

                if pd.isna(column.iloc[charge_amount_idx]) or pd.isnull(column.iloc[charge_amount_idx]):
                    continue

                # TODO: find out where transaction type is showed in Isracard xlsx
                # if pd.isna(column.iloc[transaction_type_idx]) or pd.isnull(column.iloc[transaction_type_idx]):
                #     continue

                if pd.isna(column.iloc[total_amount_idx]) or pd.isnull(column.iloc[total_amount_idx]):
                    continue

                if pd.isna(pd.to_numeric(column.iloc[total_amount_idx], errors='coerce')):
                    continue

                data = {
                    'date_of_transaction':  pd.to_datetime(column.iloc[date_of_transaction_idx], dayfirst=True),
                    'business_name':        column.iloc[business_name_idx],
                    'charge_amount':        column.iloc[charge_amount_idx],
                    'transaction_type':     UNDETERMINED_PAYMENT_TYPE,
                    'total_amount':         column.iloc[total_amount_idx],
                    'last_4_digits':        last_4_digits,
                    'card_type':            card_type,
                    'transaction_provider': 'Isracard',
                }
                info_rows.loc[len(info_rows)] = pd.Series(data)

            except ValueError:
                continue

        return info_rows

    def parse(self) -> pd.DataFrame:
        return self.extract_base_data().reset_index(drop=True)

    def extract_transaction_type(self, transaction_type: AnyStr) -> AnyStr:
        if 'רגילה' in transaction_type:
            return REGULAR_PAYMENT

        if 'תשלומים' in transaction_type:
            return CREDIT_PAYMENT

        if 'קבע' in transaction_type:
            return DIRECT_DEBIT

        return UNDETERMINED_PAYMENT_TYPE

    def validate_file_structure(self):
        valid_statement = True

        try:
            if not pd.to_datetime(self.data.iat[2, 2], format='%d/%m/%y') or pd.isna(self.data.iat[2, 2]):
                valid_statement = False
            if self.data.iat[2, 1] != 'מועד חיוב':
                valid_statement = False
        except ValueError:
            Logger.critical('Invalid date string in IsracardParser: validate_file_structure().')
        except IndexError:
            Logger.critical('Invalid data indexes in IsracardParser: validate_file_structure().')

        date_of_transaction_idx, business_name_idx, total_amount_idx, charge_amount_idx = 0, 1, 2, 4
        transaction_identifier_idx, transaction_note_idx = 6, 7

        try:
            columns_idx = 4
            if not self.data.iat[columns_idx, date_of_transaction_idx] == 'תאריך רכישה':
                valid_statement = False
            if not self.data.iat[columns_idx, business_name_idx] == 'שם בית עסק':
                valid_statement = False
            if not self.data.iat[columns_idx, total_amount_idx] == 'סכום עסקה':
                valid_statement = False
            if not self.data.iat[columns_idx, charge_amount_idx] == 'סכום חיוב':
                valid_statement = False
            if not self.data.iat[columns_idx, transaction_identifier_idx] == 'מספר שובר':
                valid_statement = False
            if not self.data.iat[columns_idx, transaction_note_idx] == 'פירוט נוסף':
                valid_statement = False

        except IndexError:
            return False

        return valid_statement


class BankLeumiParser(Parser, ABC):
    def __init__(self, file_path: AnyStr):
        super().__init__(file_path)

    def extract_base_data(self) -> pd.DataFrame:
        if not self.is_valid:
            self.logger.critical(f"Provided file: {self.filename} is not a valid xlsx/pdf")
            return pd.DataFrame(columns=['transaction_date', 'transaction_description', 'transaction_reference', 'income_balance', 'outcome_balance', 'current_balance', 'account_number', 'transaction_provider', 'transaction_category'])

        # Check if the required columns exist in the DataFrame
        info_rows = pd.DataFrame(columns=['transaction_date', 'transaction_description', 'transaction_reference', 'income_balance', 'outcome_balance', 'current_balance', 'account_number', 'transaction_provider', 'transaction_category'])
        transaction_date, transaction_description, transaction_reference, income_balance, outcome_balance, current_balance = 0, 2, 3, 5, 4, 6

        for idx, column in self.data.iterrows():
            try:
                if pd.to_datetime(column.iloc[transaction_date], dayfirst=True):
                    if pd.isna(column.iloc[transaction_date]) or pd.isnull(column.iloc[transaction_date]):
                        continue

                if pd.isna(column.iloc[transaction_description]) or pd.isnull(column.iloc[transaction_description]):
                    continue

                if pd.isna(column.iloc[transaction_reference]) or pd.isnull(column.iloc[transaction_reference]):
                    continue

                if pd.isna(column.iloc[income_balance]) or pd.isnull(column.iloc[income_balance]):
                    continue

                if pd.isna(column.iloc[outcome_balance]) or pd.isnull(column.iloc[outcome_balance]):
                    continue

                if pd.isna(column.iloc[current_balance]) or pd.isnull(column.iloc[current_balance]):
                    continue

                data = {
                    'transaction_date':         pd.to_datetime(column.iloc[transaction_date], dayfirst=True),
                    'transaction_description':  re.sub('|'.join(map(re.escape, ['\u200e'])), '', str(column.iloc[transaction_description])),
                    'transaction_reference':    re.sub('|'.join(map(re.escape, ['\u200e', '-', ','])), '', str(column.iloc[transaction_reference])),
                    'income_balance':           re.sub('|'.join(map(re.escape, ['\u200e', '-', ','])), '', str(column.iloc[income_balance])),
                    'outcome_balance':          re.sub('|'.join(map(re.escape, ['\u200e', '-', ','])), '', str(column.iloc[outcome_balance])),
                    'current_balance':          re.sub('|'.join(map(re.escape, ['\u200e', '-', ','])), '', str(column.iloc[current_balance])),
                    'account_number':           self.extract_bank_leumi_account_number(),
                    'transaction_provider':     'Bank Leumi',
                }
                info_rows.loc[len(info_rows)] = pd.Series(data)

            except ValueError:
                continue

        return info_rows

    def parse(self) -> pd.DataFrame:
        return self.extract_base_data().reset_index(drop=True)

    def validate_file_structure(self):
        valid_statement = True

        try:
            if 'בנק לאומי' not in self.data.columns[0]:
                valid_statement = False

            if "מס' חשבון" not in self.data.iat[0, 0]:
                valid_statement = False

            if self.data.iat[3, 0] != "היתרה" and self.data.iat[3, 2] != "מסגרת האשראי" and self.data.iat[3, 4] != "נכון לתאריך":
                valid_statement = False

        except ValueError:
            Logger.critical('Invalid date string in BankLeumiParser: validate_file_structure().')
        except IndexError:
            Logger.critical('Invalid data indexes in BankLeumiParser: validate_file_structure().')

        try:
            date_of_transaction_idx, date_of_transaction_value_idx, transaction_description_idx = 0, 1, 2
            transaction_identifier_idx, transaction_outcome_idx, transaction_income_idx, transaction_current_idx = 3, 4, 5, 6
            columns_idx = 10
            if not self.data.iat[columns_idx, date_of_transaction_idx] == 'תאריך':
                valid_statement = False
            if not self.data.iat[columns_idx, date_of_transaction_value_idx] == 'תאריך ערך':
                valid_statement = False
            if not self.data.iat[columns_idx, transaction_description_idx] == 'תיאור':
                valid_statement = False
            if not self.data.iat[columns_idx, transaction_identifier_idx] == 'אסמכתא':
                valid_statement = False
            if not self.data.iat[columns_idx, transaction_outcome_idx] == 'בחובה':
                valid_statement = False
            if not self.data.iat[columns_idx, transaction_income_idx] == 'בזכות':
                valid_statement = False
            if not self.data.iat[columns_idx, transaction_current_idx] == 'היתרה בש"ח':
                valid_statement = False

        except IndexError:
            return False

        return valid_statement

    def extract_bank_leumi_account_number(self) -> AnyStr:
        try:
            bank_account_number = re.findall(r'[0-9/-]+', str(self.data.iloc[0, 0]))
            if '/' in bank_account_number[0] and '-' in bank_account_number[0]:
                return bank_account_number[0]
        except IndexError:
            return BANK_DUMMY_ACCOUNT_NUMBER

    @staticmethod
    def extract_current_bank_debit(df: pd.DataFrame) -> Any:
        try:
            if "היתרה" in df.iloc[3, 0] and isinstance(float(re.sub('|'.join(map(re.escape, ['\u200e', '₪', ])), '', df.iloc[5, 0])), (float, int)):
                return float(re.sub('|'.join(map(re.escape, ['\u200e', '₪', ])), '', df.iloc[5, 0]))
        except IndexError:
            return 0.0
        except ValueError:
            return 0.0
        except TypeError:
            if isinstance(float(df.iloc[5, 0]), (float, int)):
                return float(df.iloc[5, 0])
            else:
                return 0.0


class BankMizrahiTefahotParser(Parser, ABC):
    def __init__(self, file_path: AnyStr):
        super().__init__(file_path)

    def extract_base_data(self) -> pd.DataFrame:
        if not self.is_valid:
            self.logger.critical(f"Provided file: {self.filename} is not a valid xlsx/pdf")
            return pd.DataFrame(columns=['transaction_date', 'transaction_description', 'transaction_reference', 'income_balance', 'outcome_balance', 'current_balance', 'account_number', 'transaction_provider', 'transaction_category'])

        # Check if the required columns exist in the DataFrame
        info_rows = pd.DataFrame(columns=['transaction_date', 'transaction_description', 'transaction_reference', 'income_balance', 'outcome_balance', 'current_balance', 'account_number', 'transaction_provider', 'transaction_category'])

        # extract data from pdf file into Dataframe
        pdf_text = self.extract_text_from_pdf(self.file_absolute_path)
        for line in pdf_text.split('\n'):
            tokens = line.split()
            transaction_description_len = self.count_description_len(line)

            # define rules for valid data row
            transaction_description_indexes = []
            valid_transaction_row, transaction_descriptions_valid = True, True

            # define len to read from transaction description
            for idx in range(1, transaction_description_len + INDEX_INCREASE_BY_1):
                transaction_description_indexes.append(idx)

            # define indexes of columns
            transaction_date_idx = 0
            income_outcome_balance_idx = transaction_description_indexes[LAST_INDEX] + INDEX_INCREASE_BY_1
            current_balance_idx = income_outcome_balance_idx + INDEX_INCREASE_BY_1
            transaction_reference_idx = current_balance_idx + INDEX_INCREASE_BY_1

            try:
                if not self.is_valid_date(tokens[transaction_date_idx]):
                    valid_transaction_row = False

                for idx in transaction_description_indexes:
                    if not self.is_valid_description(tokens[idx]):
                        transaction_descriptions_valid = False

                if not self.is_valid_float(tokens[income_outcome_balance_idx]):
                    valid_transaction_row = False

                if not self.is_valid_float(tokens[current_balance_idx]):
                    valid_transaction_row = False

                if not self.is_valid_float(tokens[transaction_reference_idx]):
                    valid_transaction_row = False

            except IndexError:
                continue

            if valid_transaction_row and transaction_descriptions_valid:
                data = {
                    'transaction_date':         pd.to_datetime(tokens[transaction_date_idx], dayfirst=True),
                    'transaction_description':  (' '.join([str(tokens[idx]) for idx in transaction_description_indexes])),
                    'transaction_reference':    tokens[transaction_reference_idx],
                    'income_balance':           float(str(tokens[income_outcome_balance_idx]).replace(',', '').replace('-', '')) if '-' not in tokens[income_outcome_balance_idx] else 0.0,
                    'outcome_balance':          float(str(tokens[income_outcome_balance_idx]).replace(',', '').replace('-', '')) if '-' in tokens[income_outcome_balance_idx] else 0.0,
                    'current_balance':          float(str(tokens[current_balance_idx]).replace(',', '').replace('-', '')) * (-1) if '-' in tokens[income_outcome_balance_idx] else str(tokens[current_balance_idx]).replace(',', '').replace('-', ''),
                    'account_number':           self.extract_bank_mizrahi_tefahot_account_number(),
                    'transaction_provider':     'Mizrahi Tefahot',
                }
                info_rows.loc[len(info_rows)] = pd.Series(data)

        return info_rows

    def parse(self) -> pd.DataFrame:
        return self.extract_base_data().reset_index(drop=True)

    def validate_file_structure(self):
        required_tokens = {
            'חשבון מספר': False,
            'תנועות בחשבון': False,
            'תאריך': False,
            'תאריך ערך': False,
            'סוג תנועה': False,
            'זכות/חובה': False,
            'יתרה בש"ח': False,
            'אסמכתה': False,
        }

        # extract data from pdf file
        if not self.file_absolute_path.endswith('xlsx'):
            pdf_text = self.extract_text_from_pdf(self.file_absolute_path)
            for line in pdf_text.split('\n'):
                for key in required_tokens.keys():
                    if key in line:
                        required_tokens[key] = True

        return True if False not in required_tokens.values() else False

    @staticmethod
    def is_valid_date(date_string: AnyStr) -> bool:
        # Regular expression to match the date format
        pattern = r'^\d{2}/\d{2}/\d{4}$'

        # Check if the date string matches the pattern
        if re.match(pattern, date_string):
            return True
        else:
            return False

    @staticmethod
    def is_valid_description(description: AnyStr) -> bool:
        # Range of Hebrew Unicode characters
        hebrew_range = range(0x0590, 0x05FF + 1)  # Hebrew Unicode block

        # Check if any character in the string belongs to the Hebrew Unicode block
        for char in description:
            if ord(char) in hebrew_range:
                return True
        return False

    @staticmethod
    def count_description_len(line: AnyStr) -> int:
        valid_desc = 0
        for token in line.split():
            if BankMizrahiTefahotParser.is_valid_description(token):
                valid_desc += 1

        return valid_desc

    @staticmethod
    def is_valid_float(amount: AnyStr) -> bool:
        try:
            if '-' in amount:
                amount = '-' + amount.replace('-', '')

            # Set the locale to handle numbers with commas as a thousand separators
            locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')

            # Convert the string to a float using locale-aware parsing
            _ = locale.atof(amount)

            # Check if the string represents a valid float
            return True
        except ValueError:
            return False

    def extract_bank_mizrahi_tefahot_account_number(self) -> AnyStr:
        pdf_text = self.extract_text_from_pdf(self.file_absolute_path)

        for line in pdf_text.split('\n'):
            # Define the pattern
            pattern = r'\b\d{3}-\d{6}\b'

            # Use regular expression to find matches
            matches = re.findall(pattern, str(line))
            if len(matches) > 0:
                return matches[0]

        return BANK_DUMMY_ACCOUNT_NUMBER

    @staticmethod
    def extract_current_bank_debit(df: pd.DataFrame) -> Any:
        try:
            return df['current_balance'].iloc[0]
        except IndexError:
            return 0.0
        except ValueError:
            return 0.0


class HilanParser(Parser, ABC):

    def __init__(self, file_path: AnyStr):
        super().__init__(file_path)

    def parse(self) -> pd.DataFrame:
        return self.extract_base_data().reset_index(drop=True)

    @classmethod
    def is_float_or_int(cls, value):
        try:
            # Attempt to convert the text to a float
            float_value = float(value)
            # If successful, check if the float is equal to its integer representation
            if float_value == int(float_value):
                return True  # It's an integer
            else:
                return True  # It's a float
        except ValueError:
            return False  # Not a float or integer

    @classmethod
    def str_to_float(cls, value):
        if cls.is_float_or_int(value):
            return float(value)
        return 0.0

    def extract_base_data(self) -> pd.DataFrame:
        if not self.is_valid:
            self.logger.critical(f"Provided file: {self.filename} is not a valid xlsx/pdf")
            return pd.DataFrame(columns=['normal_hours_value', 'vacation_hours_value', 'completion_hours_value', 'global_hours_value', 'total_payment_value', 'holidays_hours_value', 'transport_value', 'ssn_value',
                                         'marriage_status_value', 'hmo_value', 'working_since_value', 'job_workload_value', 'marginal_tax_rate_value', 'tax_credit_points_value', 'internal_revenue_service_value',
                                         'national_insurance_institute_value', 'health_insurance_value', 'total_taxes_value', 'education_fund_value', 'pension_fund_value', 'total_payment_value'])

        extracted_data = {
            'payslip_date': {
                'month_of_payment_value': 'None',
                'year_of_payment_value': 'None',
            },
            'gross_salary':
                {
                    'normal_hours_value': 0.0,  # code 101
                    'vacation_hours_value': 0.0,  # code 105
                    'completion_hours_value': 0.0,  # code 110
                    'global_hours_value': 0.0,  # code 120
                    'total_payment_value': 0.0,  # code 2097
                    'holidays_hours_value': 0.0,  # code 106
                },
            'other_payments':
                {  # each X items
                    'transport_value': 0.0,  # code 112
                },
            'additional_information':
                {  # each X items
                    'ssn_value': 'None',
                    'marriage_status_value': 'None',
                    'hmo_value': 'None',
                    'working_since_value': 'None',
                    'job_workload_value': 'None',
                    'marginal_tax_rate_value': 'None',
                    'tax_credit_points_value': 'None',
                },
            'mandatory_taxes':
                {  # each X items
                    'internal_revenue_service_value': 0.0,
                    'national_insurance_institute_value': 0.0,
                    'health_insurance_value': 0.0,
                    'total_taxes_value': 0.0,
                },
            'savings_and_retirement_fund':
                {  # each X items
                    'education_fund_value': 0.0,  # code 302
                    'pension_fund_value': 0.0,  # code 420
                },
            'net_salary': {
                'total_net_payment_value': 0.0
            }
        }

        extracted_indexes = {
            'payslip_date': {
                'month_of_payment_idx': -1,
                'year_of_payment_idx': -2,
                'is_data_extracted': False
            },
            'gross_salary':
                {  # each 4 items
                    'total_payment_idx': 2,
                    'global_hours_idx': 3,  # code 120
                    'completion_hours_idx': 4,  # code 110
                    'vacation_hours_idx': 4,  # code 105
                    'normal_hours_idx': 4,  # code 101
                    'holidays_hours_idx': 4,  # code 106
                    'is_data_extracted': False
                },
            'other_payments':
                {  # each X items
                    'transport_idx': 4,  # code 112
                    'is_data_extracted': False
                },
            'additional_information':
                {  # each X items
                    'ssn_idx': 2,
                    'marriage_status_idx': 2,
                    'hmo_idx': 1,
                    'working_since_idx': 2,
                    'job_workload_idx': 2,
                    'marginal_tax_rate_idx': 3,
                    'tax_credit_points_idx': 2,
                    'is_data_extracted': False
                },
            'mandatory_taxes':
                {  # each X items
                    'internal_revenue_service_idx': -4,  # code 112
                    'national_insurance_institute_idx': -5,
                    'health_insurance_idx': -8,
                    'total_taxes_idx': -11,
                    'is_data_extracted': False
                },
            'savings_and_retirement_fund':
                {  # each X items
                    'education_fund_idx': [7, 9],  # code 112
                    'pension_fund_compensation_idx': 6,
                    'pension_fund_ration_idx': [7, 9],
                    'is_data_extracted': False
                },
            'net_salary': {
                'total_payment_idx': 2,
                'is_data_extracted': False
            }
        }

        hebrew_month_to_num = {
            'ינואר' :   '01/01',
            'פברואר':    '01/02',
            'מרץ':      '01/03',
            'אפריל':    '01/04',
            'מאי':      '01/05',
            'יוני':     '01/06',
            'יולי':     '01/07',
            'אוגוסט':   '01/08',
            'ספטמבר':   '01/09',
            'אוקטובר':  '01/10',
            'נובמבר':   '01/11',
            'דצמבר':    '01/12',
        }

        fixed_text = []
        ignore_chars = r'[,]'
        ignore_date = r'^\d{2}/\d{2}/\d{4}$'
        for idx, token in enumerate(self.convert_to_hebrew().split()):
            cleaned_token = re.sub(ignore_chars, '', str(token))
            if self.is_float_or_int(cleaned_token):
                fixed_text.append(cleaned_token)
            elif re.match(ignore_date, str(token)):
                fixed_text.append(cleaned_token)
            else:
                fixed_text.append(cleaned_token[::-1])
        fixed_text.reverse()

        for idx, token in enumerate(fixed_text):
            # payslip date section
            if not extracted_indexes['payslip_date']['is_data_extracted']:
                if fixed_text[idx] == 'תלוש' and fixed_text[idx + 1] == 'שכר' and fixed_text[idx + 2] == 'לחודש:':
                    current_idx = idx + extracted_indexes['payslip_date']['month_of_payment_idx']
                    extracted_data['payslip_date']['month_of_payment_value'] = hebrew_month_to_num.get(fixed_text[current_idx], INVALID_KEY)
                    current_idx = idx + extracted_indexes['payslip_date']['year_of_payment_idx']
                    extracted_data['payslip_date']['year_of_payment_value'] = fixed_text[current_idx]

            # gross salary section
            if not extracted_indexes['gross_salary']['is_data_extracted']:
                if fixed_text[idx] == '101':
                    current_idx = idx + extracted_indexes['gross_salary']['normal_hours_idx']
                    extracted_data['gross_salary']['normal_hours_value'] = self.str_to_float(fixed_text[current_idx])

                if fixed_text[idx] == '105':
                    if fixed_text[idx] == '105' and fixed_text[idx + 2] == 'הפרש':
                        current_idx = idx + extracted_indexes['gross_salary']['vacation_hours_idx'] + 1 # offset +1 for new word
                    else:
                        current_idx = idx + extracted_indexes['gross_salary']['vacation_hours_idx']
                    extracted_data['gross_salary']['vacation_hours_value'] = self.str_to_float(fixed_text[current_idx])

                if fixed_text[idx] == '106':
                    current_idx = idx + extracted_indexes['gross_salary']['holidays_hours_idx']
                    extracted_data['gross_salary']['holidays_hours_value'] = self.str_to_float(fixed_text[current_idx])

                if fixed_text[idx] == '120':
                    current_idx = idx + extracted_indexes['gross_salary']['global_hours_idx']
                    extracted_data['gross_salary']['global_hours_value'] = self.str_to_float(fixed_text[current_idx])

                if fixed_text[idx] == '110':
                    current_idx = idx + extracted_indexes['gross_salary']['completion_hours_idx']
                    extracted_data['gross_salary']['completion_hours_value'] = self.str_to_float(
                        self.str_to_float(fixed_text[current_idx]))

                if fixed_text[idx] == 'סה"כ' and fixed_text[idx + 1] == 'תשלומים' and fixed_text[idx + 2] != 'אחרים':
                    current_idx = idx + extracted_indexes['gross_salary']['total_payment_idx']
                    extracted_data['gross_salary']['total_payment_value'] = self.str_to_float(fixed_text[current_idx])

            # other payments section
            if fixed_text[idx] == '112':
                if not extracted_indexes['other_payments']['is_data_extracted']:
                    current_idx = idx + extracted_indexes['other_payments']['transport_idx']
                    extracted_data['other_payments']['transport_value'] = self.str_to_float(fixed_text[current_idx])

                    # close extraction data
                    extracted_indexes['other_payments']['is_data_extracted'] = True

            # other payments section
            if not extracted_indexes['additional_information']['is_data_extracted']:
                if fixed_text[idx] == 'מספר' and fixed_text[idx + 1] == 'זהות':
                    current_idx = idx + extracted_indexes['additional_information']['ssn_idx']
                    extracted_data['additional_information']['ssn_value'] = fixed_text[current_idx]

                if fixed_text[idx] == 'מצב' and fixed_text[idx + 1] == 'משפחתי':
                    current_idx = idx + extracted_indexes['additional_information']['marriage_status_idx']
                    extracted_data['additional_information']['marriage_status_value'] = fixed_text[current_idx]

                if fixed_text[idx] == 'קופת-חולים':
                    current_idx = idx + extracted_indexes['additional_information']['hmo_idx']
                    extracted_data['additional_information']['hmo_value'] = fixed_text[current_idx]

                if fixed_text[idx] == 'התחלת' and fixed_text[idx + 1] == 'עבודה':
                    current_idx = idx + extracted_indexes['additional_information']['working_since_idx']
                    extracted_data['additional_information']['working_since_value'] = fixed_text[current_idx]

                if fixed_text[idx] == 'אחוז' and fixed_text[idx + 1] == 'משרה':
                    current_idx = idx + extracted_indexes['additional_information']['job_workload_idx']
                    extracted_data['additional_information']['job_workload_value'] = fixed_text[current_idx].replace('%', '')[::-1]

                if fixed_text[idx] == 'אחוז' and fixed_text[idx + 1] == 'מס' and fixed_text[idx + 2] == 'שולי':
                    current_idx = idx + extracted_indexes['additional_information']['marginal_tax_rate_idx']
                    extracted_data['additional_information']['marginal_tax_rate_value'] = fixed_text[current_idx].replace('%', '')

                if fixed_text[idx] == 'נקודות' and fixed_text[idx + 1] == 'זיכוי':
                    current_idx = idx + extracted_indexes['additional_information']['tax_credit_points_idx']
                    extracted_data['additional_information']['tax_credit_points_value'] = fixed_text[current_idx]

            # mandatory taxes section
            if not extracted_indexes['mandatory_taxes']['is_data_extracted']:
                if fixed_text[idx] == 'מס' and fixed_text[idx + 1] == 'הכנסה' and fixed_text[idx + 2] == 'ביטוח':
                    current_idx = idx + extracted_indexes['mandatory_taxes']['internal_revenue_service_idx']
                    extracted_data['mandatory_taxes']['internal_revenue_service_value'] = self.str_to_float(fixed_text[current_idx])

                if fixed_text[idx] == 'ביטוח' and fixed_text[idx + 1] == 'לאומי' and fixed_text[idx + 2] == 'הפרשי':
                    current_idx = idx + extracted_indexes['mandatory_taxes']['national_insurance_institute_idx']
                    extracted_data['mandatory_taxes']['national_insurance_institute_value'] = self.str_to_float(fixed_text[current_idx])

                if fixed_text[idx] == 'ביטוח' and fixed_text[idx + 1] == 'בריאות' and fixed_text[idx + 2] == 'הפרשי':
                    current_idx = idx + extracted_indexes['mandatory_taxes']['health_insurance_idx']
                    extracted_data['mandatory_taxes']['health_insurance_value'] = self.str_to_float(fixed_text[current_idx])

                if fixed_text[idx] == 'סה"כ' and fixed_text[idx + 1] == 'נכויי' and fixed_text[idx + 2] == 'חובה':
                    current_idx = idx + extracted_indexes['mandatory_taxes']['total_taxes_idx']
                    extracted_data['mandatory_taxes']['total_taxes_value'] = self.str_to_float(fixed_text[current_idx])

            # pension and education funds
            if not extracted_indexes['savings_and_retirement_fund']['is_data_extracted']:
                if fixed_text[idx] == '302':
                    current_idx_1 = idx + extracted_indexes['savings_and_retirement_fund']['education_fund_idx'][0]
                    current_idx_2 = idx + extracted_indexes['savings_and_retirement_fund']['education_fund_idx'][1]
                    value_1 = self.str_to_float(fixed_text[current_idx_1])
                    value_2 = self.str_to_float(fixed_text[current_idx_2])
                    extracted_data['savings_and_retirement_fund']['education_fund_value'] = value_1 + value_2

                if fixed_text[idx] == '420' and fixed_text[idx + 3] == 'קצבה':
                    current_idx_1 = idx + extracted_indexes['savings_and_retirement_fund']['pension_fund_ration_idx'][0]
                    current_idx_2 = idx + extracted_indexes['savings_and_retirement_fund']['pension_fund_ration_idx'][1]
                    value_1 = self.str_to_float(fixed_text[current_idx_1])
                    value_2 = self.str_to_float(fixed_text[current_idx_2])
                    extracted_data['savings_and_retirement_fund']['pension_fund_value'] += value_1 + value_2

                if fixed_text[idx] == '420' and fixed_text[idx + 3] == 'פיצויים':
                    current_idx = idx + extracted_indexes['savings_and_retirement_fund']['pension_fund_compensation_idx']
                    value_idx = self.str_to_float(fixed_text[current_idx])
                    extracted_data['savings_and_retirement_fund']['pension_fund_value'] += value_idx

            # net salary funds
            if not extracted_indexes['net_salary']['is_data_extracted']:
                if fixed_text[idx] == 'שכר' and fixed_text[idx + 1] == 'נטו':
                    current_idx = idx + extracted_indexes['net_salary']['total_payment_idx']
                    extracted_data['net_salary']['total_net_payment_value'] = self.str_to_float(fixed_text[current_idx])

        dict_to_df = pd.DataFrame(columns=['payslip_date', 'normal_hours_value', 'vacation_hours_value', 'completion_hours_value', 'global_hours_value', 'total_payment_value', 'holidays_hours_value', 'transport_value', 'ssn_value',
                                         'marriage_status_value', 'hmo_value', 'working_since_value', 'job_workload_value', 'marginal_tax_rate_value', 'tax_credit_points_value', 'internal_revenue_service_value',
                                         'national_insurance_institute_value', 'health_insurance_value', 'total_taxes_value', 'education_fund_value', 'pension_fund_value', 'total_net_payment_value'])
        df_row = {
            'payslip_date': extracted_data['payslip_date']['month_of_payment_value'] + '/' + extracted_data['payslip_date']['year_of_payment_value'],
            'normal_hours_value': extracted_data['gross_salary']['normal_hours_value'],
            'vacation_hours_value': extracted_data['gross_salary']['vacation_hours_value'],
            'holidays_hours_value': extracted_data['gross_salary']['holidays_hours_value'],
            'completion_hours_value': extracted_data['gross_salary']['completion_hours_value'],
            'global_hours_value': extracted_data['gross_salary']['global_hours_value'],
            'total_payment_value': extracted_data['gross_salary']['total_payment_value'],
            'transport_value': extracted_data['other_payments']['transport_value'],
            'ssn_value': extracted_data['additional_information']['ssn_value'],
            'marriage_status_value': extracted_data['additional_information']['marriage_status_value'],
            'hmo_value': extracted_data['additional_information']['hmo_value'],
            'working_since_value': extracted_data['additional_information']['working_since_value'],
            'job_workload_value': extracted_data['additional_information']['job_workload_value'],
            'marginal_tax_rate_value': extracted_data['additional_information']['marginal_tax_rate_value'],
            'tax_credit_points_value': extracted_data['additional_information']['tax_credit_points_value'],
            'internal_revenue_service_value': extracted_data['mandatory_taxes']['internal_revenue_service_value'],
            'national_insurance_institute_value': extracted_data['mandatory_taxes']['national_insurance_institute_value'],
            'health_insurance_value': extracted_data['mandatory_taxes']['health_insurance_value'],
            'total_taxes_value': extracted_data['mandatory_taxes']['total_taxes_value'],
            'education_fund_value': extracted_data['savings_and_retirement_fund']['education_fund_value'],
            'pension_fund_value': extracted_data['savings_and_retirement_fund']['pension_fund_value'],
            'total_net_payment_value': extracted_data['net_salary']['total_net_payment_value'],
            }

        dict_to_df.loc[len(dict_to_df)] = pd.Series(df_row)
        return dict_to_df

    def validate_file_structure(self):
        fixed_text = []
        ignore_chars = r'[,]'
        ignore_date = r'^\d{2}/\d{2}/\d{4}$'
        for idx, token in enumerate(self.convert_to_hebrew().split()):
            cleaned_token = re.sub(ignore_chars, '', str(token))
            if self.is_float_or_int(cleaned_token):
                fixed_text.append(cleaned_token)
            elif re.match(ignore_date, str(token)):
                fixed_text.append(cleaned_token)
            else:
                fixed_text.append(cleaned_token[::-1])
        fixed_text.reverse()

        validators_tokens = {
            'פרוט': False,
            'התשלומים': False,
            'ניכויי': False,
            'חובה': False,
            'מסים': False,
            'התחייבות': False,
            'ריכוז': False,
            'נתונים': False,
            'בתלוש': False,
            'שכר': False,
        }

        for idx, token in enumerate(fixed_text):
            if token in validators_tokens.keys():
                validators_tokens[token] = True

        if False in validators_tokens.values():
            return False
        return True

    def convert_to_hebrew(self):
        ansi_table = {
            'à': 'א',
            'á': 'ב',
            'â': 'ג',
            'ã': 'ד',
            'ä': 'ה',
            'å': 'ו',
            'æ': 'ז',
            'ç': 'ח',
            'è': 'ט',
            'é': 'י',
            'ë': 'כ',
            'ì': 'ל',
            'î': 'מ',
            'ð': 'נ',
            'ñ': 'ס',
            'ò': 'ע',
            'ô': 'פ',
            'ö': 'צ',
            '÷': 'ק',
            'ø': 'ר',
            'ù': 'ש',
            'ú': 'ת',
            'õ': 'ץ',
            'ê': 'ך',
            'ï': 'ן',
            'í': 'ם',
            'ó': 'ף',
        }

        pdf_text = self.extract_text_from_pdf(self.file_absolute_path)
        for idx, char in enumerate(pdf_text):
            if 0 <= idx < len(pdf_text):
                pdf_text = pdf_text[:idx] + ansi_table.get(char, char) + pdf_text[idx + 1:]
            else:
                Logger.critical("Convert text into hebrew encountered an error.")
        return pdf_text
