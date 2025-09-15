from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # Manejo de esperas en Selenium
from selenium.webdriver.support import expected_conditions as EC # Condiciones de espera explícitas
import time
from config import config
from selenium.webdriver.common.action_chains import ActionChains  # Permite realizar interacciones avanzadas
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

class ProductoFormPage(BasePage):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)  # Inicializar `wait` correctamente

    def datos_producto(self):
        # 1) Abrir el combobox de Año
        wait = WebDriverWait(self.driver, 20)
        # 1) Hacer clic en el combobox
        combobox = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//button[@role='combobox' and @aria-label='Año de ingreso a cotizar']"
        )))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", combobox)
        combobox.click()
        print("📌 Combobox abierto")

        # 2) Esperar que aparezca el dropdown
        dropdown = wait.until(EC.presence_of_element_located((
            By.XPATH, "//div[@role='listbox' and contains(@id,'dropdown-element')]"
        )))
        print("📂 Dropdown desplegado")

        # 3) Seleccionar la opción 2038 (lightning-base-combobox-item)
        opcion_2038 = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//lightning-base-combobox-item[@data-value='2038']"
        )))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", opcion_2038)
        opcion_2038.click()
        print("✅ Año 2038 seleccionado")
        time.sleep(2)
        try:
        # 1) Esperar a que el input después de la etiqueta "Observaciones" sea clickeable
            input_observaciones = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//label[normalize-space(text())='Observaciones']/following::input[1]"
                ))
            )

            # 2) Scroll al campo
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_observaciones)

            # 3) Clic en el campo
            input_observaciones.click()
            print("✅ Se hizo clic en Observaciones")

            # 4) Limpiar por si tiene texto previo
            input_observaciones.clear()

            # 5) Ingresar el texto "Ninguno"
            input_observaciones.send_keys("Ninguno")
            print("✍️ Texto 'Ninguno' ingresado")
        except Exception as e:
            print(f"❌ Error al interactuar con Observaciones: {e}")

    pass

    def lista_producto(self):
        wait = WebDriverWait(self.driver, 30)

        # Buscar el input asociado al label 'Producto'
        producto = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//label[normalize-space(text())='Producto']/following::input[1]"
        )))
        return producto


    def seleccionar_tarifa_septiembre(self, timeout=20):
        w = WebDriverWait(self.driver, timeout)
        # 1) Tomar el combobox que corresponde al label "Tarifa"
        container = w.until(EC.presence_of_element_located((
            By.XPATH, "//label[.//span[normalize-space()='Tarifa']]/ancestor::div[contains(@class,'slds-combobox')][1]"
        )))
        # 2) Abrir el dropdown (input o ícono ▼ del mismo combobox)
        try:
            opener = container.find_element(By.XPATH, ".//input[@role='combobox']")
        except Exception:
            opener = container.find_element(By.XPATH, ".//span[contains(@class,'slds-input__icon_right')]")
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", opener)
        self.driver.execute_script("arguments[0].click();", opener)
        # 3) Esperar el listbox de ese mismo combobox
        w.until(lambda d: container.find_element(By.XPATH, ".//div[@role='listbox']").is_displayed())
        listbox = container.find_element(By.XPATH, ".//div[@role='listbox']")
        # 4) Click en "Septiembre" dentro del listbox
        try:
            opcion = listbox.find_element(By.XPATH, ".//div[@role='option' and @data-label='Septiembre']")
        except Exception:
            opcion = listbox.find_element(By.XPATH, ".//span[normalize-space()='Septiembre']/ancestor::div[@role='option']")
        self.driver.execute_script("arguments[0].click();", opcion)   

    def lista_asegurado(self):
        wait = WebDriverWait(self.driver, 30)  # Definir WebDriverWait correctamente
        asegurado = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[1]/section/div[1]/div[2]/div[2]/div[1]/div/div/div/div/div/c-gsv-tvs-perfilador-educativo-english/div/article/div[2]/vlocity_ins-omniscript-step[4]/div[3]/slot/vlocity_ins-omniscript-block/div/div/section/fieldset/slot/vlocity_ins-omniscript-select[15]/slot/c-combobox/div/div/div[2]/div[1]/div/input")))
        self.driver.execute_script("arguments[0].scrollIntoView();", asegurado)
        asegurado.click()  
        asegurado.send_keys(config.VALOR_ASEGURADO)  # Ingresa el texto "1.000.000" en el campo de texto.
        # Selección de la opción en el desplegable (espera explícita)
        valor_asegu_option = wait.until(EC.visibility_of_element_located(
        (
            By.XPATH, "//span[contains(@class, 'slds-listbox__option-text') and text()='5.000.000']")
        ))  # Espera hasta que la opción "0 a 4.000.000" sea visible.
        ActionChains(self.driver).move_to_element(valor_asegu_option).perform()  # Desplaza el mouse sobre la opción.
        valor_asegu_option.click()  # Hace clic en la opción seleccionada.
        return asegurado
    

    def datos_producto_segura_plus(self):
        producto_elemento = self.lista_producto()          
        self.driver.execute_script("arguments[0].scrollIntoView();", producto_elemento)
        time.sleep(5)
        # Esperar a que aparezca la opción "Global Universidad Segura Plus"
        producto_elemento = self.lista_producto()
        # Mover el cursor sobre la opción y hacer clic en ella
        actions = ActionChains(self.driver)
        self.driver.execute_script("arguments[0].scrollIntoView();", producto_elemento)
        actions.move_to_element(producto_elemento).pause(1).click().perform()
        time.sleep(5)
         # Presiona ARROW_DOWN para moverse a la segunda opción
        for _ in range(1):  # Repite 4 veces
            producto_elemento.send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
        producto_elemento.send_keys(Keys.ENTER)  # Seleccionar la opción
        #MES
        self.seleccionar_tarifa_septiembre()
        time.sleep(5)
        #asegurado
        producto_asegurado = self.lista_asegurado()
        # Mover el cursor sobre la opción y hacer clic en ella
        
        time.sleep(7)
    pass

    def datos_producto_segura_plus_semestre(self):
        time.sleep(10)
        producto_elemento = self.lista_producto()          
        self.driver.execute_script("arguments[0].scrollIntoView();", producto_elemento)
        time.sleep(5)
        # Esperar a que aparezca la opción "Global Universidad Segura Plus"clear
        actions = ActionChains(self.driver)
        actions.move_to_element(producto_elemento).pause(1).click().perform()
        time.sleep(5)
         # Presiona ARROW_DOWN para moverse a la segunda opción
        for _ in range(1):  # Repite 4 veces
            producto_elemento.send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
        producto_elemento.send_keys(Keys.ENTER)  # Seleccionar la opción
        #MES
        producto_mes = self.seleccionar_tarifa_septiembre()

        # Mover el cursor sobre la opción y hacer clic en ella
        actions = ActionChains(self.driver)
        self.driver.execute_script("arguments[0].scrollIntoView();", producto_mes)
        actions.move_to_element(producto_mes).pause(1).click().perform()
        producto_mes.send_keys(Keys.ENTER)  # Seleccionar la opción
        time.sleep(5)
        #asegurado
        wait = WebDriverWait(self.driver, 30)  # Espera hasta 10 segundos
        valor_asegu = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[1]/section/div[1]/div[2]/div[2]/div[1]/div/div/div/div/div/c-gsv-tvs-perfilador-educativo-english/div/article/div[2]/vlocity_ins-omniscript-step[4]/div[3]/slot/vlocity_ins-omniscript-block/div/div/section/fieldset/slot/vlocity_ins-omniscript-select[15]/slot/c-combobox/div/div/div[2]/div[1]/div/input")))  
        self.driver.execute_script("arguments[0].scrollIntoView();", valor_asegu)
        valor_asegu.click()  
        valor_asegu.send_keys(config.VALOR_ASEGURADO)  # Ingresa el texto "1.000.000" en el campo de texto.
        # Selección de la opción en el desplegable (espera explícita)
        valor_asegu_option = wait.until(EC.visibility_of_element_located(
        (
            By.XPATH, "//span[contains(@class, 'slds-listbox__option-text') and text()='5.000.000']")
        ))  # Espera hasta que la opción "0 a 4.000.000" sea visible.
        ActionChains(self.driver).move_to_element(valor_asegu_option).perform()  # Desplaza el mouse sobre la opción.
        valor_asegu_option.click()  # Hace clic en la opción seleccionada.
        time.sleep(7)
        # XPath del combo box (campo de entrada)
        semestre_xpath = "/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/c-gsv-tvs-perfilador-educativo-english[1]/div[1]/article[1]/div[2]/vlocity_ins-omniscript-step[4]/div[3]/slot[1]/vlocity_ins-omniscript-block[1]/div[1]/div[1]/section[1]/fieldset[1]/slot[1]/vlocity_ins-omniscript-select[16]/slot[1]/c-combobox[1]/div[1]/div[1]/div[2]/div[1]/div[1]/input[1]"
        # XPath de la opción con el valor '6'
        # Esperar que el combo box sea clickeable y hacer clic
        combobox_element = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, semestre_xpath))
        )
        combobox_element.click()
        print("Combo box abierto.")
        # Esperar que la opción 6 sea visible y hacer clic
        time.sleep(2)  # Pequeña espera para que carguen las opciones
        # Presiona ARROW_DOWN para moverse a la segunda opción
        for _ in range(6):  # Repite 6 veces
            combobox_element.send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
        combobox_element.send_keys(Keys.ENTER)  # Seleccionar la opción
        time.sleep(7)  # Esperar para ver si el clic se procesó correctamente
        print("Opción 6 seleccionada.")
    pass

    def datos_producto_gmprofesional(self):
        wait = WebDriverWait(self.driver, 30)  # Espera hasta 10 segundos
        producto_elemento = self.lista_producto()          
        self.driver.execute_script("arguments[0].scrollIntoView();", producto_elemento)
        time.sleep(5)
        # Esperar a que aparezca la opción "Global Universidad Segura Plus"
        producto_elemento = self.lista_producto()
        # Mover el cursor sobre la opción y hacer clic en ella
        actions = ActionChains(self.driver)
        self.driver.execute_script("arguments[0].scrollIntoView();", producto_elemento)
        actions.move_to_element(producto_elemento).pause(1).click().perform()
        time.sleep(5)
         # Presiona ARROW_DOWN para moverse a la segunda opción
        for _ in range(1):  # Repite 4 veces
            producto_elemento.send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
        producto_elemento.send_keys(Keys.ENTER)  # Seleccionar la opción
        #MES
        wait = WebDriverWait(self.driver, 30)  # Espera hasta 10 segundos
        tarifa = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[1]/section/div[1]/div[2]/div[2]/div[1]/div/div/div/div/div/c-gsv-tvs-perfilador-educativo-english/div/article/div[2]/vlocity_ins-omniscript-step[4]/div[3]/slot/vlocity_ins-omniscript-block/div/div/section/fieldset/slot/vlocity_ins-omniscript-select[8]/slot/c-combobox/div/div/div[2]/div[1]/div/input")))
        self.driver.execute_script("arguments[0].click();", tarifa)
        tarifa.clear()
        tarifa.send_keys(config.MES_TARIFA)
        tarifa.send_keys(Keys.RETURN)  # Simula presionar Enter
        tarifa_option = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[1]/section/div[1]/div[2]/div[2]/div[1]/div/div/div/div/div/c-gsv-tvs-perfilador-educativo-english/div/article/div[2]/vlocity_ins-omniscript-step[4]/div[3]/slot/vlocity_ins-omniscript-block/div/div/section/fieldset/slot/vlocity_ins-omniscript-select[8]/slot/c-combobox/div/div/div[2]/div[2]/div/ul/li[2]/div/span/span")))
        ActionChains(self.driver).move_to_element(tarifa_option).click().perform()
        time.sleep(5)
        #asegurado
        valor_asegu = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[1]/section/div[1]/div[2]/div[2]/div[1]/div/div/div/div/div/c-gsv-tvs-perfilador-educativo-english/div/article/div[2]/vlocity_ins-omniscript-step[4]/div[3]/slot/vlocity_ins-omniscript-block/div/div/section/fieldset/slot/vlocity_ins-omniscript-select[15]/slot/c-combobox/div/div/div[2]/div[1]/div/input")))  
        self.driver.execute_script("arguments[0].scrollIntoView();", valor_asegu)
        valor_asegu.click()  
        valor_asegu.send_keys(config.VALOR_ASEGURADO2)  # Ingresa el texto "1.000.000" en el campo de texto.
        # Selección de la opción en el desplegable (espera explícita)
        valor_asegu_option = wait.until(EC.visibility_of_element_located(
        (
            By.XPATH, "//span[contains(@class, 'slds-listbox__option-text') and text()='2.000.000']")
        ))  # Espera hasta que la opción "0 a 4.000.000" sea visible.
        ActionChains(self.driver).move_to_element(valor_asegu_option).perform()  # Desplaza el mouse sobre la opción.
        valor_asegu_option.click()  # Hace clic en la opción seleccionada.
        time.sleep(5)
        año_xpath = "/html/body/div[4]/div[1]/section/div[1]/div[2]/div[2]/div[1]/div/div/div/div/div/c-gsv-tvs-perfilador-educativo-english/div/article/div[2]/vlocity_ins-omniscript-step[4]/div[3]/slot/vlocity_ins-omniscript-block/div/div/section/fieldset/slot/vlocity_ins-omniscript-custom-lwc[2]/slot/c-gsv-custom-num-year-prof/lightning-combobox/div/div[1]/lightning-base-combobox/div/div/div[1]/button"
        # XPath de la opción con el valor '6'
        # Esperar que el combo box sea clickeable y hacer clic
        combobox_element = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, año_xpath))
        )
        combobox_element.click()
        print("Combo box abierto.")
        # Esperar que la opción 6 sea visible y hacer clic
        time.sleep(2)  # Pequeña espera para que carguen las opciones
        # Presiona ARROW_DOWN para moverse a la segunda opción
        for _ in range(6):  # Repite 6 veces
            combobox_element.send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
        combobox_element.send_keys(Keys.ENTER)  # Seleccionar la opción
        time.sleep(3)  # Esperar para ver si el clic se procesó correctamente
        print("Opción 6 seleccionada.")
        per_xpath = "/html/body/div[4]/div[1]/section/div[1]/div[2]/div[2]/div[1]/div/div/div/div/div/c-gsv-tvs-perfilador-educativo-english/div/article/div[2]/vlocity_ins-omniscript-step[4]/div[3]/slot/vlocity_ins-omniscript-block/div/div/section/fieldset/slot/vlocity_ins-omniscript-select[18]/slot/c-combobox/div/div/div[2]/div[1]/div/input"
        # XPath de la opción con el valor '6'
        # Esperar que el combo box sea clickeable y hacer clic
        combobox_element = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, per_xpath))
        )
        combobox_element.click()
        print("Combo box abierto.")
        # Esperar que la opción 6 sea visible y hacer clic
        time.sleep(3)  # Pequeña espera para que carguen las opciones
        # Presiona ARROW_DOWN para moverse a la segunda opción
        for _ in range(6):  # Repite 6 veces
            combobox_element.send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
        combobox_element.send_keys(Keys.ENTER)  # Seleccionar la opción
        time.sleep(7)  # Esperar para ver si el clic se procesó correctamente
        print("Opción 6 seleccionada.")
    pass

    def simulador_producto_segura_plus(self):
        title_xpath = "//*[contains(text(), 'Valor asegurado semestre')]"  # XPath flexible para cualquier etiqueta que contenga este texto
        # Esperar hasta que el título sea visible
        titulo = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, title_xpath))
        )
        # Validar que el texto sea el esperado
        assert titulo.text.strip() == "Valor asegurado semestre", "El título no coincide"
        print("El título 'Valor asegurado semestre' está presente.")
        time.sleep(5)
        print("Combo box revisado.")
        time.sleep(10)
        texto_xpath = "//*[contains(text(), '$ 0,00')]"  # Busca cualquier etiqueta que contenga el texto exacto
        # Esperar hasta que el texto sea visible en la página
        print("El texto '$ 0,00' está presente en la página.")
        time.sleep(7)
        pass

    def simulador_producto_segura_plus_semestre(self):
        title_xpath = "//*[contains(text(), 'GlobalUniversidad Segura Plus Semestres')]"  # XPath flexible para cualquier etiqueta que contenga este texto
        # Esperar hasta que el título sea visible
        titulo = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, title_xpath))
        )
        # Validar que el texto sea el esperado
        assert titulo.text.strip() == "GlobalUniversidad Segura Plus Semestres", "El título no coincide"
        print("El título 'GlobalUniversidad Segura Plus Semestres' está presente.")
        time.sleep(5)
        combobox_xpath = "//input[contains(@class, 'slds-input') and @role='combobox']"
        # XPath de la opción con el valor '2000000'
        option_xpath = "//span[contains(@class, 'slds-listbox__option-text') and text()='3.000.000']"

        # Esperar que el combo box sea clickeable y hacer clic
        combobox_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, combobox_xpath))
        )
        combobox_element.click()
        print("Combo box abierto.")

        # Esperar que la opción de 5,000,000 esté visible y hacer clic
        option_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, option_xpath))
        )
        option_element.click()
        print("Seleccionada la opción 3000000.")
        time.sleep(5)
        texto_xpath = "//*[contains(text(), '$ 14.538.000,00')]"  # Busca cualquier etiqueta que contenga el texto exacto
        # Esperar hasta que el texto sea visible en la página
        print("El texto '$ 14.538.000,00' está presente en la página.")
        time.sleep(5)
        pass

    def simulador_producto_gmprofesional(self):
        wait = WebDriverWait(self.driver, 10)  # Espera hasta 10 segundos
        # Primer combo box y opción
        combobox_xpath = "//input[contains(@class, 'slds-input') and @role='combobox']"
        option_xpath = f"//span[contains(@class, 'slds-listbox__option-text') and text()='3.000.000']"
        # Esperar que el combo box sea clickeable y hacer clic
        combobox_element = wait.until(EC.element_to_be_clickable((By.XPATH, combobox_xpath)))
        combobox_element.click()
        print("Primer combo box abierto.")
        # Esperar que la opción esté disponible y hacer clic
        option_element = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        option_element.click()
        print(f"Seleccionada la opción $ 3.000.000.")
        time.sleep(2)  # Pequeña pausa para asegurar que se cierre
        # Segundo combo box y opción
        comboboxa_xpath = "/html/body/div[4]/div[1]/section/div[1]/div[2]/div[2]/div[1]/div/div/div/div/div/c-gsv-tvs-perfilador-educativo-english/div/article/div[2]/vlocity_ins-omniscript-step[5]/div[3]/slot/vlocity_ins-omniscript-custom-lwc/slot/vlocity_ins-ins-os-single-instance/c-ins-os-coverage-list/div/c-ins-os-coverage/article/div[2]/c-ins-attribute-category/div/div/div[6]/div/c-ins-attribute/div/div[2]/c-combobox/div/div/div[2]/div[1]/div/input"
        optiona_xpath = "//span[contains(@class, 'slds-listbox__option-text') and text()='3']"
        # Esperar que el segundo combo box sea clickeable y hacer clic
        comboboxA_element = wait.until(EC.element_to_be_clickable((By.XPATH, comboboxa_xpath)))
        comboboxA_element.click()
        print("Segundo combo box abierto.")
        # Esperar que la opción esté disponible y hacer clic
        optiona_element = wait.until(EC.element_to_be_clickable((By.XPATH, optiona_xpath)))
        optiona_element.click()
        print("Opción 3 seleccionada.")
        time.sleep(5)
        comboboxp_xpath = "/html/body/div[4]/div[1]/section/div[1]/div[2]/div[2]/div[1]/div/div/div/div/div/c-gsv-tvs-perfilador-educativo-english/div/article/div[2]/vlocity_ins-omniscript-step[5]/div[3]/slot/vlocity_ins-omniscript-custom-lwc/slot/vlocity_ins-ins-os-single-instance/c-ins-os-coverage-list/div/c-ins-os-coverage/article/div[2]/c-ins-attribute-category/div/div/div[7]/div/c-ins-attribute/div/div[2]/c-combobox/div/div/div[2]/div[1]/div/input"
        # XPath de la opción con el valor '2000000'
        optionp_xpath = "//span[contains(@class, 'slds-listbox__option-text') and text()='Trimestral']"
        # Esperar que el combo box sea clickeable y hacer clic
        comboboxp_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, comboboxp_xpath))
        )
        comboboxp_element.click()
        print("Combo box abierto.")
        # Esperar que la opción de 5,000,000 esté visible y hacer clic
        optionp_xpath = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, optionp_xpath))
        )
        optionp_xpath.click()
        print("Seleccionada la opción Trimestral.")
        time.sleep(5)
        pass

    def button_cotizar(self):
        button_xpath = "//button[span[text()='Cotizar']]"  # XPath basado en el texto del botón
        # Esperar hasta que el botón sea visible en la página
        button_element = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, button_xpath))
        )
        # Hacer scroll hasta el botón usando el elemento correcto
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button_element)
        # Esperar que sea clickeable y hacer clic
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_xpath))).click()
        print("Botón 'Cotizar' clickeado con éxito.")
        time.sleep(20)
        pass

    def boton_atras(self):
        # XPath basado en el texto dentro del botón
        boton_atras_xpath = "//button[span[text()='Atras']]"
        # Esperar hasta que el botón sea visible y clickeable
        boton_atras = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, boton_atras_xpath))
        )
        # Hacer scroll hasta el botón para asegurarse de que sea visible
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", boton_atras)
        # Hacer clic en el botón "Anterior"
        boton_atras.click()
        print("Botón 'Anterior' clickeado correctamente.")
    pass

    def boton_anterior(self):
        boton_anterior_xpath = "//button[span[text()='Anterior']]"
        boton_atras = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, boton_anterior_xpath))
        )
        
        # Scroll al botón usando el elemento real, no el string del XPath
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", boton_atras)
        
        # Click directamente sobre el elemento encontrado
        boton_atras.click()
        print("Botón 'Anterior' clickeado con éxito.")
        time.sleep(20)
    pass

    def button_finalizar(self):
        button_xpath = "//button[span[text()='Finalizar']]"  # XPath basado en el texto del botón
        # Esperar hasta que el botón sea visible en la página
        button_element = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, button_xpath))
        )
        # Hacer scroll hasta el botón usando el elemento correcto
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button_element)
        # Esperar que sea clickeable y hacer clic
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_xpath))).click()
        print("Botón 'Finalizar' clickeado con éxito.")
        time.sleep(20)
        pass