from . import constant as const
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.wait import WebDriverWait


# # ChromeDriverManager().install()


# class PARENT(webdriver.Edge):

#     def __init__(self):
#         super(PARENT, self).__init__()
#         self.maximize_window()
#         self.wait = WebDriverWait(self, timeout=15, poll_frequency=1)

#     def landFirstPage(self):
#         self.get(r'https://colab.research.google.com/')

#     def click_file(self):
#         self.find_element(
#             By.XPATH, '//*[@id="file-menu-button"]/div/div/div[contains(text(), "File")]').click()


#     def close_popup(self):
#         try:
            
#             # Wait for the popup to be visible
#             self.wait.until(EC.visibility_of_element_located(
#                 (By.XPATH, "//div[@id='inlineDialog']")))
#             # Wait for the close button to be clickable
#             element = self.wait.until(EC.element_to_be_clickable(
#                 (By.XPATH, "//button[contains(@class, 'c-glyph glyph-cancel') and @title='Close']")))
#             # Click the close button
#             element.click()
#             print('Popup closed successfully.')
#         except:
#             print('Failed to close the popup.')
#     def new_notebook(self):
#         self.find_element(By.XPATH, '//*[@id="file-menu"]').click()


# run = PARENT()
# run.landFirstPage()
# run.close_popup()
# run.click_file()
# run.new_notebook()


# time.sleep(1000)



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the Chrome driver
driver = webdriver.Chrome()

# Open the Colab sign-in page
driver.get("https://accounts.google.com/signin/v2/identifier?service=wise&passive=1209600&continue=https%3A%2F%2Fcolab.research.google.com%2F&followup=https%3A%2F%2Fcolab.research.google.com%2F&flowName=GlifWebSignIn&flowEntry=ServiceLogin")

# Find the email input field and enter your email address
email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
email_input.send_keys("ahmed.abdallah1024@gmail.com")

next_button = driver.find_element(By.XPATH, '//*[@id="next"]/div/div')
next_button.click()

# email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
# email_input.send_keys("ahmed.abdallah1024@gmail.com")



# Click the "Next" button
next_button = driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span')
next_button.click()
time.sleep(1000)
wait = WebDriverWait(driver, 10)
wait.until(EC.url_contains("accounts.google.com/signin/v2/identifier"))
time.sleep(1000)
# Find the password input field and enter your password
password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
password_input.send_keys("Aa@27835557")

# Click the "Next" button
next_button = driver.find_element(By.XPATH, "//div[@id='passwordNext']")
next_button.click()

# Wait for Colab to load
WebDriverWait(driver, 10).until(EC.title_contains("Google Colaboratory"))

time.sleep(1000)