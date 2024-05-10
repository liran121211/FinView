from typing import Text
from AI import CREDIT_CARD_TRANSACTIONS_CATEGORIES, BANK_TRANSACTIONS_CATEGORIES, Logger, BusinessesCategoriesINIParser
import google.generativeai as genai

class GeminiModel():

    def __init__(self, model_type: Text = 'gemini-pro'):
        self.model = genai.GenerativeModel(model_type)
        self.ini_parser = BusinessesCategoriesINIParser
        genai.configure(api_key='AIzaSyAK4fNcGCPf1aPC0R8oXDY20QoX_WO4HJ8')

    def find_business_category(self, business_name: Text) -> Text:
        define_role = f"""You are a Business Explorer,
        who knows which category the business I will ask you about belongs to. The categories: {self.ini_parser.get_str_values('Transactions Categories')}.
        Can you tell me what category the business: {business_name}?
        Please respond with the name of the category only in Hebrew without revealing the name of the business."""

        try:
            response = self.model.generate_content(define_role).text.strip()
        except ValueError:
            response = ' '.join([keyword.text.strip() for keyword in self.model.generate_content(define_role).parts])

        return self.ini_parser.get_main_category(ini_header='Transactions Categories', input_category=response)

    def find_bank_transaction_category(self, description: Text) -> Text:
        define_role = f"""You are a Bank Analyst,
        who knows which category the transaction I will ask you about belongs to. The categories: {BANK_TRANSACTIONS_CATEGORIES}.
        Can you tell me what category the transaction: {description}?
        Please respond with the name of the category only in Hebrew without revealing the name of the business."""

        try:
            response = self.model.generate_content(define_role).text.strip()
            Logger.critical(response)
        except ValueError:
            response = ' '.join([keyword.text.strip() for keyword in self.model.generate_content(define_role).parts])

        return self.ini_parser.get_main_category(ini_header='Transactions Categories', input_category=response)


x = GeminiModel()
print(x.find_business_category('MOR&MOR'))
