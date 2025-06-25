// pages/ConsultaPage.ts
import { Page } from '@playwright/test';
import BasePage from './base_page';
import config from '../config/config';

export default class ConsultaPage extends BasePage {
  constructor(page: Page) {
    super(page);
  }

  async login(): Promise<void> {
    await this.openUrl('https://globalseguros--qaonb.sandbox.my.salesforce.com/');
    await this.enterText('input[name="username"]', config.USERNAME);
    await this.enterText('#password', config.PASSWORD);
    await this.clickElement('input#Login');
    await this.page.waitForTimeout(15000); // Espera estática
    console.log('Ingreso Login');
  }

  async completeForm(): Promise<void> {
    const targetUrl = 'https://globalseguros--qaonb.sandbox.lightning.force.com/lightning/cmp/vlocity_ins__vlocityLWCOmniWrapper?c__target=c%3AgsvFormularyEnglish&c__layout=lightning&c__tabLabel=Perfilamiento';
    await this.openUrl(targetUrl);

    const dropdownIdentificacion = this.page.locator('xpath=//*[@id="comboboxId-215"]');
    await dropdownIdentificacion.waitFor({ state: 'visible', timeout: 20000 });
    await dropdownIdentificacion.click();

    const opcionIdentificacion = this.page.locator('//div[@role="option"]//span[contains(text(), "CEDULA DE CIUDADANIA")]');
    await opcionIdentificacion.waitFor({ state: 'visible', timeout: 10000 });
    await opcionIdentificacion.click();

    const inputAsesor = this.page.locator('xpath=/html/body/.../input');
    await inputAsesor.fill(config.ASESOR);

    const dropdownOption = this.page.locator("//span[contains(@class, 'slds-listbox__option-text') and contains(text(), 'PROYECTA-T LTDA-BOGOTA')]");
    await dropdownOption.scrollIntoViewIfNeeded();
    await dropdownOption.click();

    const nextButton = this.page.locator("//button[.//span[text()='Siguiente']]");
    await nextButton.scrollIntoViewIfNeeded();
    await nextButton.click();

    console.log("Formulario inicial completado");
  }
}
