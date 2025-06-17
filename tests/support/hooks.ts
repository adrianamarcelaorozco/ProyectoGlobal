import { BeforeAll, AfterAll } from "@cucumber/cucumber";
import { chromium, Browser, Page } from "playwright";

let browser: Browser;
export let page: Page;

BeforeAll(async () => {
  browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  page = await context.newPage();
});

AfterAll(async () => {
  await browser.close();
});