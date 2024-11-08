from typing import Text
from AI import CREDIT_CARD_TRANSACTIONS_CATEGORIES, BANK_TRANSACTIONS_CATEGORIES, Logger
import google.generativeai as genai


class GeminiModel():

    def __init__(self, model_type: Text = 'gemini-pro'):
        self.model = genai.GenerativeModel(model_type)
        genai.configure(api_key=HIDDEN')

    def find_business_category(self, business_name: Text) -> Text:
        define_role = f"""You are a Business Explorer,
        who knows which category the business I will ask you about belongs to. The categories: {CREDIT_CARD_TRANSACTIONS_CATEGORIES}.
        Can you tell me what category the business: {business_name}?
        Please respond with the name of the category only in Hebrew without revealing the name of the business."""

        try:
            response = self.model.generate_content(define_role).text.strip()
        except ValueError:
            response = ' '.join([keyword.text.strip() for keyword in self.model.generate_content(define_role).parts])

        for i, category in CREDIT_CARD_TRANSACTIONS_CATEGORIES.items():
            if response in category:
                return category

        return 'קטגוריה לא ידועה'

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

        for i, category in BANK_TRANSACTIONS_CATEGORIES.items():
            if response in category:
                return category

        return 'קטגוריה לא ידועה'

