// src/pages/ProductoFormPage.ts
import { Page, Locator, expect } from '@playwright/test';
import  BasePage from './base_page';

export default class ProductoFormPage extends BasePage {
  readonly page: Page;

  constructor(page: Page) {
    super(page);
    this.page = page;
  }

  // ✅ DATOS DE PRODUCTO
  async seleccionarAñoIngreso() {
    const combo = this.page.locator('button[aria-label*="Selecciona año"]');
    await combo.scrollIntoViewIfNeeded();
    await combo.click();
    await this.page.locator('lightning-base-combobox-item[data-value="2038"]').click();
  }

  async ingresarObservaciones(texto: string = 'Ninguno') {
    const input = this.page.locator('input[placeholder*="Observaciones"]');
    await input.click();
    await input.fill(texto);
  }

  async completarDatosProducto() {
    await this.seleccionarAñoIngreso();
    await this.ingresarObservaciones();
  }

  // ✅ LISTAS DINÁMICAS
  async seleccionarProducto(opcion: string = 'Global Universidad Segura Plus') {
    const input = this.page.locator('input[placeholder*="Producto"]');
    await input.scrollIntoViewIfNeeded();
    await input.click();
    await input.press('ArrowDown');
    await input.press('Enter');
  }

  async seleccionarMes() {
    const mes = this.page.locator('input[placeholder*="Mes"]');
    await mes.scrollIntoViewIfNeeded();
    await mes.click();
    await mes.press('Enter');
  }

  async seleccionarValorAsegurado(valor: string = '5.000.000') {
    const input = this.page.locator('input[placeholder*="Valor asegurado"]');
    await input.click();
    await input.fill(valor);
    await this.page.getByText(valor, { exact: false }).click();
  }

  // ✅ ESCENARIOS ESPECÍFICOS
  async datosProductoSeguraPlus() {
    await this.seleccionarProducto();
    await this.seleccionarMes();
    await this.seleccionarValorAsegurado();
  }

  // ✅ VALIDACIONES (Simulador)
  async validarSimuladorTextoEsperado(texto: string) {
    const locator = this.page.locator(`text=${texto}`);
    await expect(locator).toBeVisible();
  }

  async validarValorSimulado(valorEsperado: string) {
    const locator = this.page.locator(`text=${valorEsperado}`);
    await expect(locator).toBeVisible();
  }

  // ✅ BOTONES
  async clickBotonCotizar() {
    const boton = this.page.getByRole('button', { name: 'Cotizar' });
    await boton.scrollIntoViewIfNeeded();
    await boton.click();
  }

  async clickBotonFinalizar() {
    const boton = this.page.getByRole('button', { name: 'Finalizar' });
    await boton.scrollIntoViewIfNeeded();
    await boton.click();
  }

  async clickBotonAtras() {
    const boton = this.page.getByRole('button', { name: 'Atras' });
    await boton.scrollIntoViewIfNeeded();
    await boton.click();
  }

  async clickBotonAnterior() {
    const boton = this.page.getByRole('button', { name: 'Anterior' });
    await boton.scrollIntoViewIfNeeded();
    await boton.click();
  }

  // Methods for personal form functionality
  async personalFormMayor(): Promise<void> {
    // Implementation for personal form for adults
  }

  async botonRegresar(): Promise<void> {
    // Implementation for back button
  }

  async botonGuardar(): Promise<void> {
    // Implementation for save button
  }
}
