import os
import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class SeleniumSession:
    def __init__(self, url, driver_path=None, cookies_file="cookies.pkl", username=None, password=None):
        """
        Initializes a Selenium session manager.

        :param url: The website URL to manage login persistence.
        :param driver_path: Optional path to the WebDriver.
        :param cookies_file: The filename to store cookies.
        :param username: username to login
        :param password: password to login
        """
        self.username = username
        self.password = password
        self.url = url
        self.cookies_file = cookies_file
        self.driver = webdriver.Chrome(executable_path=driver_path) if driver_path else webdriver.Chrome()
        self.delay = 10 # seconds

    def load_cookies(self):
        """Loads cookies from a file and applies them to the browser."""
        if os.path.exists(self.cookies_file):
            print("Loading cookies...")
            self.driver.get(self.url)  # Open site first
            with open(self.cookies_file, "rb") as f:
                cookies = pickle.load(f)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            self.driver.refresh()
            print("Logged in using stored cookies!")
            return True
        return False

    def save_cookies(self):
        """Saves the current browser session's cookies to a file."""
        print("Saving cookies...")
        cookies = self.driver.get_cookies()
        with open(self.cookies_file, "wb") as f:
            pickle.dump(cookies, f)
        print("Cookies saved!")

    def login_and_store_cookies(self):
        """Allows manual login and then saves cookies for future use."""
        print("No cookies found. Please log in manually.")
        self.driver.get(self.url)
        
        try:
            myElem = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.NAME, 'username')))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")
        
        user = self.driver.find_element(By.NAME, "username")
        user.click()
        user.send_keys(self.username)
        psswd = self.driver.find_element(By.NAME, "password")
        psswd.click()
        psswd.send_keys(self.password)
        psswd.send_keys(Keys.RETURN)
        print("loading page and cookies!")
        time.sleep(5)
        self.save_cookies()

    def start_session(self):
        """
        Starts the Selenium session:
        - Tries to load cookies first
        - If no cookies exist, requires manual login and then saves cookies
        """
        if not self.load_cookies():
            self.login_and_store_cookies()

    def close(self):
        """Closes the browser after a short delay."""
        print("Closing session in 5 seconds...")
        time.sleep(5)
        self.driver.quit()







