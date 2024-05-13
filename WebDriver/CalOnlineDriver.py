from typing import Text

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from DataParser import UNDETERMINED_PAYMENT_TYPE
from WebDriver import MAX_WAITING_TIME, LAST_4_DIGITS_IDX, CARD_TYPE_IDX, LOGIN_BUTTON_IDX, FIRST_ELEMENT_IDX, \
    SECOND_ELEMENT_IDX

class CalOnlineDriver:
    def __init__(self, web_username: Text, web_password: Text, web_driver: Text = 'Chrome'):
        self.__username = web_username
        self.__password = web_password
        self.__login_url = 'https://www.cal-online.co.il/'
        self.__dashboard_url = 'https://digital-web.cal-online.co.il/dashboard'
        self.__flow_url_1 = 'https://digital-web.cal-online.co.il/site-tutorial'
        self.__transactions_url = 'https://digital-web.cal-online.co.il/transactions-search'
        self.transactions_data = pd.DataFrame(columns=['date_of_transaction', 'business_name', 'charge_amount', 'transaction_type', 'total_amount', 'last_4_digits', 'transaction_provider', ])

        if web_driver == 'Chrome':
            self.driver_name = web_driver
            self.__driver = webdriver.Chrome(options=self.set_browser_options())

    def set_browser_options(self):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

        if self.driver_name == 'Chrome':
            chrome_options = Options()
            # chrome_options.add_argument("--headless")
            chrome_options.add_argument(f"user-agent={user_agent}")
            return chrome_options

        return None

    def retrieve_data(self) -> pd.DataFrame:
        # Open a webpage
        self.__driver.get(self.__login_url)

        # Wait for up to 2 seconds
        self.__driver.implicitly_wait(2)

        # Find the login button and click it
        self.__driver.find_element(By.ID, 'ccLoginDesktopBtn').click()

        # set focus on login iframe window
        login_iframe = self.__driver.find_element(By.TAG_NAME, 'iframe')
        self.__driver.switch_to.frame(login_iframe)

        # set login method to username & password
        self.__driver.find_element(By.CLASS_NAME, 'mat-tab-links').find_elements(By.XPATH, "./a")[1].click()

        # fill username & password textbox with login credentials
        form_input_id = self.__driver.find_elements(By.TAG_NAME, 'input')[FIRST_ELEMENT_IDX]
        form_input_id.send_keys(self.__username)

        form_input_password = self.__driver.find_elements(By.TAG_NAME, 'input')[SECOND_ELEMENT_IDX]
        form_input_password.send_keys(self.__password)

        # submit form
        self.__driver.find_elements(By.TAG_NAME, 'button')[LOGIN_BUTTON_IDX].click()

        # continue to navigate between pages until transaction url reached.
        WebDriverWait(self.__driver, MAX_WAITING_TIME).until(expected_conditions.url_to_be(self.__flow_url_1))
        self.__driver.get(self.__dashboard_url)

        WebDriverWait(self.__driver, MAX_WAITING_TIME).until(expected_conditions.url_to_be(self.__dashboard_url))
        self.__driver.get(self.__transactions_url)

        WebDriverWait(self.__driver, MAX_WAITING_TIME).until(expected_conditions.url_to_be(self.__transactions_url))

        # get transactions list
        self.__driver.find_element(By.CLASS_NAME, 'container').find_elements(By.TAG_NAME, 'li')[FIRST_ELEMENT_IDX].click()
        self.__driver.find_element(By.CLASS_NAME, 'buttons-area').find_elements(By.TAG_NAME, 'button')[SECOND_ELEMENT_IDX].click()

        # wait until all transactions rows are loaded.
        WebDriverWait(self.__driver, MAX_WAITING_TIME).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'search-results')))

        # extract transactions rows data
        for idx, element in enumerate(self.__driver.find_elements(By.TAG_NAME, 'li')):
            data = {
                    'date_of_transaction': pd.to_datetime(element.find_element(By.CLASS_NAME, 'trnDate').text, dayfirst=True),
                    'business_name': element.find_element(By.CLASS_NAME, 'merchantName').text,
                    'charge_amount': element.find_element(By.CLASS_NAME, 'price').text.replace('₪',''),
                    'transaction_type': UNDETERMINED_PAYMENT_TYPE,
                    'total_amount': element.find_element(By.CLASS_NAME, 'price').text.replace('₪',''),
                    'last_4_digits': element.find_element(By.CLASS_NAME, 'details').text.split()[LAST_4_DIGITS_IDX],
                    'transaction_provider': 'Cal-Online',
                }
            self.transactions_data.loc[idx] = pd.Series(data)

        # finish driver process
        self.__driver.quit()

        return self.transactions_data
