import os
import time
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from pydantic import BaseModel
from typing import List, Tuple, Optional

from pydantic import BaseModel, Field
from typing import Optional, List
import re

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

class CleanRule(BaseModel):
    pattern: str = Field(..., description="Regex pattern to search in the HTML")
    replacement: Optional[str] = Field(
        None,
        description="Replacement string for the matched pattern. If omitted, the text will be removed."
    )
    flags: Optional[List[str]] = Field(
        default=None,
        description="Optional regex flags (e.g. ['ignorecase', 'dotall'])"
    )

    def compile_flags(self) -> int:
        """Convert list of string flags into re flags"""
        flag_map = {
            "ignorecase": re.IGNORECASE,
            "multiline": re.MULTILINE,
            "dotall": re.DOTALL,
        }
        result = 0
        if self.flags:
            for f in self.flags:
                result |= flag_map.get(f.lower(), 0)
        return result

    def apply(self, text: str) -> str:
        """Apply this cleaning rule to given text"""
        return re.sub(
            self.pattern,
            self.replacement if self.replacement is not None else "",
            text,
            flags=self.compile_flags()
        )

class WebSaveHTMLAction(WebAction):
    filename: str
    clean_rules: Optional[List[CleanRule]] = None

    def run(self, driver):
        folder = os.path.dirname(self.filename)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

        html = driver.page_source

        if self.clean_rules:
            for rule in self.clean_rules:
                html = rule.apply(html)

        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(html)

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
    option: str | int

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
        if isinstance(self.option, int):
            select.select_by_index(self.option)
        else:
            select.select_by_value(self.option)

class WebActionRunner:

    _driver: webdriver.Firefox = None

    def __init__(self):
        GeckoDriverManager().install()
        options: Options = Options()
        self._driver = webdriver.Firefox(options=options)

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
