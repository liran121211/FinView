import g4f
import requests
from typing import Text, Any
from bs4 import BeautifulSoup


def google_query_description(query: Text) -> Any:
    try:
        # Perform Google search
        url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the description of the first search result
        description = soup.find('div', class_='BNeawe s3v9rd AP7Wnd').text

        return description

    except Exception as e:
        print("An error occurred:", e)
        return None


def send_chatgpt_4_prompt(query: Text) -> Any:
    messages = [{"role": "system", "content": query}, ]

    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=messages,
    )

    return response
