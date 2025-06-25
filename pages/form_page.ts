import { Page, expect } from '@playwright/test';
import BasePage from './base_page';
import config from '../config/config';
import {
  generarIdentificacionAleatoria,
  generarCorreoAleatorio,
  generarNumeroTelefono
} from '../utils/helpers';
import { setDefaultTimeout } from '@cucumber/cucumber';

// Aumenta el timeout global a 120 segundos (2 minutos)
setDefaultTimeout(120 * 1000);

export class FormPage extends BasePage {
  constructor(page: Page) {
    super(page);
  }

  async completeForm(): Promise<void> {
    const targetUrl = "https://globalseguros--qaonb.sandbox.lightning.force.com/lightning/cmp/vlocity_ins__vlocityLWCOmniWrapper?c__target=c%3AgsvFormularyEnglish&c__layout=lightning&c__tabLabel=Perfilamiento";
    await this.openUrl(targetUrl);
  
    // 1. Esperar y hacer clic en el combobox
    const combobox = this.page.locator("//input[@role='combobox' and starts-with(@aria-controls, 'combobox-list')]");

    // Asegúrate de que el combobox esté visible
    await combobox.waitFor({ state: 'visible', timeout: 15000 });
    await combobox.scrollIntoViewIfNeeded();

    // Haz clic hasta que el dropdown se abra (aria-expanded='true')
    await combobox.click();
    await this.page.waitForFunction(
      el => el && el.getAttribute('aria-expanded') === 'true',
      await combobox.elementHandle(),
      { timeout: 10000 }
    );

    // Ahora sí espera la opción
    const option = this.page.locator("//div[@role='option']//span[text()='CEDULA DE CIUDADANIA']");
    await option.waitFor({ state: 'visible', timeout: 10000 });
    await option.scrollIntoViewIfNeeded();
    await option.click();
    // 3. Ingresar número aleatorio
    const numeroIdentificacion = generarIdentificacionAleatoria();
    //await this.enterText("//input[contains(@class, 'vlocity-input') and @type='text']", numeroIdentificacion);
    await this.enterText("//input[@placeholder='Ingresa el Número de documento']", numeroIdentificacion);

    // 4. Buscar asesor
    await this.enterText(
      "//input[contains(@class, 'slds-input') and @role='combobox' and contains(@aria-autocomplete, 'list')]",
      config.ASESOR
    );
  
    const dropdownOption = this.page.locator("//div[@role='option']//span[contains(text(), 'PROYECTA-T LTDA-BOGOTA')]");
    await dropdownOption.waitFor({ state: 'visible', timeout: 10000 });
    await dropdownOption.click();
  }
  
  async completeFormEmail(): Promise<void> {
    const targetUrl = "https://globalseguros--qaonb.sandbox.lightning.force.com/lightning/cmp/vlocity_ins__vlocityLWCOmniWrapper?c__target=c%3AgsvFormularyEnglish&c__layout=lightning&c__tabLabel=Perfilamiento";
    await this.openUrl(targetUrl);

    await this.page.locator("//span[contains(text(), 'Email o Celular')]").click();

    await this.enterText("//input[@placeholder='Ingrese el número telefónico']", generarNumeroTelefono());
    await this.enterText("//input[@placeholder='Ingrese el correo electrónico']", generarCorreoAleatorio());

    await this.enterText("//input[contains(@class, 'slds-input') and @role='combobox']", config.ASESOR);
    const option = this.page.locator("//div[@role='option']//span[contains(text(), 'PROYECTA-T LTDA-BOGOTA')]");
    await option.scrollIntoViewIfNeeded();
    await option.click();
  }

  async botonSiguiente(): Promise<void> {
    const boton = this.page.locator("//button[.//span[text()='Siguiente']]").first(); // ← Aquí está el fix
    await boton.scrollIntoViewIfNeeded();
    await boton.click();
    console.log("Formulario inicial completado");
  }
  

  async validateSecondForm(): Promise<void> {
    await this.enterText("//input[@placeholder='Nombres']", config.NOMBRE);
    await this.enterText("//input[@placeholder='Primer Apellido']", config.PAPELLIDO);
    await this.enterText("//input[@placeholder='Segundo Apellido']", config.SAPELLIDO);
    await this.enterText("//input[@placeholder='Correo electrónico']", config.EMAIL);

    const ciudadInput = this.page.getByRole('combobox', { name: /Ciudad/i });
    await ciudadInput.waitFor({ state: 'visible', timeout: 15000 });
    await ciudadInput.scrollIntoViewIfNeeded();
    await ciudadInput.fill(config.CIUDAD);


    // Esperar la opción "BOGOTA" y hacer clic
    const opcionBogota = this.page.locator("//span[text()='BOGOTA']");
    await opcionBogota.waitFor({ state: 'visible', timeout: 10000 });
    await opcionBogota.click();

    const telefonoInput = this.page.locator('input[type="tel"].vlocity-input');
    await telefonoInput.waitFor({ state: 'visible', timeout: 10000 });
    await telefonoInput.scrollIntoViewIfNeeded();
    await telefonoInput.fill(config.TELEFONO);
    
    const eventoInput = this.page.getByRole('combobox', { name: /evento/i });
    await eventoInput.waitFor({ state: 'visible', timeout: 10000 });
    await eventoInput.scrollIntoViewIfNeeded();
    await eventoInput.fill(config.EVENTO);
    
    // seleccionar la opción
    const eventoOpcion = this.page.locator("//span[contains(text(), 'FERIA DEL LIBRO 2024')]");
    await eventoOpcion.click();
    
    await this.page.locator('input.vlocity-input[type="checkbox"]').first().check();
  }

  async validateSecondFormEmail(): Promise<void> {
    await this.enterText("//input[@type='text' and contains(@class, 'slds-input')]", config.NOMBRE);
    await this.enterText("//input[@placeholder='Primer Apellido']", config.PAPELLIDO);
    await this.enterText("//input[@placeholder='Segundo Apellido']", config.SAPELLIDO);

    const tipoDocInput = this.page.locator("//div[contains(@class, 'slds-combobox__form-element')]//input");
    await tipoDocInput.click();
    await this.page.locator("//*[contains(text(), 'CEDULA DE CIUDADANIA')]").click();

    await this.enterText("//input[@placeholder='Numero Documento']", generarIdentificacionAleatoria());
    await this.enterText("//input[@placeholder='Correo electrónico']", config.EMAIL);

    await this.enterText('//*[@id="inputId-307"]', config.CIUDAD);
    await this.page.locator("//span[text()='BOGOTA']").click();

    await this.page.locator('//*[@id="input33-319"]').scrollIntoViewIfNeeded();
    await this.page.locator('//*[@id="input33-319"]').fill(config.TELEFONO);

    await this.enterText('//*[@id="inputId-322"]', config.EVENTO);
    await this.page.locator("//span[text()='FERIA DEL LIBRO 2024']").click();

  
    // Scroll dentro del contenedor que sí tiene el scroll
await this.page.evaluate(() => {
  const scrollContainer = document.querySelector('.slds-form-element.slds-form-container');
  if (scrollContainer) {
    scrollContainer.scrollTop = scrollContainer.scrollHeight;
  }
});
await this.page.waitForTimeout(1000);
// 2. Esperar que el "checkbox visual" esté visible (el span clickeable)
const fauxCheckbox = this.page.locator('span.slds-checkbox_faux');
await fauxCheckbox.waitFor({ state: 'visible', timeout: 10000 });
await fauxCheckbox.scrollIntoViewIfNeeded();
await fauxCheckbox.click();

// 3. Scroll solo al faux-checkbox (por si está dentro de un contenedor)
await fauxCheckbox.scrollIntoViewIfNeeded();

// 4. Click directamente sobre el span visual (NO el input)
await fauxCheckbox.click();

// 5. Validar que el input asociado ahora esté checked
const checkbox = this.page.locator('input.vlocity-input[type="checkbox"]').first();
await expect(checkbox).toBeChecked();

console.log("✅ Checkbox marcado correctamente vía slds-checkbox_faux");

  }

  async botonGuardaryContinuar(): Promise<void> {
    const boton = this.page.getByRole('button', { name: 'Guardar y continuar' });
    await boton.waitFor({ state: 'visible', timeout: 10000 });
    await boton.click();    
    console.log("Validación Datos de contacto");
  }
 
}

export default FormPage;
