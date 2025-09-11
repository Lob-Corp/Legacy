import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from pydantic import BaseModel

class WebAction(BaseModel):
    def run(self, _: webdriver.Firefox):
        raise NotImplementedError()

class WebGetAction(WebAction):
    url: str

    def run(self, driver):
        driver.get(self.url)

class WebWaitAction(WebAction):
    seconds: float

    def run(self, _):
        time.sleep(self.seconds)

class WebSaveHTMLAction(WebAction):
    filename: str

    def run(self, driver):
        folder = os.path.dirname(self.filename)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(driver.page_source)

class WebClickAction(WebAction):
    by: str
    value: str

    def run(self, driver):
        by_mapping = {
            "id": By.ID,
            "name": By.NAME,
            "xpath": By.XPATH,
            "css": By.CSS_SELECTOR,
            "class": By.CLASS_NAME
        }
        element = driver.find_element(by_mapping[self.by.lower()], self.value)
        element.click()

class WebTypeAction(WebAction):
    by: str
    value: str
    text: str

    def run(self, driver):
        by_mapping = {
            "id": By.ID,
            "name": By.NAME,
            "xpath": By.XPATH,
            "css": By.CSS_SELECTOR,
            "class": By.CLASS_NAME
        }
        element = driver.find_element(by_mapping[self.by.lower()], self.value)
        element.clear()
        element.send_keys(self.text)

class WebSelectAction(WebAction):
    by: str
    value: str
    option: str

    def run(self, driver):
        from selenium.webdriver.support.ui import Select
        by_mapping = {
            "id": By.ID,
            "name": By.NAME,
            "xpath": By.XPATH,
            "css": By.CSS_SELECTOR,
            "class": By.CLASS_NAME
        }
        element = driver.find_element(by_mapping[self.by.lower()], self.value)
        select = Select(element)
        select.select_by_value(self.option)

class WebActionRunner:

    _driver: webdriver.Firefox = None

    def __init__(self):
        GeckoDriverManager().install()
        self._driver = webdriver.Firefox()

    def run_action_sequence(self, actions: list[WebAction]):
        for action in actions:
            action.run(self._driver)

    def dispose(self):
        self._driver.quit()

WEB_ACTION_TYPE = {
    "Get": WebGetAction,
    "Click": WebClickAction,
    "SaveHTML": WebSaveHTMLAction,
    "Wait": WebWaitAction,
    "Type": WebTypeAction,
    "Select": WebSelectAction,
}
