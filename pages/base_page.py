from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open_url(self, url):
        self.driver.get(url)
        self.driver.maximize_window()

    def wait_for_element(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def click_element(self, by, value, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        element.click()

    def enter_text(self, by, value, text):
        element = self.wait_for_element(by, value)
        element.clear()
        element.send_keys(text)

    def scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def select_dropdown_option(self, by_dropdown, by_option):
        """ Selecciona una opción en un dropdown """
        self.click_element(*by_dropdown)  # Abre el dropdown
        self.click_element(*by_option)  # Selecciona la opción


