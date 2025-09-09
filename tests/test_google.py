import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    print(ChromeDriverManager().install())
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_google_search(driver):
    driver.get("https://www.google.com")
    assert "google" in driver.title.lower()
