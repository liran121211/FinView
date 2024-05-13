from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

extracted_data = {
    'pension_current_value': 0.0,
    'education_fund_current_value': 0.0,
}

# Define login credentials and target URL
login_url = 'https://www.migdal.co.il/mymigdal/process/login'
username = '311370092'
password = '@jx8xcSTA!'

# Set the user agent string
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

# Set Chrome options to run in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument(f"user-agent={user_agent}")

# Initialize Chrome browser
driver = webdriver.Chrome(options=chrome_options)

# Open a webpage
driver.get(login_url)
driver.get_screenshot_as_file("screenshot.png")

# Find an element by its ID and type some text
driver.find_element(By.CLASS_NAME, 'enter_link').click()

form_input_id = driver.find_element(By.CLASS_NAME, 'user_input').find_element(By.CLASS_NAME, 'input')
form_input_id.send_keys(username)

form_input_password = driver.find_element(By.CLASS_NAME, 'user_password').find_element(By.CLASS_NAME, 'input')
form_input_password.send_keys(password)

# submit form
driver.find_element(By.CLASS_NAME, 'button').click()

# data page
pension_div = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, "Pensioncube")))
education_fund_div = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, "Hishtalmutcube")))

extracted_data['pension_current_value'] = pension_div.find_element(By.CLASS_NAME, 'value').text
extracted_data['education_fund_current_value'] = education_fund_div.find_element(By.CLASS_NAME, 'value').text

# Close the browser
driver.quit()

print(f" סכום פנסיה נוכחי:{extracted_data['pension_current_value']}")
print(f" סכום קרן השתלמות נוכחי:{extracted_data['education_fund_current_value']}")