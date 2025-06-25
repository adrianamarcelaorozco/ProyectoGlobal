import { Page, expect } from '@playwright/test';

export class MetasFormPage {
  constructor(private page: Page) {}

  async metasFinancieras() {
    const botonNavegar = this.page.locator(
      '//div/c-gsv-data-comparador-english/div/article/div[2]/vlocity_ins-omniscript-step/div[3]/slot/vlocity_ins-omniscript-navigate-action[1]/slot/c-navigate-action/slot/div/c-button/button'
    );
    await botonNavegar.scrollIntoViewIfNeeded();
    await this.page.waitForTimeout(3000);

    const titulo = this.page.locator(
      "//*[@id='brandBand_2']//h2[contains(text(), 'Solución educativa')]"
    );
    await expect(titulo).toBeVisible();
    await this.page.waitForTimeout(5000);
  }

  async buttonCotizar() {
    const botonCotizar = this.page.locator(
      '//c-global-onboarding-product-card-cmp/article/section/div[1]/button'
    );
    await botonCotizar.scrollIntoViewIfNeeded();
    await botonCotizar.click();
    await this.page.waitForTimeout(30000);
    console.log("Validación Metas Financieras");
  }

  async buttonRegreso() {
    const botonRegresar = this.page.locator("//button[.//span[text()='Regresar al perfilamiento']]");
    await botonRegresar.click();
  }

  async buttonComprador() {
    const botonComprador = this.page.locator("//button[.//span[text()='Regresar al comparador']]");
    await botonComprador.click();
  }
}
