import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(service=service, options=options)

@pytest.fixture
def driver():
    driver = setup_driver()
    yield driver
    driver.quit()
