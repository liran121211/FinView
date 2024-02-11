from typing import Text
from AI import BUSINESS_CATEGORIES
import google.generativeai as genai


class GeminiModel():

    def __init__(self, model_type: Text = 'gemini-pro'):
        self.model = genai.GenerativeModel(model_type)
        genai.configure(api_key='AIzaSyAK4fNcGCPf1aPC0R8oXDY20QoX_WO4HJ8')

    def find_business_category(self, business_name: Text) -> Text:
        define_role = f"""You are a Business Explorer,
        who knows which category the business I will ask you about belongs to. The categories: {BUSINESS_CATEGORIES}.
        Can you tell me what category the business: {business_name}?
        Please respond with the name of the category only in Hebrew without revealing the name of the business."""

        try:
            response = self.model.generate_content(define_role).text.strip()
        except ValueError:
            response = ' '.join([keyword.text.strip() for keyword in self.model.generate_content(define_role).parts])

        print(response)
        return response