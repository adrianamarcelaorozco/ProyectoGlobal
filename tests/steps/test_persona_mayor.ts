import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from '@playwright/test';
import ConsultaPage from '../../pages/consulta_page';
import {FormPage} from '../../pages/form_page';
import PersonalFormPage from '../../pages/personal_form_page';
import { FinancieroFormPage } from '../../pages/financiero_page';
import { MetasFormPage } from '../../pages/metas_pages';
import { CotizarFormPage } from '../../pages/cotizar_page';

let consulta: ConsultaPage;
let form: FormPage;
let pform: PersonalFormPage;
let finan: FinancieroFormPage;
let metas: MetasFormPage;
let cotizarPage: CotizarFormPage;


When('completo los formularios iniciales como persona mayor', async function () {
  form = new FormPage(this.page);
  await form.completeForm();
  await form.botonSiguiente();
  await form.validateSecondForm();
  await form.botonGuardaryContinuar();

});

When('realizo el formulario como persona mayor y continuo', async function () {

  pform = new PersonalFormPage(this.page);
  await pform.completarFormularioMayor();
  await pform.clickGuardar();
});

When('completo el perfil financiero como persona mayor y continuo', async function () {
  finan = new FinancieroFormPage(this.page);
  await finan.perfilFinanciero();
  await finan.buttonSiguiente();
});

When('defino mis metas financieras como persona mayor y continuo', async function () {
  metas = new MetasFormPage(this.page);
  await metas.metasFinancieras();
  await metas.buttonCotizar();
});

When('realizo la cotización', async function () {
  cotizarPage = new CotizarFormPage(this.page);
  await cotizarPage.datosAsegurado();
  await cotizarPage.datosBeneficiario();
  await cotizarPage.botonGuardar();
});

Then('debería poder simular diferentes productos y finalizar correctamente', async function () {
  await cotizarPage.datosColegio();
  await cotizarPage.botonGuardar(); // o el método que finaliza la simulación si tienes uno
});