import configparser
import os
from abc import abstractmethod
from typing import Text
from INIParser import Logger, INVALID_CONFIG_FILE


class INIFileHandler:
    def __init__(self, file_name):
        self.file_name = file_name
        self.handler = None
        self.file_path = self.find_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

    def find_file(self, directory):
        for root, dirs, files in os.walk(directory):
            if self.file_name in files:
                return os.path.join(root, self.file_name)
        Logger.critical(f"Cannot find config INI file: {self.file_name} in project files")
        exit(INVALID_CONFIG_FILE)

    def read_ini(self):
        try:
            config = configparser.ConfigParser()
            config.read(self.file_path, encoding='utf-8')
            self.handler = config
        except FileNotFoundError:
            Logger.critical(f"FileNotFoundError - INI file '{self.file_path}' not found.")
            return None
        except configparser.ParsingError as e:
            Logger.critical(f"Error parsing INI file '{self.file_path}': {e}")
            return None

    def write_ini(self):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as configfile:
                self.handler.write(configfile)
        except FileNotFoundError:
            Logger.critical(f"INI file '{self.file_path}' not found.")
            return None
        except IOError as e:
            Logger.critical(f"Error writing to INI file '{self.file_path}': {e}")
            return None

    def get_headers(self):
        if self.handler is None:
            return list()

        if getattr(self.handler, 'sections'):
            return self.handler.sections()
        return list()

    @abstractmethod
    def get_values(self, ini_header: Text):
        pass

    @abstractmethod
    def get_str_values(self, ini_header: Text):
        pass


class BusinessesCategoriesINI(INIFileHandler):
    def __init__(self, file_name):
        super().__init__(file_name)

    def get_values(self, ini_header: Text):
        result = dict()
        if self.handler is None:
            return result

        if getattr(self.handler, 'sections'):
            try:
                for category, sub_categories in self.handler[ini_header].items():
                    result[category] = [sub_category.strip() for sub_category in sub_categories.split(',')]
            except KeyError:
                Logger.critical(f"Error reading from INI file, ini_header: '{ini_header}' not found.")
                return result

            return result
        return result

    def get_str_values(self, ini_header: Text):
        result = ""
        for idx, (category, sub_categories) in enumerate(self.get_values(ini_header).items()):
            result += f"{idx}.{category}: {str(sub_categories)}\n"
        return result

    def get_main_category(self, ini_header: Text, input_category: Text):
        all_categories = self.get_values(ini_header=ini_header)
        for ini_main_category, ini_sub_categories in all_categories.items():
            if input_category == ini_main_category:
                return ini_main_category
            if input_category in ini_sub_categories:
                return ini_main_category

        return 'לא מקוטלג'

    def is_business_exist(self, input_business: Text):
        all_businesses = self.get_values(ini_header='Predefined Businesses')
        input_business = input_business.lower()
        for ini_business, _ in all_businesses.items():
            if input_business in ini_business:
                return True
        return False

    def get_predefined_business_category(self, business_name: Text):
        if self.is_business_exist(business_name):
            try:
                return self.get_values(ini_header='Predefined Businesses')[business_name][0]
            except KeyError:
                Logger.critical(f"Error reading from INI file, predefined business name: '{business_name}' not found.")
                return None
            except IndexError:
                Logger.critical(f"Error reading from INI file, predefined business name: '{business_name}' has no category.")
                return None
        return None

    def add_new_business_category(self, business_name: Text, category: Text):
        self.handler["Predefined Businesses"] = {business_name: category}
        self.write_ini()