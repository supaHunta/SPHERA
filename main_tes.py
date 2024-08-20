import requests
from time import sleep
import random_file_generator as RFG
import rand
import unittest
from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import random

chrome_options = Options()
chrome_options.add_argument("user-data-dir=selenium")

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)

CONFIG_BASE_URL = "https://staging.sphera.work/"

USER_OWNER_PHONE = "9999999999"
USER_ADMIN_PHONE = "9777777777"
USER_USER_PHONE = "9111111111"



class Authorization(unittest.TestCase):
    
    cookies = None


    def _prepare_form_fields(self,phone):
        self.email_field = driver.find_element(By.NAME, "phone").send_keys(phone)
    # Сетап сайта и подвязка переменных к соответсвующим формам

    @classmethod
    def setUpClass(self):
        print('Тест-Сьют №1: Авторизация \n')
        self.driver = driver
        self.driver.get(CONFIG_BASE_URL)

    def setUp(self):
        """
        Sets up the test environment before each test case.
        """
        print('\n\nsetup')
        
    def test_01_authorization(self):
        global cookies
        print('test_01_authorization')
        wait.until(EC.presence_of_element_located((By.NAME, "phone" )))
        self._prepare_form_fields(USER_OWNER_PHONE)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.phone-input__receive-button:not([disabled])')))
        try:
            driver.find_element(By.CSS_SELECTOR, "button").click()
        except Exception as ex:
            print('Element not found', ex)
        wait.until(EC.presence_of_element_located((By.ID, "one-time-code"))).send_keys("9999")
        sleep(3)
        # wait.until(EC.presence_of_element_located((By. CSS_SELECTOR, "div[role = 'dialog']")))
        # dialog = driver.find_element(By.CLASS_NAME, 'MuiDialogActions-spacing')
        # dialog.find_elements(By.TAG_NAME, 'button')[0].click()
        cookies = driver.get_cookies()
        driver.find_elements(By.CSS_SELECTOR, 'button[type="button"]')[-1].click()
        wait.until(EC.presence_of_element_located((By. CSS_SELECTOR, "div[role = 'dialog']")))
        dialog = driver.find_element(By.CLASS_NAME, 'MuiDialogActions-spacing')
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'button')))
        dialog.find_elements(By.TAG_NAME, 'button')[0].click()
        cookies = driver.get_cookies()
        
        
    def test_02_choosing_random_channel_and_typing_a_message(self):
        print("test_02_choosing_random_channel_and_typing_a_message")
        self.driver.get(CONFIG_BASE_URL)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'channel-data-container')))
        channel = driver.find_elements(By.CLASS_NAME, 'channel-data-container')
        random_channel = random.choice(channel)
        random_channel.click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-owns="quill-mention-list"]'))).click()
        self.driver.find_element(By.CSS_SELECTOR, 'div[aria-owns="quill-mention-list"]').send_keys(rand.generate_random_string(15))
        wait.until(EC.presence_of_element_located((By.XPATH, '//button[text()="Отправить"]'))).click()
        
        
    def test_03_creating_a_channel(self):
        print("test_03_creating_a_channel")
        self.driver.get(CONFIG_BASE_URL)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Создать канал']"))).click()
        wait.until(EC.presence_of_element_located((By.NAME, 'name'))).send_keys(rand.generate_random_string(15))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='description']"))).send_keys(rand.generate_random_string(60))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))).click()
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button[type='button']"))).click()
        driver.find_elements(By.CSS_SELECTOR, "button[type='button']")[-1].click()
        sleep(5)
                
    def tearDown(self):
        print('tearDown')
        
        
if __name__ == '__main__':
    unittest.main()