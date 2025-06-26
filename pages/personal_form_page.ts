import { Page, expect, Locator } from '@playwright/test';
import config from '../config/config';
import BasePage from './base_page';

export class PersonalFormPage extends BasePage {
  constructor(page: Page) {
    super(page);
  }
  async getFechaNacimientoPrincipal(): Promise<Locator> {
    const primerLabel = this.page.locator('label:has-text("Fecha de Nacimiento")').first();
    const inputId = await primerLabel.getAttribute('for');
    return this.page.locator(`#${inputId}`);
  }
  
  async getFechaNacimientoPersona(): Promise<Locator> {
    const segundoLabel = this.page.locator('label:has-text("Fecha de nacimiento")').nth(1);
    const inputId = await segundoLabel.getAttribute('for');
    return this.page.locator(`#${inputId}`);
  }

  async completarFormularioMayor(): Promise<void> {
    const fechaNacimientoInput = await this.getFechaNacimientoPrincipal();
    await fechaNacimientoInput.waitFor({ state: 'visible', timeout: 10000 });
    await fechaNacimientoInput.click({ force: true });
    await fechaNacimientoInput.fill('');
    await fechaNacimientoInput.type('12/28/1984');
    await fechaNacimientoInput.press('Tab');
    await expect(fechaNacimientoInput).toHaveValue('12/28/1984');

    const sexoCombo = this.page.getByRole('combobox', { name: /Sexo/i });
    await sexoCombo.waitFor({ state: 'visible' });
    await sexoCombo.click();
    await this.page.locator('//div[@role="option"]//span[text()="Masculino"]').click();

    const radio = this.page.locator('input[type="radio"][value="Pareja con hijos menores de edad"]');
    await radio.waitFor({ state: 'visible' });
    const radioId = await radio.getAttribute('id');
    await this.page.locator(`label[for="${radioId}"]`).click();
    await expect(radio).toBeChecked();

    const dependientes = this.page.getByRole('combobox', { name: /¿Cuántas personas dependen de ti\?/i });
    await dependientes.click();
    await this.page.locator('//div[@role="option"]//span[normalize-space()="01"]').first().click();

    const nombre = this.page.locator('input.vlocity-input.slds-input[type="text"]').first();
    await nombre.fill(config.NOMBRED);
    await expect(nombre).toHaveValue(config.NOMBRED);

    const apellido1 = this.page.locator('input[placeholder="Primer apellido"]').first();
    await apellido1.fill(config.PAPELLIDOD);

    const apellido2 = this.page.locator('input[placeholder="Segundo apellido"]').first();
    await apellido2.fill(config.SAPELLIDOD);

    const parentescoCombo = this.page.getByRole('combobox', { name: /parentesco/i });
    await parentescoCombo.click();
    await this.page.getByRole('option', { name: 'Hijo/a', exact: true }).click();

    const fechaNacimientoFamiliar = await this.getFechaNacimientoPersona();
    await fechaNacimientoFamiliar.waitFor({ state: 'visible', timeout: 10000 });
    await fechaNacimientoFamiliar.click({ force: true });
    await fechaNacimientoFamiliar.fill('');
    await fechaNacimientoFamiliar.type('01/18/1970');
    await fechaNacimientoFamiliar.press('Tab');
    await expect(fechaNacimientoFamiliar).toHaveValue('01/18/1970');// 👇 Validación opcional para depurar el valor real del input
}

  async completarFormularioMenor(): Promise<void> {
    await this.page.locator('//input[@data-id="date-picker-slds-input"]').fill('12/28/1992');

    const sexoCombo = this.page.locator('#comboboxId-366');
    await sexoCombo.click();
    await this.page.locator('//div[@role="option" and @data-value="Masculino"]').click();

    const radio = this.page.locator('input[type="radio"][value="Pareja con hijos menores de edad"]');
    const radioId = await radio.getAttribute('id');
    await this.page.locator(`label[for="${radioId}"]`).click();

    const tipoHogar = this.page.locator('#comboboxId-391');
    await tipoHogar.click();
    await this.page.locator('//div[@role="option"]//span[text()="01"]').click();

    await this.page.locator('//c-input[1] input').fill(config.NOMBRED);
    await this.page.locator('//c-input[2] input').fill(config.PAPELLIDOD);
    await this.page.locator('//c-input[3] input').fill(config.SAPELLIDOD);

    const rolCombo = this.page.getByRole('combobox', { name: /rol/i });
    await rolCombo.click();
    await this.page.getByRole('option', { name: 'Hijo/a', exact: true }).click();

    const fecha = this.page.getByPlaceholder('Fecha de nacimiento');
    await fecha.fill('01/18/2020');

    const escolaridad = this.page.locator('//vlocity_ins-omniscript-select[2] input');
    await escolaridad.click();
    await escolaridad.fill(config.ESCOLARIDAD);
    await this.page.locator("//span[contains(text(),'Primero')]").click();

    const calendario = this.page.locator('//vlocity_ins-omniscript-select[3] input');
    await calendario.click();
    await calendario.fill(config.CALENDARIOE);
    await this.page.locator("//span[contains(text(),'Calendario A (Enero - Diciembre)')]").click();
  }

  async clickGuardar(): Promise<void> {
    const botonGuardar = this.page.getByRole('button', { name: 'Guardar y continuar' });
    await botonGuardar.scrollIntoViewIfNeeded();
    await botonGuardar.click();
  }

  async clickRegresar(): Promise<void> {
    const botonRegresar = this.page.getByRole('button', { name: 'Anterior' })
    await botonRegresar.waitFor({ state: 'visible' });
    await botonRegresar.click();
  }
  
}

export default PersonalFormPage;
