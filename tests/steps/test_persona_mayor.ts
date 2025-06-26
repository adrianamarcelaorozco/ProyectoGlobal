import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from '@playwright/test';
import { page} from '../../support/hooks';
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


Given('que ingreso al sistema como persona mayor', async function () {
  consulta = new ConsultaPage(this.page);
  await consulta.login();
});

When('completo los formularios como persona mayor', async function () {
  form = new FormPage(this.page);
  await form.completeForm();
  await form.botonSiguiente();
  await form.validateSecondForm();
  await form.botonGuardaryContinuar();

  pform = new PersonalFormPage(this.page);
  await pform.completarFormularioMayor();
  await pform.clickGuardar();

  finan = new FinancieroFormPage(page);
  await finan.perfilFinanciero();
  await finan.buttonSiguiente();

  metas = new MetasFormPage(page);
  await metas.metasFinancieras();
  await metas.buttonCotizar();
});

Then('se completa el proceso de cotización de persona mayor', async function () {
  cotizarPage = new CotizarFormPage(this.page);
  await cotizarPage.datosAsegurado();
  await cotizarPage.datosBeneficiario();
  await cotizarPage.botonGuardar();
  await cotizarPage.datosColegio();
  await cotizarPage.botonGuardar();
});
