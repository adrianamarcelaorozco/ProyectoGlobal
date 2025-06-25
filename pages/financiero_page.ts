import { Page } from '@playwright/test';
import BasePage from './base_page';
import config from '../config/config';

export class FinancieroFormPage extends BasePage {
  constructor(page: Page) {
    super(page);
  }

  async perfilFinanciero(): Promise<void> {
    const promedioInput = this.page.locator('xpath=//input[contains(@class,"slds-input") and @role="combobox"]');
    await promedioInput.click();
    await promedioInput.fill(config.PROMEDIO);
    await this.page.locator("//span[contains(@class, 'slds-listbox__option-text') and text()='0 a 4.000.000']").click();

    const empleadoInput = this.page.locator(
      'xpath=/html/body/div[4]/div[1]/section/div[1]/div[2]/div[2]/div[1]/div/div/div/div/div/c-gsv-formulary-english/div/article/div[2]/vlocity_ins-omniscript-step[6]/div[3]/slot/vlocity_ins-omniscript-block/div/div/section/fieldset/slot/vlocity_ins-omniscript-select[2]/slot/c-combobox/div/div/div[2]/div[1]/div/input'
    );
    await empleadoInput.scrollIntoViewIfNeeded();
    await empleadoInput.fill('Empleado');
    await this.page.locator("//span[contains(@class, 'slds-listbox__option-text') and text()='Empleado']").click();

    const ahorrosInput = this.page.locator('xpath=//c-masked-input//input[@type="text"]');
    await ahorrosInput.scrollIntoViewIfNeeded();
    await ahorrosInput.fill(config.VALOR_APROX);

    const checkboxXPaths = [
      '//c-checkbox-group//label[1]/span[1]',
      '//c-checkbox-group//div[4]/label/span[1]',
      '//c-checkbox-group//div[6]/label/span[1]',
    ];

    for (const xpath of checkboxXPaths) {
      const checkbox = this.page.locator(`xpath=${xpath}`);
      await checkbox.scrollIntoViewIfNeeded();
      await checkbox.click();
    }

    const imageOption = this.page.locator(
      'xpath=//c-checkbox-image-group//div[2]/label/div'
    );
    await imageOption.scrollIntoViewIfNeeded();
    await imageOption.click();
  }

  async buttonSiguiente(): Promise<void> {
    const button = this.page.locator(
      'xpath=/html/body/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div/div/div/div/div/c-gsv-formulary-english/div/article/div[2]/vlocity_ins-omniscript-step[6]/div[3]/slot/vlocity_ins-omniscript-block/div/div/section/fieldset/slot/vlocity_ins-omniscript-custom-lwc/slot/c-global-onboarding-custom-button-cmp/div/button[2]'
    );
    await button.scrollIntoViewIfNeeded();
    await button.click();
    await this.page.waitForTimeout(30000);
    console.log('Validación Perfil Financiero');
  }

  async buttonAnterior(): Promise<void> {
    const botonRegresar = this.page.locator("//button[text()='Anterior']");
    await botonRegresar.click();
  }
}
