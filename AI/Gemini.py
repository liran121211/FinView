import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Text
from AI import Logger, BusinessesCategoriesINIParser
import google.generativeai as genai

class GeminiModel():

    def __init__(self, model_type: Text = 'gemini-pro'):
        self.__model = genai.GenerativeModel(model_type)
        self.__ini_parser = BusinessesCategoriesINIParser
        genai.configure(api_key='AIzaSyAK4fNcGCPf1aPC0R8oXDY20QoX_WO4HJ8')

    def find_business_category(self, business_name: Text) -> Text:
        define_role = f"""You are a Business Explorer,
        who knows which category the business I will ask you about belongs to. The categories: {self.__ini_parser.get_str_values('Transactions Categories')}.
        Can you tell me what category the business: {business_name}?
        Please respond with the name of the category only in Hebrew without revealing the name of the business."""

        result = self.__ini_parser.get_predefined_business_category(business_name)
        if result is not None:
            return result
        else:
            try:
                response = self.__model.generate_content(define_role)
            except ValueError:
                response = ' '.join([keyword.text.strip() for keyword in self.__model.generate_content(define_role).parts])
            result = self.__ini_parser.get_main_category(ini_header='Transactions Categories', input_category=response)
            self.__ini_parser.add_new_business_category(business_name=business_name, category=result)

    def find_bank_transaction_category(self, transaction_desc: Text) -> Text:
        define_role = f"""You are a Bank Analyst,
        who knows which category the transaction I will ask you about belongs to. The categories: {self.__ini_parser.get_str_values('Transactions Categories')}.
        Can you tell me what category the transaction: {transaction_desc}?
        Please respond with the name of the category only in Hebrew without revealing the name of the business."""

        result = self.__ini_parser.get_predefined_business_category(business_name=transaction_desc)
        if result is not None:
            return result
        else:
            try:
                response = self.__model.generate_content(define_role).text.strip()
            except ValueError:
                response = ' '.join([keyword.text.strip() for keyword in self.__model.generate_content(define_role).parts])
            result = self.__ini_parser.get_main_category(ini_header='Transactions Categories', input_category=response)
            self.__ini_parser.add_new_business_category(business_name=transaction_desc, category=result)


x = GeminiModel()
print(x.find_business_category('מאסטר-קארד'))
