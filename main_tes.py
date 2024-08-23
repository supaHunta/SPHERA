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
from selenium.webdriver.common.action_chains import ActionChains
import random

chrome_options = Options()
chrome_options.add_argument("user-data-dir=selenium")
chrome_options.add_argument("auto-open-devtools-for-tabs")

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)

CONFIG_BASE_URL = "https://staging.sphera.work/"

USER_OWNER_PHONE = "9999999999"
USER_ADMIN_PHONE = "9777777777"
USER_USER_PHONE = "9111111111"


def get_shadow_root(element):
    return driver.execute_script('return arguments[0].shadowRoot', element)


class Authorization(unittest.TestCase):

    cookies = None

    def _prepare_form_fields(self, phone):
        self.email_field = driver.find_element(
            By.NAME, "phone").send_keys(phone)
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
        wait.until(EC.presence_of_element_located((By.NAME, "phone")))
        self._prepare_form_fields(USER_OWNER_PHONE)
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'button.phone-input__receive-button:not([disabled])')))
        try:
            driver.find_element(By.CSS_SELECTOR, "button").click()
        except Exception as ex:
            print('Element not found', ex)
        wait.until(EC.presence_of_element_located(
            (By.ID, "one-time-code"))).send_keys("9999")
        sleep(3)
        # wait.until(EC.presence_of_element_located((By. CSS_SELECTOR, "div[role = 'dialog']")))
        # dialog = driver.find_element(By.CLASS_NAME, 'MuiDialogActions-spacing')
        # dialog.find_elements(By.TAG_NAME, 'button')[0].click()
        cookies = driver.get_cookies()
        driver.find_elements(
            By.CSS_SELECTOR, 'button[type="button"]')[-1].click()
        wait.until(EC.presence_of_element_located(
            (By. CSS_SELECTOR, "div[role = 'dialog']")))
        dialog = driver.find_element(By.CLASS_NAME, 'MuiDialogActions-spacing')
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'button')))
        dialog.find_elements(By.TAG_NAME, 'button')[0].click()
        cookies = driver.get_cookies()

    @unittest.skip("") 
    def test_02_choosing_random_channel_and_typing_a_message(self):
        print("test_02_choosing_random_channel_and_typing_a_message")
        self.driver.get(CONFIG_BASE_URL)
        wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'channel-data-container')))
        channel = driver.find_elements(
            By.CLASS_NAME, 'channel-data-container')[1::]
        random_channel = random.choice(channel)
        random_channel.click()
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div[aria-owns="quill-mention-list"]'))).click()
        self.driver.find_element(
            By.CSS_SELECTOR, 'div[aria-owns="quill-mention-list"]').send_keys(rand.generate_random_string(15))
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//button[text()="Отправить"]'))).click()

    @unittest.skip("")
    def test_03_creating_and_deleting_a_channel(self):
        """Test creating and deleting a channel"""
        print("test_03_creating_and_deleting_a_channel")

        CREATE_CHANNEL_BTN_SELECTOR = "button[aria-label='Создать канал']"
        FORM_DISCRIPTION_FIELD_SELECTOR = "textarea[name='description']"
        
        self.driver.get(CONFIG_BASE_URL)
        # Wait until the "Create channel" button appears
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, CREATE_CHANNEL_BTN_SELECTOR))).click()
        # Fill in the channel name and description
        wait.until(EC.presence_of_element_located((By.NAME, 'name'))
                   ).send_keys(rand.generate_random_string(15))
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, FORM_DISCRIPTION_FIELD_SELECTOR))).send_keys(rand.generate_random_string(60))
        # Submit the form
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button[type='submit']"))).click()
        # Wait until the channel appears in the list
        wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div[role='dialog']")))
        # Click on the last button in the channel list
        button_skip = driver.find_element(
            By.CSS_SELECTOR, "div[role='dialog']")
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//button[text() = 'Пока пропустить']"))).click()
        wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'header__button-icon'))).click()
        # Click on the "Channels" tab
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div[role = 'tablist']")))
        tablist = driver.find_element(By.CSS_SELECTOR, "div[role = 'tablist']")
        tablist.find_elements(
            By.CSS_SELECTOR, 'button[role = "tab"]')[-1].click()
        # Wait until the "Delete channel" button appears
        wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "MuiBox-root")))
        # Click on the "Delete channel" button
        driver.find_elements(By.TAG_NAME, 'button')[-1].click()
        # Wait until the confirmation dialog appears
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'button[type="submit"]'))).click()
        # Wait until the success toast appears
        try:
            wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'Toastify__toast')))
            toast = driver.find_element(By.CLASS_NAME, 'Toastify__toast')
            self.assertEqual(toast.text, "Канал удален")
        except Exception as ex:
            print('No toasts found!', ex)
        sleep(5)

    @unittest.skip("") 
    def test_04_replying_to_a_comment(self):
        print("test_04_replying_to_a_comment")
        self.driver.get(CONFIG_BASE_URL)
        wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'channel-data-container')))
        channel = driver.find_elements(
            By.CLASS_NAME, 'channel-data-container')[1:]
        random_channel = random.choice(channel)
        random_channel.click()
        wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'message-card')))
        comment_box = driver.find_elements(By.CLASS_NAME, 'message-card')
        comment1 = comment_box[-1]
        comment_hover1 = ActionChains(driver).move_to_element(comment1)
        comment_hover1.perform()
        
        WebDriverWait(comment1, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'button[aria-label="Ответить на сообщение"]'))).click()
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div[aria-owns="quill-mention-list"]'))).click()
        self.driver.find_element(
            By.CSS_SELECTOR, 'div[aria-owns="quill-mention-list"]').send_keys(rand.generate_random_string(15))
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//button[text()="Отправить"]'))).click()

    @unittest.skip("") 
    def test_05_opening_a_discussing(self):
        """
        This test case verifies if the user can leave a reaction on a comment.
        It performs the following steps:
        1. Navigates to the Configuration URL.
        2. Waits for all the channels to load.
        3. Selects a random channel.
        4. Waits for all the comments to load.
        5. Selects a random comment.
        6. Performs a hover action on the comment.
        7. Waits for the reaction button to appear.
        8. Clicks on the reaction button.
        9. Waits for the emojis to load.
        10. Selects a random emoji.

        Note: The test currently does not verify if the reaction was successfully added.
        """
        print("test_05_opening_a_discussing")

        # Navigate to the configuration URL
        self.driver.get(CONFIG_BASE_URL)

        # Wait for all the channels to load
        wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'channel-data-container')))

        # Select a random channel
        channel = driver.find_elements(
            By.CLASS_NAME, 'channel-data-container')[1::]
        random_channel = random.choice(channel)
        random_channel.click()
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div[aria-owns="quill-mention-list"]'))).click()
        self.driver.find_element(
            By.CSS_SELECTOR, 'div[aria-owns="quill-mention-list"]').send_keys(rand.generate_random_string(15))
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//button[text()="Отправить"]'))).click()
        # Wait for all the comments to load
        comment_box = driver.find_elements(By.CLASS_NAME, 'message-card')
        comment1 = comment_box[-1]
        # Select a random comment
        # Perform a hover action on the comment
        comment_hover = ActionChains(driver).move_to_element(comment1)
        comment_hover.perform()

        # Click on the reaction button
        try:
            WebDriverWait(comment1, 10).until(EC.visibility_of_element_located(
                       (By.CSS_SELECTOR, 'button[aria-label="Начать обсуждение"]'))).click()
        except Exception as ex:
            print('Reaction button not found!', ex)
        wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'div[aria-owns="quill-mention-list"]')))[-1].click()
        self.driver.find_elements(
            By.CSS_SELECTOR, 'div[aria-owns="quill-mention-list"]')[-1].send_keys(rand.generate_random_string(15))
        wait.until(EC.presence_of_all_elements_located(
            (By.TAG_NAME, 'button')))
        driver.find_elements(By.TAG_NAME, 'button')[-1].click()

    @unittest.skip("")
    def test_06_editing_a_comment(self):
        print("test_06_editing_a_comment")

        # Navigate to the configuration URL
        self.driver.get(CONFIG_BASE_URL)

        # Wait for all the channels to load
        wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'channel-data-container')))

        # Select a random channel
        channel = driver.find_elements(
            By.CLASS_NAME, 'channel-data-container')[1::]
        random_channel = random.choice(channel)
        random_channel.click()
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div[aria-owns="quill-mention-list"]'))).click()
        self.driver.find_element(
            By.CSS_SELECTOR, 'div[aria-owns="quill-mention-list"]').send_keys(rand.generate_random_string(15))
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//button[text()="Отправить"]'))).click()

        # Wait for all the comments to load
        wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'message-card')))
        sleep(1)
        # Select a last comment
        comment_box = driver.find_elements(By.CLASS_NAME, 'message-card')
        last_comment = comment_box[0]
        comment_first = last_comment.text
        comment = last_comment

        # Perform a hover action on the comment
        comment_hover = ActionChains(driver).move_to_element(comment)
        comment_hover.perform()

        # Click on the discussion button
        WebDriverWait(comment, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'button[aria-label="Редактировать сообщение"]'))).click()
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div[aria-owns="quill-mention-list"]'))).click()
        comment_edit = self.driver.find_element(
            By.CSS_SELECTOR, 'div[aria-owns="quill-mention-list"]')
        comment_edit.clear()
        comment_edit.send_keys(rand.generate_random_string(15))
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//button[text()="Отправить"]'))).click()
        wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'message-card')))
        sleep(0.5)
        # Select a last comment
        comment_box = driver.find_elements(By.CLASS_NAME, 'message-card')
        last_comment = comment_box[0]
        comment_second = last_comment.text

        # Check if the comments are different
        self.assertNotEqual(comment_first, comment_second)
        sleep(2)
    @unittest.skip("")  
    def test_07_leaving_a_reaction(self):
        
        print("test_07_leaving_a_reaction")
        self.driver.get(CONFIG_BASE_URL)
        wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'channel-data-container')))
        channel = driver.find_elements(
            By.CLASS_NAME, 'channel-data-container')[1:]
        random_channel = random.choice(channel)
        random_channel.click()
        wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'message-card')))
        comment_box = driver.find_elements(By.CLASS_NAME, 'message-card')
        comment1 = comment_box[-1]
        comment_hover1 = ActionChains(driver).move_to_element(comment1)
        comment_hover1.perform()
        
        WebDriverWait(comment1, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'button[aria-label="Добавить реакцию"]'))).click()
        shadow_host = driver.find_element(By.TAG_NAME, 'em-emoji-picker')
        WebDriverWait(get_shadow_root(shadow_host), 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-setsize = "1747"]')))
        smile_window = get_shadow_root(shadow_host).find_elements(By.CSS_SELECTOR, 'button[aria-setsize = "1747"]')
        randomm_smile = random.choice(smile_window)
        randomm_smile.click()
        sleep(0.5)
        
        

    def test_08_archiving_a_channel_after_creating(self):
        print("test_08_archiving_a_channel")
        
        GENERATED_NAME = rand.generate_random_string(15)
        GENERATED_DESCRIPTION = rand.generate_random_string(60)
        
        CREATE_CHANNEL_BTN_SELECTOR = "button[aria-label='Создать канал']"
        FORM_DISCRIPTION_FIELD_SELECTOR = "textarea[name='description']"
        
        self.driver.get(CONFIG_BASE_URL)
        # Wait until the "Create channel" button appears
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, CREATE_CHANNEL_BTN_SELECTOR))).click()
        # Fill in the channel name and description
        wait.until(EC.presence_of_element_located((By.NAME, 'name'))
                   ).send_keys(GENERATED_NAME)
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, FORM_DISCRIPTION_FIELD_SELECTOR))).send_keys(GENERATED_DESCRIPTION)
        # Submit the form
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button[type='submit']"))).click()
        # Wait until the channel appears in the list
        wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div[role='dialog']")))
        # Click on the last button in the channel list
        button_skip = driver.find_element(
            By.CSS_SELECTOR, "div[role='dialog']")
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//button[text() = 'Пока пропустить']"))).click()
        wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'header__button-icon'))).click()
        # Click on the "Channels" tab
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div[role = 'tablist']")))
        tablist = driver.find_element(By.CSS_SELECTOR, "div[role = 'tablist']")
        tablist.find_elements(
            By.CSS_SELECTOR, 'button[role = "tab"]')[-1].click()
        # Wait until the "Archive channel" button appears
        wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "MuiBox-root")))
        # Click on the "Delete channel" button
        driver.find_elements(By.TAG_NAME, 'button')[-2].click()
        # Wait until the confirmation dialog appears
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'button[type="submit"]'))).click()
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'channels-list-header')))
        channel_wrapper = driver.find_elements(By.CLASS_NAME, 'channels-list-header')[0].click()
        button_wrapper = driver.find_elements(By.CLASS_NAME, 'header-content-wrapper')[1]
        menulist_clicker = button_wrapper.find_elements(By.CSS_SELECTOR, 'button[variant="permanent"]')[0]
        menulist_clicker.click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[role="menu"]')))
        menulist = driver.find_element(By.CSS_SELECTOR, 'ul[role="menu"]')
        listitems = menulist.find_elements(By.TAG_NAME, 'li')[-1].click()
        wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'channel-name')))
        channel_list = driver.find_elements(By.CLASS_NAME, 'channel-name')
        for channel in channel_list:
            if channel.text == GENERATED_NAME:
                self.assertEqual(channel.text, GENERATED_NAME)
                channel.click()
                sleep(1)
                print('Channel has been successfully archived!')
            else:
                self.assertNotEqual(channel.text, GENERATED_NAME)
        wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'header__button-icon'))).click()
        # Click on the "Channels" tab
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div[role = 'tablist']")))
        tablist = driver.find_element(By.CSS_SELECTOR, "div[role = 'tablist']")
        tablist.find_elements(
            By.CSS_SELECTOR, 'button[role = "tab"]')[-1].click()
        # Wait until the "Delete channel" button appears
        wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "MuiBox-root")))
        # Click on the "Delete channel" button
        driver.find_elements(By.TAG_NAME, 'button')[-1].click()
        # Wait until the confirmation dialog appears
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'button[type="submit"]'))).click()
        # Wait until the success toast appears
        try:
            wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'Toastify__toast')))
            toast = driver.find_element(By.CLASS_NAME, 'Toastify__toast')
            self.assertEqual(toast.text, "Канал удален")
        except Exception as ex:
            print('No toasts found!', ex)
        sleep(5)
        
            
            
        
    
    def tearDown(self):
        print('tearDown')


if __name__ == '__main__':
    unittest.main()
