import { Page, Locator, expect } from '@playwright/test';
import BasePage from './base_page';
import config from '../config/config';

export class FinancieroFormPage extends BasePage {
  constructor(page: Page) {
    super(page);
  }

  async getComboBoxByLabelText(labelText: string): Promise<Locator> {
    const label = this.page.locator(`label:has-text("${labelText}")`).first();
    const inputId = await label.getAttribute('for');
    return this.page.locator(`#${inputId}`);
  }

  async getInputByLabelText(labelText: string): Promise<Locator> {
    const label = this.page.locator(`label:has-text("${labelText}")`).first();
    const inputId = await label.getAttribute('for');
    return this.page.locator(`#${inputId}`);
  }

  async seleccionarSueñosYObjetivos(opciones: string[]) {
    for (const opcion of opciones) {
      try {
        console.log(`🔍 Seleccionando opción: "${opcion}"`);
  
        // Forzar scroll hacia abajo por si no se ha renderizado
        await this.page.evaluate(() => window.scrollBy(0, 800));
        await this.page.waitForTimeout(500);
  
        // Buscar el texto visible que representa la opción
        const textoOpcion = this.page.getByText(opcion, { exact: false });
        await textoOpcion.waitFor({ state: 'visible', timeout: 5000 });
  
        // Hacer clic en el texto (ya que probablemente activa el checkbox)
        await textoOpcion.click({ force: true });
  
        // Esperar un poco para evitar problemas de sincronización
        await this.page.waitForTimeout(300);
      } catch (e) {
        console.error(`❌ No se pudo seleccionar "${opcion}". Detalles:`, e);
        await this.page.screenshot({ path: `error_${opcion}.png`, fullPage: true });
      }
    }
  }
  
  async seleccionarMediosTransporte(opciones: string[]) {
    for (const opcion of opciones) {
      try {
        console.log(`🚲 Seleccionando medio de transporte: ${opcion}`);
  
        // Buscar el texto visible que identifica la opción
        const texto = this.page.getByText(opcion, { exact: true });
        await texto.waitFor({ state: 'visible', timeout: 5000 });
  
        // Subir al label → luego buscar el input[type="checkbox"]
        const label = texto.locator('..'); // div.captionOut
        const contenedor = label.locator('..'); // label.slds-checkbox__label
        const wrapper = contenedor.locator('..'); // div.slds-checkbox
        const checkbox = wrapper.locator('input[type="checkbox"]');
  
        const isChecked = await checkbox.isChecked();
        if (!isChecked) {
          await texto.click({ force: true }); // El click en el texto activa el checkbox visual
          await this.page.waitForTimeout(300);
        }
      } catch (error) {
        console.error(`❌ No se pudo seleccionar "${opcion}":`, error);
        await this.page.screenshot({ path: `error_transporte_${opcion}.png`, fullPage: true });
      }
    }
  }
    
  async perfilFinanciero(): Promise<void> {
    const ingresosMensuales = await this.getComboBoxByLabelText('¿Cuál es el promedio de tus ingresos mensuales?');
    await ingresosMensuales.scrollIntoViewIfNeeded();
    await ingresosMensuales.waitFor({ state: 'visible', timeout: 10000 });
    await ingresosMensuales.click({ force: true });
  
    const opcionIngresos = this.page.getByRole('option', { name: '4.000.000 a 8.000.000' });
    await opcionIngresos.waitFor({ state: 'visible', timeout: 5000 });
    await opcionIngresos.click();
  
    // Selección del campo "¿Cuál es tu ocupación?"
    const ocupacion = await this.getComboBoxByLabelText('¿Cuál es tu ocupación?');
    await ocupacion.scrollIntoViewIfNeeded();
    await ocupacion.waitFor({ state: 'visible', timeout: 10000 });
    await ocupacion.click({ force: true });
  
    const opcionOcupacion = this.page.getByRole('option', { name: 'Empleado' });
    await opcionOcupacion.waitFor({ state: 'visible', timeout: 5000 });
    await opcionOcupacion.click();

    const ahorrosInput = await this.getInputByLabelText('¿Cuál es el valor aproximado de tus ahorros y/o cesantías?');  
    await ahorrosInput.scrollIntoViewIfNeeded();
    await ahorrosInput.waitFor({ state: 'visible', timeout: 10000 });
    await ahorrosInput.click({ force: true });
    await ahorrosInput.fill('');
    await ahorrosInput.fill('10000000');
    await ahorrosInput.press('Tab');

    // Seleccionar sueños/objetivos
    await this.seleccionarSueñosYObjetivos([
      'Comprar casa',
      'Viajar',
      'Pensionarme con más ingresos',
    ]);

    await this.seleccionarMediosTransporte([
      'Transporte público (bus)',
      'Bicicleta',
      'Carro Particular'
    ]);
  }

  async buttonSiguiente(): Promise<void> {
    const botonGuardar = this.page.getByRole('button', { name: 'Guardar y continuar' });
    await botonGuardar.scrollIntoViewIfNeeded();
    await botonGuardar.click();
  }

  async buttonAnterior(): Promise<void> {
    const botonRegresar = this.page.getByRole('button', { name: 'Anterior' })
    await botonRegresar.waitFor({ state: 'visible' });
    await botonRegresar.click();
  }
}
