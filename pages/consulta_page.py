from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import time
from config import config
from selenium.webdriver.common.action_chains import ActionChains  # Permite realizar interacciones avanzadas
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class ConsultaPage(BasePage):
    def login(self):
        self.open_url("https://globalseguros--qaonb.sandbox.my.salesforce.com/")
        self.enter_text(By.CSS_SELECTOR, "input[name='username']", config.USERNAME)
        self.enter_text(By.ID, 'password', config.PASSWORD)
        self.click_element(By.CSS_SELECTOR, "input[id='Login']")
        time.sleep(15)
        print("Ingreso Login")


    def complete_form(self):
        """ Completa el formulario inicial """
        target_url = "https://globalseguros--qaonb.sandbox.lightning.force.com/lightning/cmp/vlocity_ins__vlocityLWCOmniWrapper?c__target=c%3AgsvFormularyEnglish&c__layout=lightning&c__tabLabel=Perfilamiento"
        self.open_url(target_url)

        # Seleccionar opción en el dropdown
        wait = WebDriverWait(self.driver, 20)  # Asegúrate de tener esto antes de usar 'wait'
        dropdown_identificacion = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="comboboxId-215"]'))
        )
        self.driver.execute_script("arguments[0].click();", dropdown_identificacion)

        # Espera la opción de "CÉDULA DE CIUDADANÍA" y haz clic en ella
        opcion_identificacion = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//div[@role="option"]//span[contains(text(), "CEDULA DE CIUDADANIA")]')))
        opcion_identificacion.click()

        # Ingresar nombre del asesor
        self.enter_text(By.XPATH, "/html/body/div[4]/div[1]/section/div[1]/div[2]/div[2]/div[1]/div/div/div/div/div/c-gsv-formulary-english/div/article/div[2]/vlocity_ins-omniscript-step[1]/div[3]/slot/vlocity_ins-omniscript-block[2]/div/div/section/fieldset/slot/vlocity_ins-omniscript-typeahead-block/div/slot/vlocity_ins-omniscript-typeahead/slot/div/c-typeahead/div/div[2]/div[2]/div[1]/div/div[1]/input", config.ASESOR)

        # Esperar y seleccionar una opción en el dropdown
        dropdown_option = self.wait_for_element(By.XPATH, "//span[contains(@class, 'slds-listbox__option-text') and contains(text(), 'PROYECTA-T LTDA-BOGOTA')]")

        # Mueve el cursor hasta la opción y selecciona
        ActionChains(self.driver).move_to_element(dropdown_option).perform()
        dropdown_option.click()

        # Hacer clic en "Siguiente"
        next_button = self.wait_for_element(By.XPATH, "//button[.//span[text()='Siguiente']]")
        self.scroll_into_view(next_button)
        next_button.click()

        print("Formulario inicial completado")