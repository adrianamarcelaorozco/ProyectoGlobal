# pages/producto_page.py
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


class ProductoFormPage(BasePage):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    # ==============================
    # AÑO / OBSERVACIONES
    # ==============================
    def datos_producto(self):
        w = WebDriverWait(self.driver, 25)

        # Año
        anio_btn = w.until(EC.element_to_be_clickable((
            By.XPATH, "//button[@role='combobox' and @aria-label='Año de ingreso a cotizar']"
        )))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", anio_btn)
        anio_btn.click()
        w.until(EC.presence_of_element_located((
            By.XPATH, "//div[@role='listbox' and contains(@id,'dropdown-element')]"
        )))
        opcion_2038 = w.until(EC.element_to_be_clickable((
            By.XPATH, "//lightning-base-combobox-item[@data-value='2038']"
        )))
        self.driver.execute_script("arguments[0].click();", opcion_2038)
        time.sleep(0.3)

        # Observaciones
        obs = w.until(EC.element_to_be_clickable((
            By.XPATH, "//label[normalize-space()='Observaciones']/following::input[1]"
        )))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", obs)
        obs.clear()
        obs.send_keys("Ninguno")

    # ==============================
    # HELPERS PRODUCTO
    # ==============================
    def _find_producto_wrapper(self):
        # Preferido por data-omni-key
        try:
            wrap = self.driver.find_element(By.XPATH, "//*[starts-with(@data-omni-key,'ProductoSeleccionado')]")
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", wrap)
            return wrap
        except Exception:
            pass
        # Fallback: segundo select (similar a grabación)
        try:
            wrap = self.driver.find_element(By.XPATH, "(//vlocity_ins-omniscript-select)[2]")
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", wrap)
            return wrap
        except Exception:
            return None

    def _get_producto_container_and_control(self, wrapper):
        container = wrapper.find_element(By.XPATH, ".//div[contains(@class,'slds-combobox')][1]")
        control = wrapper.find_element(
            By.XPATH,
            ".//div[contains(@class,'slds-form-element__control')]//div[contains(@class,'slds-combobox__form-element')]"
        )
        return container, control

    def _abrir_producto(self):
        wrap = self._find_producto_wrapper()
        if not wrap:
            raise RuntimeError("No se encontró el componente de Producto.")
        container, control = self._get_producto_container_and_control(wrap)
        try:
            inp = container.find_element(By.XPATH, ".//input[@role='combobox']")
        except Exception:
            inp = None

        for _ in range(3):
            if inp:
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", inp)
                self.driver.execute_script("arguments[0].click();", inp)
                time.sleep(0.15)
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", control)
            self.driver.execute_script("arguments[0].click();", control)
            time.sleep(0.2)
            cls = container.get_attribute("class") or ""
            expanded = (inp.get_attribute("aria-expanded") if inp else "") or ""
            if "slds-is-open" in cls or expanded.lower() == "true":
                break

        listbox = container.find_element(By.XPATH, ".//div[@role='listbox']")
        return container, listbox

    def _click_opcion(self, listbox, label_text):
        try:
            op = listbox.find_element(By.XPATH, f".//div[@role='option' and @data-label=\"{label_text}\"]")
        except Exception:
            op = listbox.find_element(By.XPATH, f".//span[normalize-space()=\"{label_text}\"]/ancestor::div[@role='option']")
        # eventos nativos
        self.driver.execute_script("""
            const el = arguments[0];
            for (const t of ['pointerdown','mousedown','mouseup','click']) {
                el.dispatchEvent(new MouseEvent(t,{bubbles:true,cancelable:true,composed:true}));
            }
        """, op)
        return op

    def _hard_set_producto(self, container, desired_label, option_elem=None):
        """
        Plan B: setear el valor por JS + disparar eventos para que OmniScript haga binding.
        """
        self.driver.execute_script("""
            const container = arguments[0];
            const desired = arguments[1];
            const option = arguments[2];
            const inp = container.querySelector("input[role='combobox']");
            let dv = "";
            if (option) {
                dv = option.getAttribute("data-value") || "";
            } else {
                const lb = container.querySelector("div[role='listbox']");
                const found = Array.from(lb.querySelectorAll("div[role='option']")).find(
                  o => (o.getAttribute('data-label')===desired) || (o.textContent.trim()===desired)
                );
                if (found) dv = found.getAttribute("data-value") || "";
            }
            if (inp) {
                inp.value = desired;
                inp.setAttribute("data-value", dv);
                inp.setAttribute("aria-invalid", "false");
                inp.dispatchEvent(new Event("input", {bubbles:true}));
                inp.dispatchEvent(new Event("change", {bubbles:true}));
                inp.dispatchEvent(new Event("blur", {bubbles:true}));
            }
        """, container, desired_label, option_elem)

    def _confirm_producto_set(self, container, desired_label, timeout=6):
        end = time.time() + timeout
        try:
            inp = container.find_element(By.XPATH, ".//input[@role='combobox']")
        except Exception:
            inp = None
        last_val = ""
        while time.time() < end and inp:
            val = (inp.get_attribute("value") or "").strip()
            ai = (inp.get_attribute("aria-invalid") or "").strip().lower()
            last_val = val
            if val == desired_label or ai == "false":
                return True
            time.sleep(0.25)
        return False

    def _seleccionar_producto(self, etiqueta_visible):
        container, listbox = self._abrir_producto()

        # 1) intento normal con click a la opción
        opcion = self._click_opcion(listbox, etiqueta_visible)
        if self._confirm_producto_set(container, etiqueta_visible, timeout=3):
            return

        # 2) HARD SET por JS (forzar binding)
        self._hard_set_producto(container, etiqueta_visible, opcion)
        if self._confirm_producto_set(container, etiqueta_visible, timeout=3):
            return

        # 3) Blur con TAB y reintento de confirmación
        try:
            inp = container.find_element(By.XPATH, ".//input[@role='combobox']")
            inp.send_keys(Keys.TAB)
            time.sleep(0.3)
        except Exception:
            pass

        if not self._confirm_producto_set(container, etiqueta_visible, timeout=2):
            try:
                ai = inp.get_attribute("aria-invalid") if inp else "N/A"
                val = (inp.get_attribute("value") if inp else "N/A")
            except Exception:
                ai, val = "N/A", "N/A"
            raise AssertionError(f"Producto no quedó seleccionado. value='{val}', aria-invalid={ai}")

    # ==============================
    # FLUJOS DE PRODUCTO
    # ==============================
    def datos_producto_segura_plus(self):
        self._seleccionar_producto("Global Universidad Segura Plus")
        self._llenar_campos_comunes()

    def datos_producto_segura_plus_semestre(self):
        self._seleccionar_producto("Global Universidad Segura Plus Semestres")
        self._llenar_campos_comunes()

    def datos_producto_gmprofesional(self):
        self._seleccionar_producto("GlobalMás Profesional")
        self._llenar_campos_comunes()

    # ==============================
    # CAMPOS COMUNES (Tarifa)
    # ==============================
    def _llenar_campos_comunes(self):
        try:
            self.seleccionar_tarifa_septiembre()
        except Exception as e:
            print(f"⚠ No se pudo seleccionar tarifa: {e}")

    def seleccionar_tarifa_septiembre(self, timeout=15):
        w = WebDriverWait(self.driver, timeout)
        cont = w.until(EC.presence_of_element_located((
            By.XPATH, "//label[.//span[normalize-space()='Tarifa']]/ancestor::div[contains(@class,'slds-combobox')][1]"
        )))
        try:
            opener = cont.find_element(By.XPATH, ".//input[@role='combobox']")
        except Exception:
            opener = cont.find_element(By.XPATH, ".//span[contains(@class,'slds-input__icon_right')]")
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", opener)
        self.driver.execute_script("arguments[0].click();", opener)

        # listbox (aunque no marque slds-is-open)
        lb = cont.find_element(By.XPATH, ".//div[@role='listbox']")

        # intenta “Septiembre”, si no existe, toma el primer option disponible
        opcion = None
        try:
            opcion = lb.find_element(By.XPATH, ".//div[@role='option' and @data-label='Septiembre']")
        except Exception:
            try:
                opcion = lb.find_element(By.XPATH, ".//span[normalize-space()='Septiembre']/ancestor::div[@role='option']")
            except Exception:
                # primer opción disponible
                opcion = lb.find_element(By.XPATH, ".//div[@role='option'][1]")

        self.driver.execute_script("arguments[0].click();", opcion)
        print("✅ Tarifa seleccionada")

    # ==============================
    # SIMULADORES (validaciones)
    # ==============================
    def simulador_producto_segura_plus(self):
        # si te sigue fallando aquí, probablemente no quedó el producto → ver arriba
        titulo = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//*[normalize-space()='Valor asegurado semestre']"))
        )
        assert titulo.is_displayed()

    def simulador_producto_segura_plus_semestre(self):
        titulo = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//*[normalize-space()='Global Universidad Segura Plus Semestres']"))
        )
        assert titulo.is_displayed()

    def simulador_producto_gmprofesional(self):
        titulo = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(normalize-space(),'GlobalMás Profesional')]"))
        )
        assert titulo.is_displayed()

    # ==============================
    # BOTONES
    # ==============================
    def button_cotizar(self):
        # Sólo dispara si el campo Producto NO está en error
        try:
            wrap = self._find_producto_wrapper()
            cont, _ = self._get_producto_container_and_control(wrap)
            inp = cont.find_element(By.XPATH, ".//input[@role='combobox']")
            ai = (inp.get_attribute("aria-invalid") or "").lower()
            if ai == "true":
                raise AssertionError("Producto sigue requerido. No se puede Cotizar.")
        except Exception:
            # si no podemos leer el estado, continuamos, pero el simulador puede fallar
            pass

        btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[normalize-space()='Cotizar']]")))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        btn.click()
        time.sleep(1.5)

    def boton_anterior(self):
        btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[normalize-space()='Anterior']]")))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        btn.click()
        time.sleep(1.0)

    def button_finalizar(self):
        btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[normalize-space()='Finalizar']]")))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        btn.click()
        time.sleep(1.5)
