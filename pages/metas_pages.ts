import { Page, expect } from '@playwright/test';

export class MetasFormPage {
  constructor(private page: Page) {}

  async seleccionarObjetivos(textos: string[]) {
    for (const texto of textos) {
      const opcion = this.page.getByText(texto, { exact: true });
  
      await opcion.scrollIntoViewIfNeeded();
      await opcion.waitFor({ state: 'visible', timeout: 5000 });
  
      // Dale clic si no tiene clase de seleccionado (o simplemente dale clic)
      await opcion.click();
    }
  }
  
  async metasFinancieras() {
    await this.seleccionarObjetivos([
      'Realizar un viaje',
      'Adquirir una casa propia',
      'Pensionarme con más ingresos',
    ]);

    await expect(this.page.getByText('Solución Educativa', { exact: true })).toBeVisible();
    await expect(this.page.getByRole('button', { name: 'Cotizar' })).toBeVisible();
  }

  async buttonCotizar() {
    const botonCotizar = this.page.getByRole('button', { name: 'Cotizar' });
    await botonCotizar.scrollIntoViewIfNeeded();
    await botonCotizar.waitFor({ state: 'visible', timeout: 5000 });
    await botonCotizar.click();
  }
  async RegresarAlPerfilamiento() {
    const botonRegresar = this.page.getByRole('button', { name: 'Regresar al perfilamiento' });
    await botonRegresar.scrollIntoViewIfNeeded();
    await botonRegresar.waitFor({ state: 'visible', timeout: 5000 });
    await botonRegresar.click();
  }

  async buttonComprador(): Promise<void> {
    const botonComprador =this.page.getByRole('button', { name: 'Regresar al comparador' });  
    await botonComprador.scrollIntoViewIfNeeded();
    await botonComprador.waitFor({ state: 'visible', timeout: 5000 });
    await botonComprador.click();
  }
}
