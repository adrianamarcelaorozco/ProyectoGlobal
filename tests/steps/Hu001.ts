import { Given, When, Then } from "@cucumber/cucumber";
import assert from "assert";
import { page } from "../support/hooks";

Given("el usuario abre la página del formulario local", async () => {
  await page.goto("https://dev-6il01yl7.us.auth0.com/samlp/rnIY9rO6oQyEe3196S9kID4yhuio1PVh");
});

When("llena el campo {string} con {string}", async (campo: string, valor: string) => {
  await page.fill(`input[name="${campo}"]`, valor);
});

When("hace clic en el botón {string}", async (boton: string) => {
  await page.click(`button:text("${boton}")`);
});

Then("debería ver el mensaje {string}", async (mensaje: string) => {
  const locator = page.locator(`text=${mensaje}`);
  const visible = await locator.isVisible();
  assert(visible, `El mensaje "${mensaje}" no es visible`);
});