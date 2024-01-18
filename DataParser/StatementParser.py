import os
import os.path
from typing import AnyStr, Any
import pandas as pd
import requests
from abc import ABC, abstractmethod
from DataParser import PROJECT_ROOT


class Parser:
    def __init__(self, file_path: AnyStr):
        self.__file_absolute_path = os.path.join(PROJECT_ROOT, file_path)
        self.__df = pd.read_excel(self.__file_absolute_path, engine='openpyxl')

    @staticmethod
    def is_string_in_hebrew(value):
        try:
            hebrew_chars = set(range(0x0590, 0x05FF + 1))
            contains_hebrew = any(ord(char) in hebrew_chars for char in value)

            if contains_hebrew:
                return value[::-1]
            else:
                return value

        except TypeError:
            return value

    @staticmethod
    def get_business_category(business_name):
        base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        api_key = "AIzaSyAxcSgbrcJL7ucJ8bTfagIf27952bhj0xM"
        params = {
            "key": api_key,
            "input": business_name,
            "inputtype": "textquery",
            "fields": "name,types"
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if data.get("candidates"):
            first_candidate = data["candidates"][0]
            # business_name = first_candidate.get("name", "Unknown Business")
            business_types = first_candidate.get("types", [])

            if business_types:
                return business_types
            else:
                return []

        return []

    @abstractmethod
    def parse(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def extract_base_data(self) -> pd.DataFrame:
        pass

    def define_missing_category(self, temp_df):
        categories = {'1': 'ציוד לבית ולמשרד',
                      '2': 'אוכל',
                      '3': 'פנאי ובידור',
                      '4': 'עמלות',
                      '5': 'קוסמטיקה ופארם',
                      '6': 'ביגוד',
                      '7': 'שירותי תקשורת',
                      '8': 'ממשלה ועירייה',
                      '9': 'שונות',
                      }

        temp_df['category'] = pd.Series()

        for idx, row in temp_df.iterrows():
            print(f"Business Category: {row['business_name']}")
            print(
                "1.Home Equipment | 2. Food | 3.Entertainment | 4. Fees | 5.Cosmetic and Pharmacy | 6.Clothes | 7. Communication | 8. Goverment and Municipality | 9. Misc")

            answer = categories[input(str("Answer (1-9): "))]
            temp_df.loc[idx:idx, ['category']] = self.is_string_in_hebrew(answer)
            os.system('cls' if os.name == 'nt' else 'clear')

        output_path = os.path.basename(self.__file_absolute_path)[:-5]
        output_path = output_path + '_parsed.xlsx'
        temp_df.to_excel(os.path.join(PROJECT_ROOT, fr'files\Output\{output_path}'))

        return temp_df

    @property
    def data(self):
        return self.__df


class LeumiParser(Parser, ABC):
    def __init__(self, file_path: AnyStr):
        super().__init__(file_path)

    def retrieve_first_index(self) -> Any:
        # Check if the required columns exist in the DataFrame
        required_columns = {'תאריך העסקה', 'שם בית העסק', 'סכום חיוב'}

        for idx, values in self.data.iterrows():
            col_values = set(v[1] for v in values.items())
            if len(required_columns & col_values) > 0:
                return int(str(idx)) + 1

        raise IndexError("Could not find first row of data.")

    def retrieve_last_index(self, start_idx) -> Any:
        date_of_purchase, business_name, total_amount = 0, 1, 5
        for idx, values in self.data.iloc[start_idx:].iterrows():
            if pd.isna(values[date_of_purchase]) or pd.isna(values[business_name]) or pd.isna(values[total_amount]):
                return idx

        raise IndexError("Could not find last row of data.")

    def extract_base_data(self) -> pd.DataFrame:
        temp_df = pd.DataFrame(
            columns=['date_of_purchase', 'business_name', 'charge_amount', 'total_amount', 'payment_type'])
        date_of_purchase_idx, business_name_idx, charge_amount_idx, payment_type_idx, total_amount_idx = 0, 1, 2, 3, 5
        first_idx = self.retrieve_first_index()
        last_idx = self.retrieve_last_index(first_idx)
        current_df = self.data.iloc[first_idx: last_idx]

        for idx, column in current_df.iterrows():
            try:
                if pd.to_datetime(column.iloc[date_of_purchase_idx], dayfirst=True):
                    if pd.isna(column.iloc[date_of_purchase_idx]) or pd.isnull(column.iloc[date_of_purchase_idx]):
                        continue

                if pd.isna(column.iloc[business_name_idx]) or pd.isnull(column.iloc[business_name_idx]):
                    continue

                if pd.isna(column.iloc[charge_amount_idx]) or pd.isnull(column.iloc[charge_amount_idx]):
                    continue

                if pd.isna(column.iloc[payment_type_idx]) or pd.isnull(column.iloc[payment_type_idx]):
                    continue

                if pd.isna(column.iloc[total_amount_idx]) or pd.isnull(column.iloc[total_amount_idx]):
                    continue

                data = {
                    'date_of_purchase': pd.to_datetime(column.iloc[date_of_purchase_idx], dayfirst=True),
                    'business_name': column.iloc[business_name_idx],
                    'charge_amount': column.iloc[charge_amount_idx],
                    'payment_type': column.iloc[payment_type_idx],
                    'total_amount': column.iloc[total_amount_idx],
                }
                temp_df.loc[len(temp_df)] = pd.Series(data)

            except ValueError:
                continue

        return temp_df.iloc[first_idx: last_idx]

    def parse(self) -> pd.DataFrame:
        base_df = self.extract_base_data().reset_index(drop=True)
        return self.define_missing_category(temp_df=base_df)


class CalOnlineParser(Parser, ABC):
    def __init__(self, file_path: AnyStr):
        super().__init__(file_path)

    def extract_base_data(self) -> pd.DataFrame:
        # Check if the required columns exist in the DataFrame
        info_rows = pd.DataFrame(
            columns=['date_of_purchase', 'business_name', 'charge_amount', 'total_amount', 'payment_type'])
        date_of_purchase_idx, business_name_idx, charge_amount_idx, payment_type_idx, total_amount_idx = 0, 1, 3, 4, 2

        for idx, column in self.data.iterrows():
            try:
                if pd.to_datetime(column.iloc[date_of_purchase_idx], dayfirst=True):
                    if pd.isna(column.iloc[date_of_purchase_idx]) or pd.isnull(column.iloc[date_of_purchase_idx]):
                        continue

                if pd.isna(column.iloc[business_name_idx]) or pd.isnull(column.iloc[business_name_idx]):
                    continue

                if pd.isna(column.iloc[charge_amount_idx]) or pd.isnull(column.iloc[charge_amount_idx]):
                    continue

                if pd.isna(column.iloc[payment_type_idx]) or pd.isnull(column.iloc[payment_type_idx]):
                    continue

                if pd.isna(column.iloc[total_amount_idx]) or pd.isnull(column.iloc[total_amount_idx]):
                    continue

                data = {
                    'date_of_purchase': pd.to_datetime(column.iloc[date_of_purchase_idx], dayfirst=True),
                    'business_name': column.iloc[business_name_idx],
                    'charge_amount': column.iloc[charge_amount_idx],
                    'payment_type': column.iloc[payment_type_idx],
                    'total_amount': column.iloc[total_amount_idx],
                }
                info_rows.loc[len(info_rows)] = pd.Series(data)

            except ValueError:
                continue

        return info_rows

    def parse(self) -> pd.DataFrame:
        base_df = self.extract_base_data().reset_index(drop=True)
        return self.define_missing_category(temp_df=base_df)


class MaxParser(Parser, ABC):
    def __init__(self, file_path: AnyStr):
        super().__init__(file_path)

    def extract_base_data(self) -> pd.DataFrame:
        # Check if the required columns exist in the DataFrame
        info_rows = pd.DataFrame(
            columns=['date_of_purchase', 'business_name', 'charge_amount', 'total_amount', 'payment_type'])
        date_of_purchase_idx, business_name_idx, charge_amount_idx, payment_type_idx, total_amount_idx = 0, 1, 5, 10, 7

        for idx, column in self.data.iterrows():
            try:
                if pd.to_datetime(column.iloc[date_of_purchase_idx], dayfirst=True):
                    if pd.isna(column.iloc[date_of_purchase_idx]) or pd.isnull(column.iloc[date_of_purchase_idx]):
                        continue

                if pd.isna(column.iloc[business_name_idx]) or pd.isnull(column.iloc[business_name_idx]):
                    continue

                if pd.isna(column.iloc[charge_amount_idx]) or pd.isnull(column.iloc[charge_amount_idx]):
                    continue

                if pd.isna(column.iloc[payment_type_idx]) or pd.isnull(column.iloc[payment_type_idx]):
                    continue

                if pd.isna(column.iloc[total_amount_idx]) or pd.isnull(column.iloc[total_amount_idx]):
                    continue

                data = {
                    'date_of_purchase': pd.to_datetime(column.iloc[date_of_purchase_idx], dayfirst=True),
                    'business_name': column.iloc[business_name_idx],
                    'charge_amount': column.iloc[charge_amount_idx],
                    'payment_type': column.iloc[payment_type_idx],
                    'total_amount': column.iloc[total_amount_idx],
                }
                info_rows.loc[len(info_rows)] = pd.Series(data)

            except ValueError:
                continue

        return info_rows

    def parse(self) -> pd.DataFrame:
        base_df = self.extract_base_data().reset_index(drop=True)
        return self.define_missing_category(temp_df=base_df)
