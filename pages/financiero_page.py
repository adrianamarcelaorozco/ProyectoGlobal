from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # Manejo de esperas en Selenium
from selenium.webdriver.support import expected_conditions as EC # Condiciones de espera explícitas
import time
from config import config
from selenium.webdriver.common.action_chains import ActionChains  # Permite realizar interacciones avanzadas


class FinancieroFormPage(BasePage):
    def perfil_financiero(self):
        wait = WebDriverWait(self.driver, 30)
        # 1. Click en el combobox
        promedio = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//label[span[normalize-space(text())='¿Cuál es el promedio de tus ingresos mensuales?']]/following::input[@role='combobox'][1]"
            ))
        )
        promedio.click()

        # 2. Seleccionar la opción
        opcion = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//div[@role='option' and @data-value='0 a 4.000.000']"
            ))
        )
        opcion.click()  # Espera hasta que el campo de texto sea clickeable.
        # Selección de la opción en el desplegable (espera explícita)

        # Esperar a que el campo sea clickeable
    # 1. Abrir combobox "¿Cuál es tu ocupación?"
        ocupacion_input = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//label[span[normalize-space(text())='¿Cuál es tu ocupación?']]/following::input[@role='combobox'][1]"
            ))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", ocupacion_input)
        ocupacion_input.click()

        # 2. Seleccionar la opción "Empleado"
        empleado_option = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//div[@role='option' and @data-value='Empleado']"
            ))
        )
        empleado_option.click()
        # 1. Esperar input de ahorros
        ahorros_input = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//label[normalize-space(text())='¿Cuál es el valor aproximado de tus ahorros y/o cesantías?']/following::input[@class='vlocity-input slds-input'][1]"
            ))
        )

        # 2. Scroll hasta el campo
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", ahorros_input)

        # 3. Click + ingreso de datos
        ahorros_input.click()
        ahorros_input.clear()
        ahorros_input.send_keys(config.VALOR_APROX)
        time.sleep(2) # Esperar 2 segundos para asegurar que el valor se haya ingresado correctamente
        checkbox_labels = [
            "Asegurar la educación superior de mis hijos",
            "Estudiar un posgrado",
            "Comprar casa"
        ]
        # Opciones que quieres seleccionar
        transportes = ["Bicicleta", "Carro Particular", "Patineta"]

        for transporte in transportes:
            # XPath: busca el input checkbox por su value
            xpath = f"//input[@type='checkbox' and @name='transport' and @value='{transporte}']"
            
            checkbox = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            
            # Buscar el label asociado al input
            label = self.driver.find_element(By.XPATH, f"//label[@for='{checkbox.get_attribute('id')}']")
            
            # Scroll hasta el label
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", label
            )

            # Clic en el label (más confiable que en el input)
            wait.until(EC.element_to_be_clickable((By.XPATH, f"//label[@for='{checkbox.get_attribute('id')}']"))).click()
            
    def button_siguiente(self):
        try:
            # XPath más estable, busca el botón por el texto visible
            button_xpath = "//button[contains(text(),'Guardar y continuar')]"

            # Esperar hasta que el botón sea visible y clickeable
            button_element = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, button_xpath))
            )

            # Hacer scroll hasta el botón para asegurarnos de que sea visible
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                button_element
            )

            # Clic en el botón
            button_element.click()
            print("✅ Botón 'Guardar y continuar' clickeado correctamente.")

            # Esperar hasta que el botón desaparezca o la página avance
            WebDriverWait(self.driver, 20).until_not(
                EC.presence_of_element_located((By.XPATH, button_xpath))
            )
            print("➡️ Avanzó de pantalla después de guardar.")

        except Exception as e:
            print(f"❌ Error al intentar hacer clic en 'Guardar y continuar': {e}")
            raise


    def button_anterior(self):
        boton_regresar= WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Anterior']"))
        )
        boton_regresar.click()       
        pass