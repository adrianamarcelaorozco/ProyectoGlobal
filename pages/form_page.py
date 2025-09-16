from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # Manejo de esperas en Selenium
from selenium.webdriver.support import expected_conditions as EC # Condiciones de espera explícitas
import time
from config import config
from utils.helpers import generar_identificacion_aleatoria
from selenium.webdriver.common.action_chains import ActionChains  # Permite realizar interacciones avanzadas
from utils.helpers import generar_numero_telefono  # Importa la función desde helpers.py
from utils.helpers import generar_correo_aleatorio  # Importa la función desde helpers.py

class FormPage(BasePage):
    def complete_form(self):
        """ Completa el formulario inicial """
        target_url = "https://globalseguros--qaonb.sandbox.lightning.force.com/lightning/cmp/vlocity_ins__vlocityLWCOmniWrapper?c__target=c%3AgsvFormularyEnglish&c__layout=lightning&c__tabLabel=Perfilamiento"
        self.open_url(target_url)

        # Seleccionar opción en el dropdown
        self.select_dropdown_option(
            (By.XPATH, "//input[@role='combobox' and starts-with(@aria-controls, 'combobox-list')]"),
            (By.XPATH, '//div[@role="option" and .//span[text()="CEDULA DE CIUDADANIA"]]')
        )
        # Generar e ingresar número de identificación aleatorio
        numero_identificacion = generar_identificacion_aleatoria()
        self.enter_text(By.XPATH, "//input[contains(@class, 'vlocity-input') and @type='text']", numero_identificacion)

       # Datos de Asesor
        self.enter_text(
            By.XPATH,
            "//input[contains(@class, 'slds-input') and @role='combobox' and contains(@aria-autocomplete, 'list')]",
            config.ASESOR
        )

        # Esperar y seleccionar la opción en el dropdown
        dropdown_option = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@role="option" and contains(.//span, "PROYECTA-T LTDA-BOGOTA")]')
            )
        )

        # Mover el cursor hasta la opción y seleccionarla
        ActionChains(self.driver).move_to_element(dropdown_option).perform()
        dropdown_option.click()

    def complete_form_email(self):
        #Completa el formulario inicial con el correo
        target_url = "https://globalseguros--qaonb.sandbox.lightning.force.com/lightning/cmp/vlocity_ins__vlocityLWCOmniWrapper?c__target=c%3AgsvFormularyEnglish&c__layout=lightning&c__tabLabel=Perfilamiento"
        self.open_url(target_url)

        # Esperar a que el elemento esté presente
        self.driver.implicitly_wait(10)

        # Encontrar el botón de radio por su ID y hacer clic
        opcion_email_celular = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Email o Celular')]")
        opcion_email_celular.click()

        telefono_input = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Ingrese el número telefónico']"))
        )
        telefono_input.click()  # Limpia el campo antes de ingresar el número
        telefono_input.send_keys(generar_numero_telefono())

        correo_input = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Ingrese el correo electrónico']"))
        )
        correo_aleatorio = generar_correo_aleatorio()
        correo_input.send_keys(correo_aleatorio)
        time.sleep(5)
        # Datos de Asesor
        self.enter_text(
            By.XPATH,
            "//input[contains(@class, 'slds-input') and @role='combobox' and contains(@aria-autocomplete, 'list')]",
            config.ASESOR
        )

        # Esperar y seleccionar la opción en el dropdown
        dropdown_option = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@role="option" and contains(.//span, "PROYECTA-T LTDA-BOGOTA")]')
            )
        )

        # Mover el cursor hasta la opción y seleccionarla
        ActionChains(self.driver).move_to_element(dropdown_option).perform()
        dropdown_option.click()

    def boton_siguiente(self):
        # Hacer clic en "Siguiente"
        next_button = self.wait_for_element(By.XPATH, "//button[.//span[text()='Siguiente']]")
        self.scroll_into_view(next_button)
        next_button.click()

        print("Formulario inicial completado")

    def validate_second_form(self):
        # Valida y completa el segundo formulario
        # Args: driver (webdriver): Instancia del navegador en uso.
        wait = WebDriverWait(self.driver, 10)  # Espera explícita hasta que el formulario esté listo para ser validado.
        self.enter_text(
            By.XPATH,
            "//div[contains(@class, 'slds-form-element__control')]//input[contains(@class, 'slds-input') and @type='text']",
            config.NOMBRE
        )  # Ingreso de datos en el formulario de los Nombres
        # Encuentra el elemento para "Primer Apellido"
       # Espera explícita hasta que el elemento esté presente en el DOM
        element = self.driver.find_element(By.XPATH,"//input[contains(@class, 'vlocity-input') and @placeholder='Primer Apellido']")
        # Forzar scroll al elemento
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        # Haz clic en el elemento (opcional para activarlo)
        ActionChains(self.driver).move_to_element(element).click().perform()
        # Ingresa el texto
        element.send_keys(config.PAPELLIDO)

        element = self.driver.find_element(By.XPATH, "//input[contains(@class, 'vlocity-input') and @placeholder='Segundo Apellido']")
        # Ingresa el texto
        element.send_keys(config.SAPELLIDO)

        element_email = self.driver.find_element(By.XPATH, "//input[@required and @placeholder='Correo electrónico']")
        element_email.send_keys(config.EMAIL)
        self.enter_text(
            By.XPATH,
            '//label[contains(normalize-space(.), "Ciudad o Municipio de residencia")]/following::input[1]',
            config.CIUDAD
        )
        dropdown_option = WebDriverWait(self.driver, 10).until(  # Selección de la ciudad (con una espera explícita)
            EC.visibility_of_element_located(
                (By.XPATH, "//span[contains(@class, 'slds-listbox__option-text') and text()='BOGOTA']")
            )
        )
        ActionChains(self.driver).move_to_element(dropdown_option).perform()  # Desplazarse al elemento
        dropdown_option.click()  # Selección de la opción       
        # Departamento
        hidden_field = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//label[normalize-space()="Departamento"]/following::input[1]')
            )
        )
        hidden_value = hidden_field.get_attribute("value")  # Obtener valor del campo oculto
        # País
        country_field = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//label[normalize-space()="País"]/following::input[1]')
            )
        )
        country_value = country_field.get_attribute("value")  # Obtener valor de país

        input_field = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//label[contains(normalize-space(), "Celular")]/following::input[1]')
            )
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
        self.driver.execute_script("arguments[0].click();", input_field)
        ActionChains(self.driver).move_to_element(input_field).click().send_keys(config.TELEFONO).perform()
        checkbox = WebDriverWait(self.driver, 20).until( # Marcar checkbox
            EC.element_to_be_clickable((By.XPATH, '//*[@class="slds-checkbox_faux"]'))
        )
        self.driver.execute_script("arguments[0].scrollIntoView();", checkbox)  # Desplaza el checkbox a la vista.
        ActionChains(self.driver).move_to_element(checkbox).click().perform()  # Mueve al checkbox y lo selecciona.

    def validate_second_form_email(self):
        # Valida y completa el segundo formulario
        # Args: driver (webdriver): Instancia del navegador en uso.
        wait = WebDriverWait(self.driver, 10)  # Espera explícita hasta que el formulario esté listo para ser validado.
        self.enter_text(
            By.XPATH,
            "//div[contains(@class, 'slds-form-element__control')]//input[contains(@class, 'slds-input') and @type='text']",
            config.NOMBRE
        )  # Ingreso de datos en el formulario de los Nombres
        # Encuentra el elemento para "Primer Apellido"
       # Espera explícita hasta que el elemento esté presente en el DOM
        element = self.driver.find_element(By.XPATH,"//input[contains(@class, 'vlocity-input') and @placeholder='Primer Apellido']")
        # Forzar scroll al elemento
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        # Haz clic en el elemento (opcional para activarlo)
        ActionChains(self.driver).move_to_element(element).click().perform()
        # Ingresa el texto
        element.send_keys(config.PAPELLIDO)

        element = self.driver.find_element(By.XPATH, "//input[contains(@class, 'vlocity-input') and @placeholder='Segundo Apellido']")
        # Ingresa el texto
        element.send_keys(config.SAPELLIDO)

        combobox_tipo = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'slds-combobox__form-element')]//input"))
        )

        combobox_tipo.click()

        #Esperar a que se despliegue la lista de opciones
        option_xpath = "//*[contains(@class, 'slds-listbox')]/descendant::*[contains(text(), 'CEDULA DE CIUDADANIA')]"

        option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, option_xpath))
        )

        #Hacer clic en la opción correcta
        option.click()

        # Generar e ingresar número de identificación aleatorio
        numero_identificacion = generar_identificacion_aleatoria()
        self.enter_text(By.XPATH,  "//input[@placeholder='Numero Documento' and @maxlength='11' and @minlength='7']", numero_identificacion)


        element_email = self.driver.find_element(By.XPATH, "//input[@required and @placeholder='Correo electrónico']")
        element_email.send_keys(config.EMAIL)

        self.enter_text(By.XPATH, '//*[@id="inputId-307"]', config.CIUDAD)  # Datos de la ciudad

        dropdown_option = WebDriverWait(self.driver, 10).until(  # Selección de la ciudad (con una espera explícita)
            EC.visibility_of_element_located(
                (By.XPATH, "//span[contains(@class, 'slds-listbox__option-text') and text()='BOGOTA']")
            )
        )
        ActionChains(self.driver).move_to_element(dropdown_option).perform()  # Desplazarse al elemento
        dropdown_option.click()  # Selección de la opción
        hidden_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="input25-311"]')))  # validar que el departamento sea el correcto
        hidden_value = hidden_field.get_attribute(config.DEPARTAMENTO)  # Obtener valor de un campo oculto
        country_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="input27-313"]'))) # validar que el pais sea el correcto
        country_value = country_field.get_attribute(config.PAIS)  # Obtener valor de país
        input_field = WebDriverWait(self.driver, 10).until(  # Espera explícita hasta que el campo de teléfono esté presente en el DOM.
            EC.presence_of_element_located((By.XPATH, '//*[@id="input33-319"]'))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)  # Desplaza el campo de teléfono a la vista.
        self.driver.execute_script("arguments[0].click();", input_field)  # Hace clic en el campo de teléfono para activarlo.
        ActionChains(self.driver).move_to_element(input_field).click().send_keys(config.TELEFONO).perform()  # Mueve al campo de teléfono, hace clic y envía el número de teléfono.
        self.enter_text(By.XPATH, '//*[@id="inputId-322"]', config.EVENTO) # Datos del evento
        dropdown_option = WebDriverWait(self.driver, 10).until(  # Selección del evento (esperar la opción visible y hacer clic)
            EC.visibility_of_element_located(
                (By.XPATH, "//span[contains(@class, 'slds-listbox__option-text') and text()='FERIA DEL LIBRO 2024']")
            )
        )
        ActionChains(self.driver).move_to_element(dropdown_option).perform()  # Desplaza el cursor hasta la opción del dropdown.
        dropdown_option.click()  # Hace clic en la opción del dropdown.
        checkbox = WebDriverWait(self.driver, 20).until( # Marcar checkbox
            EC.element_to_be_clickable((By.XPATH, '//*[@class="slds-checkbox_faux"]'))
        )
        self.driver.execute_script("arguments[0].scrollIntoView();", checkbox)  # Desplaza el checkbox a la vista.
        ActionChains(self.driver).move_to_element(checkbox).click().perform()  # Mueve al checkbox y lo selecciona.
        pass


    def boton_siguiente2(self):
        boton = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Guardar y continuar')]"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton)
        self.driver.execute_script("arguments[0].click();", boton)
        print("Validación Datos de contacto")
        pass
