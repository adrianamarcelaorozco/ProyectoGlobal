from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # Manejo de esperas en Selenium
from selenium.webdriver.support import expected_conditions as EC # Condiciones de espera explícitas
import time
from config import config
from selenium.webdriver.common.action_chains import ActionChains  # Permite realizar interacciones avanzadas
from selenium.webdriver.common.keys import Keys

class PersonalFormPage(BasePage):
    def personal_form_mayor(self):
        self.enter_text(By.XPATH, "//input[@data-id='date-picker-slds-input']", '12/28/1984') # Ingresar la fecha en el campo de fecha usando el input de tipo date
        # Haz clic en el combobox
        wait = WebDriverWait(self.driver, 15)
        # Espera hasta que el label "Sexo" esté presente
        label_sexo = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//label[@for="comboboxId-387" and contains(., "Sexo")]')
        ))
        # Scroll al label
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", label_sexo)
        time.sleep(1)  # Espera que la animación termine (por si hay transiciones de Salesforce)        
        #Encuentra el input que está cerca del label "Sexo"
        dropdown_input = self.driver.find_element(By.XPATH, '//*[@id="comboboxId-387"]')  
        dropdown_input.click()
        time.sleep(2)
        wait = WebDriverWait(self.driver, 10)  # Configura la espera explícita para el siguiente paso.
        M_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@role="option" and .//span[text()="Masculino"]]')))  # Espera hasta que la opción "01" sea clickeable.
        M_option.click()  # Hace clic en la opción "01"
        #dropdown_input.send_keys('Masculino')
        time.sleep(1)  # Deja que se rendericen las opciones
        # 4️⃣ Seleccionar opción "Masculino"
        radio = self.wait_for_element(By.XPATH, "//input[@type='radio' and @value='Pareja con hijos menores de edad']")  # Espera hasta que el radio button sea visible.
        self.driver.execute_script("arguments[0].click();", radio)  # Usa Javascript para hacer clic en el radio button.
        dropdown = self.driver.find_element(By.XPATH, '//*[@id="comboboxId-412"]')  # Encuentra el dropdown.
        self.driver.execute_script("arguments[0].scrollIntoView();", dropdown)  # Desplaza el dropdown a la vista si es necesario.
        dropdown.click()  # Hace clic para desplegar las opciones del dropdown.
        wait = WebDriverWait(self.driver, 10)  # Configura la espera explícita para el siguiente paso.
        one_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@role="option" and .//span[text()="01"]]')))  # Espera hasta que la opción "01" sea clickeable.
        one_option.click()  # Hace clic en la opción "01".
        time.sleep(5)  # Pausa de 2 segundos para garantizar que la acción se complete.
        self.enter_text(By.XPATH, '/html/body/div[4]/div[1]/section/div[1]/div[2]/div[2]/div[1]/div/div/div/div/div/c-gsv-formulary-english/div/article/div[2]/vlocity_ins-omniscript-step[5]/div[3]/slot/vlocity_ins-omniscript-block/div/div/section/fieldset/slot/vlocity_ins-omniscript-block[1]/div/div/section/fieldset/slot/vlocity_ins-omniscript-text[1]/slot/c-input/div/div[2]/input', config.NOMBRED)  # Ingresa el nombre en el campo correspondiente.
        self.enter_text(By.XPATH, '/html/body/div[4]/div[1]/section/div[1]/div[2]/div[2]/div[1]/div/div/div/div/div/c-gsv-formulary-english/div/article/div[2]/vlocity_ins-omniscript-step[5]/div[3]/slot/vlocity_ins-omniscript-block/div/div/section/fieldset/slot/vlocity_ins-omniscript-block[1]/div/div/section/fieldset/slot/vlocity_ins-omniscript-text[2]/slot/c-input/div/div[2]/input', config.PAPELLIDOD)  # Ingresa el primer apellido en el campo correspondiente.
        self.enter_text(By.XPATH, '/html/body/div[4]/div[1]/section/div[1]/div[2]/div[2]/div[1]/div/div/div/div/div/c-gsv-formulary-english/div/article/div[2]/vlocity_ins-omniscript-step[5]/div[3]/slot/vlocity_ins-omniscript-block/div/div/section/fieldset/slot/vlocity_ins-omniscript-block[1]/div/div/section/fieldset/slot/vlocity_ins-omniscript-text[3]/slot/c-input/div/div[2]/input', config.SAPELLIDOD)  # Ingresa el segundo apellido en el campo correspondiente.
        time.sleep(5)
        dropdown_input_h = self.driver.find_element(By.XPATH, '//*[@id="comboboxId-426"]')  
        dropdown_input_h.click()
        time.sleep(2)
        wait = WebDriverWait(self.driver, 10)  # Configura la espera explícita para el siguiente paso.
        H_option = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@role="option" and .//span[text()="Hijo/a"]]')))  # Espera hasta que la opción "01" sea clickeable.
        H_option.click()  # Hace clic en la opción "01"
        #dropdown_input.send_keys('Masculino')
        time.sleep(1)  # Deja que se rendericen las opciones
        date_input = self.driver.find_element(By.XPATH, '//*[@id="date-input-430"]')  # Encuentra el campo de fecha.
        date_input.send_keys('01/18/1970')  # Ingresa la fecha manualmente (por ejemplo, 01/18/1970).
        pass

    def boton_guardar(self):
        save_button = self.wait_for_element(By.XPATH, '//button[contains(text(), "Guardar y continuar")]')  # Espera hasta que el botón esté visible.
        self.driver.execute_script("arguments[0].scrollIntoView();", save_button)  # Desplaza el dropdown a la vista si es necesario.
        # Desplaza el botón a la vista si no está visible.
        save_button.click()  # Hace clic en el botón para continuar.
        time.sleep(5)  # Espera 5 segundos para asegurar que la acción se haya completado.
        print("Validación Información Personal")
        pass


    def personal_form_menor(self):
        self.enter_text(By.XPATH, "//input[@aria-label='Fecha de Nacimiento']", "12/28/1992")# Ingresar la fecha en el campo de fecha usando el input de tipo date
        # Espera a que el combobox esté clickeable
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@role='combobox' and contains(@class,'slds-listbox__option-text_entity')]"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
        dropdown.click()
        # Espera a que la opción "Masculino" esté clickeable y haz clic
        option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='option' and @data-value='Masculino']"))
        )
        option.click()
        time.sleep(2)  # Pausa de 2 segundos para garantizar la interacción completa.
        radio_label = self.wait_for_element(
        By.XPATH,
        "//label[@class='slds-radio__label' and contains(., 'Pareja con hijos')]"
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", radio_label)
        self.driver.execute_script("arguments[0].click();", radio_label)
        # Hacer clic SOLO en el combobox que tiene el label "¿Cuántas personas dependen de ti?"
        combobox = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//label[span[normalize-space()='¿Cuántas personas dependen de ti?']]/following::input[@role='combobox'][1]"
            ))
        )
        combobox.click()

        # Esperar a que aparezca alguna opción dentro de ese mismo bloque
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//label[span[normalize-space()='¿Cuántas personas dependen de ti?']]/ancestor::div[contains(@class,'slds-combobox')]" +
                "//div[@role='option']"
            ))
        )

        # Seleccionar la opción '01' dentro de ese mismo bloque
        one_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//label[span[normalize-space()='¿Cuántas personas dependen de ti?']]/ancestor::div[contains(@class,'slds-combobox')]" +
                "//div[@role='option']//span[normalize-space()='01']"
            ))
        )
        one_option.click()

        time.sleep(5)  # Pausa de 2 segundos para garantizar que la acción se complete.
        self.enter_text(
            By.XPATH,
            "//label[span[normalize-space(text())='Nombres']]/following::input[contains(@class,'vlocity-input')][1]",
            config.NOMBRED
        )        
        self.enter_text(
        By.XPATH,
        "//label[span[normalize-space(text())='Primer Apellido']]/following::input[contains(@class,'vlocity-input')][1]",
        config.PAPELLIDO
        )
        self.enter_text(
            By.XPATH,
            "//label[span[normalize-space(text())='Segundo Apellido']]/following::input[contains(@class,'vlocity-input')][1]",
            config.SAPELLIDO
        )
        time.sleep(5)
      # Hacer clic en el combobox que tiene el label "Parentesco"
        combobox_parentesco = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//label[span[normalize-space()='Parentesco']]/following::input[@role='combobox'][1]"
            ))
        )
        combobox_parentesco.click()

        # Esperar a que se muestren las opciones (del mismo combobox)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//label[span[normalize-space()='Parentesco']]/ancestor::div[contains(@class,'slds-combobox')]//div[@role='option']"
            ))
        )
        # Seleccionar la opción 'Hijo/a' dentro del mismo bloque
        option_hijo = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//label[span[normalize-space()='Parentesco']]/ancestor::div[contains(@class,'slds-combobox')]//div[@role='option']//span[normalize-space()='Hijo/a']"
            ))
        )
        option_hijo.click()
        # Localizar el INPUT asociado al label "Fecha de nacimiento"
        date_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//label[normalize-space()='Fecha de nacimiento']/following::input[@type='text'][1]"
            ))
        )

        date_input.clear()
        date_input.send_keys('01/18/2020')
        date_input.send_keys(Keys.TAB)   # Para que el datepicker se cierre (opcional)
        time.sleep(10)  # Pausa de 2 segundos para garantizar la interacción completa.
       # 1. Hacer clic en el combobox asociado al label "Grado de escolaridad actual del dependiente"
        combobox_escolaridad = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//label[span[normalize-space()='Grado de escolaridad actual del dependiente']]/following::input[@role='combobox'][1]"
            ))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", combobox_escolaridad)
        combobox_escolaridad.click()

        # 2. Esperar a que aparezcan las opciones dentro de ese mismo bloque
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//label[span[normalize-space()='Grado de escolaridad actual del dependiente']]" +
                "/ancestor::div[contains(@class,'slds-combobox')]//div[@role='option']"
            ))
        )

        # 3. Hacer clic sobre la opción "Primero"
        opcion_primero = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//label[span[normalize-space()='Grado de escolaridad actual del dependiente']]" +
                "/ancestor::div[contains(@class,'slds-combobox')]//div[@role='option']//span[normalize-space()='Primero']"
            ))
        )
        opcion_primero.click()

        # 1. Hacer clic en el combobox asociado al label "Calendario en el que estudia"
        combobox_calendario = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//label[span[normalize-space()='Calendario en el que estudia']]/following::input[@role='combobox'][1]"
            ))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", combobox_calendario)
        combobox_calendario.click()

        # 2. Esperar a que se muestren las opciones dentro de ese combobox
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//label[span[normalize-space()='Calendario en el que estudia']]" +
                "/ancestor::div[contains(@class,'slds-combobox')]//div[@role='option']"
            ))
        )

        # 3. Hacer clic en la opción "Calendario A (Enero - Diciembre)"
        opcion_calendario_a = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//label[span[normalize-space()='Calendario en el que estudia']]" +
                "/ancestor::div[contains(@class,'slds-combobox')]//span[normalize-space()='Calendario A (Enero - Diciembre)']"
            ))
        )
        opcion_calendario_a.click()
        time.sleep(10)
        pass

    def button_regresar(self):
        boton_anterior = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='button-container']/button[1]"))
        )
        boton_anterior.click()  
        pass
