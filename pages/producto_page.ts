import { Page, Locator, expect } from '@playwright/test';
import config from '../config/config';

export class ProductoFormPage {
  readonly page: Page;
  readonly comboboxAnio: Locator;
  readonly opcion2038: Locator;
  readonly observaciones: Locator;
  readonly aseguradoInput: Locator;
  readonly aseguradoOption: Locator;
  readonly productoInput: Locator;
  readonly mesInput: Locator;

  constructor(page: Page) {
    this.page = page;
    this.comboboxAnio = page.locator('button[aria-label*="Año"]');
    this.opcion2038 = page.locator('lightning-base-combobox-item[data-value="2038"]');
    this.observaciones = page.locator('input').nth(1);
    this.aseguradoInput = page.locator('input[role="combobox"]').nth(2);
    this.aseguradoOption = page.locator('text=5.000.000');
    this.productoInput = page.locator('input[role="combobox"]').first();
    this.mesInput = page.locator('input[role="combobox"]').nth(1);
  }

  async datosProducto() {
    await this.comboboxAnio.scrollIntoViewIfNeeded();
    await this.comboboxAnio.click({ timeout: 10000 });

    await this.opcion2038.waitFor({ state: 'visible', timeout: 10000 });
    await this.opcion2038.click();

    await this.observaciones.waitFor({ state: 'visible', timeout: 10000 });
    await this.observaciones.click();
    await this.observaciones.fill('Ninguno');

    console.log('Año de ingreso a cotizar');
  }

async listaAsegurado() {
    await this.aseguradoInput.scrollIntoViewIfNeeded();
    await this.aseguradoInput.click();
    await this.aseguradoInput.fill(config.VALOR_ASEGURADO || '1.000.000');

    await this.aseguradoOption.waitFor({ state: 'visible', timeout: 10000 });
    await this.aseguradoOption.click();
  }

  async datosProductoSeguraPlus() {
    // PRODUCTO
    await this.productoInput.scrollIntoViewIfNeeded();
    await this.productoInput.click();

    // Simular navegación con flechas
    await this.page.keyboard.press('ArrowDown');
    await this.page.keyboard.press('Enter');

    // MES
    await this.mesInput.scrollIntoViewIfNeeded();
    await this.mesInput.click();
    await this.page.keyboard.press('Enter');

    // ASEGURADO
    await this.listaAsegurado();
  }
  async datosProductoSeguraPlusSemestre() {
    // PRODUCTO
    await this.productoInput.scrollIntoViewIfNeeded();
    await this.productoInput.click();
    await this.page.waitForTimeout(500); // breve espera para evitar errores
  
    await this.page.keyboard.press('ArrowDown'); // para bajar una vez
    await this.page.keyboard.press('Enter');
  
    // MES
    await this.mesInput.scrollIntoViewIfNeeded();
    await this.mesInput.click();
    await this.page.keyboard.press('Enter');
  
    // ASEGURADO
    await this.aseguradoInput.scrollIntoViewIfNeeded();
    await this.aseguradoInput.click();
    await this.aseguradoInput.fill(config.VALOR_ASEGURADO || '1.000.000');
    await this.aseguradoOption.waitFor({ state: 'visible' });
    await this.aseguradoOption.click();
  
    // SEMESTRE
    const semestreInput = this.page.locator(
      'vlocity_ins-omniscript-select >> nth=15 input'
    );
    await semestreInput.scrollIntoViewIfNeeded();
    await semestreInput.click();
    for (let i = 0; i < 6; i++) {
      await this.page.keyboard.press('ArrowDown');
      await this.page.waitForTimeout(300);
    }
    await this.page.keyboard.press('Enter');
    console.log('Opción semestre 6 seleccionada');
  }
  async datosProductoGmProfesional() {
    await this.page.waitForTimeout(5000);
    const productoElemento = this.page.locator('input[role="combobox"]');
    await productoElemento.scrollIntoViewIfNeeded();
    await productoElemento.click();
    await productoElemento.press('ArrowDown');
    await productoElemento.press('Enter');

    const tarifa = this.page.locator('xpath=/html/body/.../input');
    await tarifa.click();
    await tarifa.fill(process.env.MES_TARIFA || '');
    await tarifa.press('Enter');
    await this.page.locator('xpath=/html/body/.../span[text()="...opcion..."]').click();

    const asegurado = this.page.locator('xpath=/html/body/.../input');
    await asegurado.click();
    await asegurado.fill(process.env.VALOR_ASEGURADO2 || '');
    await this.page.locator('xpath=//span[text()="2.000.000"]').click();

    const año = this.page.locator('xpath=/html/body/.../button');
    await año.click();
    for (let i = 0; i < 6; i++) await año.press('ArrowDown');
    await año.press('Enter');

    const periodo = this.page.locator('xpath=/html/body/.../input');
    await periodo.click();
    for (let i = 0; i < 6; i++) await periodo.press('ArrowDown');
    await periodo.press('Enter');
  }

  async simuladorProductoSeguraPlus() {
    const titulo = this.page.locator('text=Valor asegurado semestre');
    await expect(titulo).toBeVisible();
    await this.page.waitForTimeout(10000);
    console.log("El texto '$ 0,00' está presente en la página.");
  }

  async simuladorProductoSeguraPlusSemestre() {
    const titulo = this.page.locator('text=GlobalUniversidad Segura Plus Semestres');
    await expect(titulo).toBeVisible();
    const combobox = this.page.locator('input[role="combobox"]');
    await combobox.click();
    await this.page.locator('text=3.000.000').click();
    await this.page.waitForTimeout(5000);
    console.log("El texto '$ 14.538.000,00' está presente en la página.");
  }

  async simuladorProductoGmProfesional() {
    const combobox = this.page.locator('input[role="combobox"]');
    await combobox.click();
    await this.page.locator('text=3.000.000').click();

    const segundoCombo = this.page.locator('xpath=/html/body/.../input');
    await segundoCombo.click();
    await this.page.locator('text=3').click();

    const tercerCombo = this.page.locator('xpath=/html/body/.../input');
    await tercerCombo.click();
    await this.page.locator('text=Trimestral').click();
  }

  async buttonCotizar() {
    const boton = this.page.locator('button:has-text("Cotizar")');
    await boton.scrollIntoViewIfNeeded();
    await boton.click();
    await this.page.waitForTimeout(20000);
  }

  async botonAtras() {
    const boton = this.page.locator('button:has-text("Atras")');
    await boton.scrollIntoViewIfNeeded();
    await boton.click();
  }

  async botonAnterior() {
    const boton = this.page.locator('button:has-text("Atras")');
    await boton.scrollIntoViewIfNeeded();
    await boton.click();
  }
}