import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.consulta_page import ConsultaPage
from pages.form_page import FormPage
from pages.personal_form_page import PersonalFormPage
from pages.financiero_page import FinancieroFormPage
from pages.metas_pages import MetasFormPage
import time

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

def test_consulta(driver):
    consulta = ConsultaPage(driver)
    form = FormPage(driver)
    pform = PersonalFormPage(driver)
    finan= FinancieroFormPage(driver)
    metas= MetasFormPage(driver)
    consulta.login()
    form.complete_form()
    form.boton_siguiente()
    form.validate_second_form()
    form.boton_siguiente2()
    pform.personal_form_mayor()
    pform.button_regresar()
    time.sleep(5)
    form.boton_siguiente2()
    time.sleep(5)
    pform.boton_guardar()
    time.sleep(5)
    finan.perfil_financiero()
    time.sleep(5)
    finan.button_anterior()
    time.sleep(5)
    pform.boton_guardar()
    time.sleep(5)
    finan.button_siguiente()
    time.sleep(5)
    metas.metas_fiancieras()
    time.sleep(5)
    metas.button_regreso()
    time.sleep(5)