from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # Manejo de esperas en Selenium
from selenium.webdriver.support import expected_conditions as EC # Condiciones de espera explícitas
from selenium.common.exceptions import TimeoutException
import time
from config import config
from utils.helpers import generar_identificacion_aleatoria
from selenium.webdriver.common.action_chains import ActionChains  # Permite realizar interacciones avanzadas

class MetasFormPage(BasePage):
    def metas_fiancieras(self):
        xpath = "//article[.//h2[normalize-space()='Solución Educativa']]//button[normalize-space()='Cotizar']"
        try:
            # 1) Espera hasta que aparezca en el DOM (aunque no sea visible aún)
            element = WebDriverWait(self.driver, 40).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            # 2) Scroll hasta el elemento
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element
            )
            return element  # 🔹 Devolvemos el elemento para usarlo después

        except TimeoutException:
            print("⏰ No se pudo encontrar el botón 'Cotizar' en la tarjeta 'Solución Educativa'.")
            raise

    def button_cotizar(self):
        # Usamos el método anterior para obtener el botón
        boton = self.metas_fiancieras()
        # 3) Esperamos un poco extra si es necesario
        time.sleep(2)
        # 4) Hacemos clic en el botón
        boton.click()
        # 5) Validación
        print("✅ Se hizo clic en el botón 'Cotizar' (Metas Financieras)")


    def button_regreso(self):
        boton_regresar_p = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[./span[text()='Regresar al perfilamiento']]"))
        )
        boton_regresar_p.click()      
        pass
    

    def button_comprador(self):
        boton_comprador = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[./span[text()='Regresar al comparador']]"))
    )
        boton_comprador.click()
    pass
