import pandas as pd
import datetime
import os.path
import re
from abc import ABC, abstractmethod
from typing import AnyStr, Any
from openpyxl.reader.excel import load_workbook
from openpyxl.utils.exceptions import InvalidFileException
from DataParser import *


class Parser:
    def __init__(self, file_path: AnyStr):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(FILE_HANDLER)
        self.filename = os.path.basename(file_path)
        self.__file_absolute_path = os.path.join(PROJECT_ROOT, file_path)

        # validate xlsx file before init instance
        if self.is_xlsx_file(self.__file_absolute_path):
            self.__df = pd.read_excel(self.__file_absolute_path, engine='openpyxl')
            self.is_valid = True
        else:
            self.is_valid = False

    @staticmethod
    def is_xlsx_file(file_path: AnyStr) -> bool:
        try:
            # Try to load the file with openpyxl
            load_workbook(file_path)
            return True
        except InvalidFileException:
            return False

    @abstractmethod
    def parse(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def extract_base_data(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def extract_transaction_type(self, transaction_type: AnyStr) -> AnyStr:
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
            self.logger.critical(f"Provided file: {self.filename} is not a valid xlsx.")
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


class CalOnlineParser(Parser, ABC):
    def __init__(self, file_path: AnyStr):
        super().__init__(file_path)

    def extract_base_data(self) -> pd.DataFrame:
        if not self.is_valid:
            self.logger.critical(f"Provided file: {self.filename} is not a valid xlsx.")
            return pd.DataFrame(columns=['date_of_transaction', 'business_name', 'charge_amount', 'total_amount', 'transaction_type', 'transaction_provider', 'last_4_digits', 'card_type' 'category'])

        # Check if the required columns exist in the DataFrame
        info_rows = pd.DataFrame(columns=['date_of_transaction', 'business_name', 'charge_amount', 'total_amount', 'transaction_type', 'transaction_provider', 'last_4_digits', 'card_type', 'category'])
        date_of_transaction_idx, business_name_idx, charge_amount_idx, transaction_type_idx, total_amount_idx = 0, 1, 3, 4, 2

        # extract last 4 card digits from file
        if len(self.data.keys()) > 0:
            last_4_digits = re.findall(r'\b\d{4}\b', self.data.keys()[0])
            card_type = 'Visa' if 'ויזה' in self.data.keys()[0] else 'MasterCard' if 'מאסטרקארד' in self.data.keys()[0] else 'Unknown'

            if len(last_4_digits) > 0:
                last_4_digits = last_4_digits[0]
        else:
            last_4_digits = CREDIT_CARD_DUMMY_LAST_4_DIGITS
            card_type = 'Unknown'

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


class MaxParser(Parser, ABC):
    def __init__(self, file_path: AnyStr):
        super().__init__(file_path)

    def extract_base_data(self) -> pd.DataFrame:
        if not self.is_valid:
            self.logger.critical(f"Provided file: {self.filename} is not a valid xlsx.")
            return pd.DataFrame(columns=['date_of_transaction', 'business_name', 'charge_amount', 'total_amount', 'transaction_type', 'transaction_provider', 'last_4_digits', 'card_type', 'category'])

        # Check if the required columns exist in the DataFrame
        info_rows = pd.DataFrame(columns=['date_of_transaction', 'business_name', 'charge_amount', 'total_amount', 'transaction_type', 'transaction_provider', 'last_4_digits','card_type', 'category'])
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


class BankLeumiParser(Parser, ABC):
    def __init__(self, file_path: AnyStr):
        super().__init__(file_path)

    def extract_base_data(self) -> pd.DataFrame:
        if not self.is_valid:
            self.logger.critical(f"Provided file: {self.filename} is not a valid xlsx.")
            return pd.DataFrame(columns=['transaction_date', 'transaction_description', 'transaction_reference', 'income_balance', 'outcome_balance', 'current_balance', 'account_number', 'transaction_provider', 'transaction_category'])

        # Check if the required columns exist in the DataFrame
        info_rows = pd.DataFrame(columns=['transaction_date', 'transaction_description', 'transaction_reference','income_balance', 'outcome_balance', 'current_balance', 'account_number', 'transaction_provider', 'transaction_category'])
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
