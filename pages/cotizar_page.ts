import { Page } from '@playwright/test';
import BasePage from './base_page';
import config from '../config/config';
import { generarNombreCompleto, generarIdentificacionAleatoria } from '../utils/helpers';

export class CotizarFormPage extends BasePage {
  constructor(page: Page) {
    super(page);
  }

  async datosAsegurado(): Promise<void> {
    const botonContinuar = this.page.locator("//button[.//span[text()='Guardar y continuar']]");
    await botonContinuar.scrollIntoViewIfNeeded();
    await botonContinuar.click();
  }

  async datosBeneficiario(): Promise<void> {
    const [nombre, apellido1, apellido2] = generarNombreCompleto();
    const numero = generarIdentificacionAleatoria();

    console.log(`Ingresando: ${nombre} ${apellido1} ${apellido2}`);

    // Ingresar nombres
    await this.page.locator("//input[@placeholder='Nombres completos']").click();
    await this.page.locator("//input[@placeholder='Nombres completos']").fill(nombre);

    await this.page.locator("//input[@placeholder='Primer Apellido']").fill(apellido1);
    await this.page.locator("//input[@placeholder='Segundo Apellido']").fill(apellido2);

    // Seleccionar tipo de documento
    const combobox = this.page.locator("//div[contains(@class, 'slds-combobox__form-element')]//input");
    await combobox.click();

    const optionTipoDoc = this.page.locator("//*[contains(@class, 'slds-listbox')]//span[text()='Tarjeta de Identidad']");
    await optionTipoDoc.click();

    // Número de documento
    await this.page.locator("//input[@placeholder='Ingresar número']").fill(numero.toString());

    // Fecha de nacimiento
    await this.page.locator("//input[@aria-label='Fecha de Nacimiento']").fill('18-02-2020');

    // Selección de sexo
    const sexoInput = this.page.locator('//label[.//span[text()="Sexo"]]/ancestor::div[contains(@class, "slds-form-element")]//input[@role="combobox"]');
    await sexoInput.click();

    const opcionFemenino = this.page.locator('//div[@role="option" and @data-label="Femenino"]');
    await opcionFemenino.scrollIntoViewIfNeeded();
    await opcionFemenino.click();

    await this.page.waitForTimeout(3000);
  }

  async botonGuardar(): Promise<void> {
    const botonGuardar = this.page.locator("//button[span[text()='Guardar y continuar']]");
    await botonGuardar.scrollIntoViewIfNeeded();
    await botonGuardar.click();
    await this.page.waitForTimeout(3000);
    console.log("Validación Información beneficiario");
  }

  async buttonRegresar(): Promise<void> {
    const botonAnterior = this.page.locator("//div[@class='button-container']/button[1]");
    await botonAnterior.click();
  }

  async datosColegio(): Promise<void> {
    await this.page.locator("//input[@role='combobox'][contains(@aria-autocomplete, 'list')]").fill(config.COLEGIO);

    const opcionColegio = this.page.locator("//div[@role='option']//span[contains(text(), 'COLEGIO CALENDARIO A COTIZACION')]");
    await opcionColegio.scrollIntoViewIfNeeded();
    await opcionColegio.click();

    // Hacer clic en icono de editar
    const iconoEditar = this.page.locator('//c-icon[.//span[text()="Edit"]]');
    await iconoEditar.scrollIntoViewIfNeeded();
    await iconoEditar.click();
    await this.page.waitForTimeout(1000);
    await iconoEditar.click();

    // Expandir combobox
    const iconoCombo = this.page.locator('//span[contains(@class, "slds-icon_container")]');
    await iconoCombo.click();

    const inputCurso = this.page.locator("/html/body/div[4]/div[1]/section/.../div/input"); // ← Asegura que sea el selector correcto
    await inputCurso.fill("Prekinder");
    await inputCurso.press("Enter");

    const optionPrekinder = this.page.locator("/html/body/div[4]/div[1]/section/.../li[2]/div/span/span"); // ← Asegura el XPATH
    await optionPrekinder.click();

    console.log("Prekinder seleccionado correctamente");
  }
}
