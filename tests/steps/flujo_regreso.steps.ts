import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from '@playwright/test';
import { page} from '../../support/hooks';
import ConsultaPage from '../../pages/consulta_page';
import {FormPage} from '../../pages/form_page';
import ProductoFormPage from '../../pages/personal_form_page';
import { FinancieroFormPage } from '../../pages/financiero_page';
import { MetasFormPage } from '../../pages/metas_pages';

let consulta: ConsultaPage;
let form: FormPage;
let pform: ProductoFormPage;
let finan: FinancieroFormPage;
let metas: MetasFormPage;

Given('que ingreso al sistema', async () => {
  consulta = new ConsultaPage(page);
  await consulta.login();
});

When('completo los formularios iniciales', async () => {
  form = new FormPage(page);
  await form.completeForm();
  await form.botonSiguiente();
  await form.validateSecondForm();
  await form.botonGuardaryContinuar();
});

When('realizo el formulario personal y regreso', async () => {
  pform = new ProductoFormPage(page);
  await pform.personalFormMayor();
  await pform.botonRegresar();

  // Validación de regreso al formulario anterior
  await expect(page).toHaveURL(/second-formulario/); // Ajusta si cambia la URL
  await form.botonGuardaryContinuar();
  await pform.botonGuardar();
});

When('regreso desde el perfil financiero', async () => {
  finan = new FinancieroFormPage(page);
  await finan.perfilFinanciero();
  await finan.buttonAnterior();

  await expect(page).toHaveURL(/personal-formulario/); // Ajusta si cambia
  await pform.botonGuardar();
  await finan.buttonSiguiente();
});

When('regreso desde las metas financieras', async () => {
  metas = new MetasFormPage(page);
  await metas.metasFinancieras();
  await metas.buttonRegreso();
});

Then('cada regreso debe llevar a la página anterior correctamente', async () => {
  await expect(page).toHaveURL(/financiero/); // Ajusta según el paso actual
});
