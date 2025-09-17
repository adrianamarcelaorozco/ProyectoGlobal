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
from pages.cotizar_page import CotizarFormPage
from pages.producto_page import ProductoFormPage

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
    cotizar= CotizarFormPage(driver)
    producto= ProductoFormPage(driver)
    consulta.login()
    form.complete_form()
    form.boton_siguiente()
    form.validate_second_form()
    form.boton_siguiente2()
    pform.personal_form_mayor()
    pform.boton_guardar()
    finan.perfil_financiero()
    finan.button_siguiente()
    metas.metas_fiancieras()
    metas.button_cotizar()
    cotizar.datos_asegurado()
    cotizar.datos_beneficiario()
    cotizar.boton_guardar()
    cotizar.datos_colegio()
    cotizar.boton_guardar()
    producto.datos_producto()
    producto.datos_producto_segura_plus()
    producto.button_cotizar()
    producto.simulador_producto_segura_plus()
    producto.boton_anterior()
    producto.datos_producto_segura_plus_semestre()
    producto.button_cotizar()
    producto.simulador_producto_segura_plus_semestre()
    producto.boton_anterior()
    producto.datos_producto_gmprofesional()
    producto.button_cotizar()
    producto.simulador_producto_gmprofesional()
    producto.button_cotizar()
    producto.button_finalizar()

