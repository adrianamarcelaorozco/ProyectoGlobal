import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from '@playwright/test';
import ConsultaPage from '../../pages/consulta_page';
import {FormPage} from '../../pages/form_page';
import PersonalFormPage from '../../pages/personal_form_page';
import { FinancieroFormPage } from '../../pages/financiero_page';
import { MetasFormPage } from '../../pages/metas_pages';

let consulta: ConsultaPage;
let form: FormPage;
let pform: PersonalFormPage;
let finan: FinancieroFormPage;
let metas: MetasFormPage;

Given('que ingreso al sistema', async function () {
  consulta = new ConsultaPage(this.page); // 👈 usa this.page
  await consulta.login();
});

When('completo los formularios iniciales', async function () {
  form = new FormPage(this.page);
  await form.completeForm();
  await form.botonSiguiente();
  await form.validateSecondForm();
  await form.botonGuardaryContinuar();
});

When('realizo el formulario personal y regreso', async function () {
  pform = new PersonalFormPage(this.page);
  await pform.completarFormularioMayor();
  await pform.clickRegresar();

  // Validación de regreso al formulario anterior
  await expect(this.page).toHaveURL('https://globalseguros--qaonb.sandbox.lightning.force.com/lightning/cmp/vlocity_ins__vlocityLWCOmniWrapper?c__target=c%3AgsvFormularyEnglish&c__layout=lightning&c__tabLabel=Perfilamiento');
  await form.botonGuardaryContinuar();
  await pform.clickGuardar();
});

When('regreso desde el perfil financiero', async function () {
  finan = new FinancieroFormPage(this.page);
  await finan.perfilFinanciero();
  await finan.buttonAnterior();

  await expect(this.page).toHaveURL('https://globalseguros--qaonb.sandbox.lightning.force.com/lightning/cmp/vlocity_ins__vlocityLWCOmniWrapper?c__target=c%3AgsvFormularyEnglish&c__layout=lightning&c__tabLabel=Perfilamiento');
  await pform.clickGuardar();
  await finan.buttonSiguiente();
});

When('regreso desde las metas financieras', async function () {
  metas = new MetasFormPage(this.page);
  await metas.metasFinancieras();
  await metas.RegresarAlPerfilamiento();
});

Then('cada regreso debe llevar a la página anterior correctamente', async function () {
  await expect(this.page).toHaveURL(/vlocityLWCOmniWrapper.*c__target=c%3AgsvFormularyEnglish/);
});