from pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # Manejo de esperas en Selenium
from selenium.webdriver.support import expected_conditions as EC # Condiciones de espera explícitas
import time
from config import config
from utils.helpers import generar_nombre_completo
from utils.helpers import generar_identificacion_aleatoria
from selenium.webdriver.common.action_chains import ActionChains  # Permite realizar interacciones avanzadas

class CotizarFormPage(BasePage):
    def datos_asegurado(self):
        boton_continuar = WebDriverWait(self.driver, 25).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Guardar y continuar']]"))
        )
        # Hacer scroll hasta el botón
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_continuar)
        # Mover el cursor al botón y hacer clic
        ActionChains(self.driver).move_to_element(boton_continuar).click().perform()
        pass

    def datos_beneficiario(self):
        # Generar datos aleatorios
        nombre, apellido1, apellido2 = generar_nombre_completo()
        numero= generar_identificacion_aleatoria()
        print(f"Ingresando: {nombre} {apellido1} {apellido2}")

        # Esperar 2 segundos antes de buscar los elementos
        time.sleep(2)

        # Buscar los campos por su placeholder
        campo_nombre = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Nombres completos']"))
        )
        time.sleep(1)  # Espera antes de escribir
        campo_nombre.click()
        campo_nombre.send_keys(nombre)
        time.sleep(1)
     
        # Esperar hasta que el campo sea interactivo
        campo_apellido1 = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Primer Apellido']"))
        )
        
        time.sleep(1)  # Pausa opcional para evitar problemas

        campo_apellido1.send_keys(apellido1)  # Ingresar apellido
        time.sleep(1)

        campo_apellido2 = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Segundo Apellido']"))
        )
        
        time.sleep(1)  # Pausa opcional para evitar problemas

        campo_apellido2.send_keys(apellido2)  #
        time.sleep(1)
        combobox_tipo = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'slds-combobox__form-element')]//input"))
        )

        combobox_tipo.click()

        #Esperar a que se despliegue la lista de opciones
        option_xpath = "//*[contains(@class, 'slds-listbox')]/descendant::*[contains(text(), 'Tarjeta de Identidad')]"

        option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, option_xpath))
        )

        #Hacer clic en la opción correcta
        option.click()
        time.sleep(2)
        campo_numero = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Ingresar número']"))
        )
        time.sleep(1)  # Pequeña pausa
        campo_numero.send_keys(str(numero))  # Ingresar número
        time.sleep(1)  # Pequeña pausa
        campo_fecha = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Fecha de Nacimiento']"))
        )
        time.sleep(1)  # Pequeña pausa
        campo_fecha.send_keys('18-02-2020')  # Ingresa la fecha manualmente (por ejemplo, 01/18/1970).
        wait = WebDriverWait(self.driver, 20)
        # 1️⃣ Espera que el label 'Sexo' esté presente
        label_sexo = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//label[contains(@for, "comboboxId") and .//span[text()="Sexo"]]')))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", label_sexo)
        time.sleep(1)

        input_xpath = '//label[.//span[text()="Sexo"]]/ancestor::div[contains(@class, "slds-form-element")]/descendant::input[@role="combobox"]'
        dropdown_input = wait.until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
        dropdown_input.click()
        time.sleep(1)

        # 3️⃣ Espera la apertura de la lista y selecciona "Femenino" con data-label
        option_femenino = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//div[@role="option" and @data-label="Femenino"]'))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option_femenino)
        option_femenino.click()

        time.sleep(10)  # Pequeña pausa
            
    def boton_guardar(self):
        wait = WebDriverWait(self.driver, 20)
        boton_guardar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Guardar y continuar']]")))

        # Hacer scroll hasta el botón
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", boton_guardar)

        # Pequeña pausa para que la animación termine
        time.sleep(1)

        # Usar ActionChains para hacer clic
        ActionChains(self.driver).move_to_element(boton_guardar).click().perform()

        # Otra pausa corta si es necesario antes de continuar con otros pasos
        time.sleep(10)
        print("Validación Información beneficiario")
        pass

    def button_regresar(self):
        boton_anterior = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='button-container']/button[1]"))
        )
        boton_anterior.click()  
        pass

    def datos_colegio(self):
        # Ingresar texto en el campo del colegio
        self.enter_text(
            By.XPATH,
            "//input[contains(@class, 'slds-input') and @role='combobox' and contains(@aria-autocomplete, 'list')]",
            config.COLEGIO  # Variable con el nombre del colegio a buscar
        )
        # Esperar y seleccionar la opción en el dropdown
        opcion_colegio = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@role="option" and contains(.//span, "COLEGIO CALENDARIO A COTIZACION")]')  # Ajusta el texto al colegio correcto
            )
        )
        # Mover el cursor hasta la opción y seleccionarla
        ActionChains(self.driver).move_to_element(opcion_colegio).perform()
        opcion_colegio.click()
        time.sleep(2)
        icono_editar = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//c-icon[.//span[text()="Edit"]]')
            )
        )
        # Crear la acción de clic
        action = ActionChains(self.driver)
        # Hacer el primer clic
        action.move_to_element(icono_editar).click().perform()
        # Pausa breve antes del segundo clic
        time.sleep(2)  # Ajusta el tiempo si es necesario
        # Hacer el segundo clic
        action.move_to_element(icono_editar).click().perform()
        time.sleep(2)  # Ajusta el tiempo si es necesario
        # Esperar a que el input del combobox esté presente y hacer clic en el ícono para expandirlo
        campo_icono = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(@class, "slds-icon_container")]'))
        )
        campo_icono.click()

        # Hacer clic en el ícono del combobox para desplegar las opciones
        campo_icono = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(@class, "slds-icon_container")]'))
        )
        self.driver.execute_script("arguments[0].click();", campo_icono)  # Click forzado con JS
        # Espera hasta que el combobox sea visible y clickeable
        wait = WebDriverWait(self.driver, 20)
        # Esperar a que el input del combobox esté presente y hacer clic
        # Encuentra el input asociado al label 'Curso'
        combobox_input = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//input[@role='combobox' and @aria-haspopup='listbox']"
        )))
        combobox_input.click()
        print("📌 Combobox abierto")

        option_prekinder = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//span[normalize-space()='Prekinder']"
        )))
        option_prekinder.click()
        print("✅ Prekinder seleccionado correctamente")
        pass  