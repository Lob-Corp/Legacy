import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

class WebAction:
    def run(self, _: webdriver.Firefox):
        raise NotImplementedError()

class WebGetAction(WebAction):
    def __init__(self, url):
        self._url = url

    def run(self, driver):
        driver.get(self._url)

class WebWaitAction(WebAction):
    def __init__(self, seconds):
        self.seconds = seconds

    def run(self, _):
        time.sleep(self.seconds)

class WebSaveHTMLAction(WebAction):
    def __init__(self, filename):
        self.filename = filename

    def run(self, driver):
        folder = os.path.dirname(self.filename)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(driver.page_source)

class WebClickAction(WebAction):
    def __init__(self, by, value):
        self._by = by.lower()
        self._value = value

    def run(self, driver):
        by_mapping = {
            "id": By.ID,
            "name": By.NAME,
            "xpath": By.XPATH,
            "css": By.CSS_SELECTOR,
            "class": By.CLASS_NAME
        }
        element = driver.find_element(by_mapping[self._by], self._value)
        element.click()

class WebTypeAction(WebAction):
    def __init__(self, by, value, text):
        self._by = by.lower()
        self._value = value
        self._text = text

    def run(self, driver):
        by_mapping = {
            "id": By.ID,
            "name": By.NAME,
            "xpath": By.XPATH,
            "css": By.CSS_SELECTOR,
            "class": By.CLASS_NAME
        }
        element = driver.find_element(by_mapping[self._by], self._value)
        element.clear()
        element.send_keys(self._text)

class WebActionRunner:

    _driver: webdriver.Firefox = None

    def __init__(self):
        GeckoDriverManager().install()

    def run_action_sequence(self, actions: list[WebAction]):
        if (self._driver is not None):
            self._driver.quit()
            self._driver = None
        self._driver = webdriver.Firefox()

        for action in actions:
            action.run(self._driver)

    def dispose(self):
        self._driver.quit()
