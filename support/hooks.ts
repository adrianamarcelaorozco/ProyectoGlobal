// tests/support/hooks.ts
import { Before, After, setDefaultTimeout } from '@cucumber/cucumber';
import { chromium, Browser, Page } from '@playwright/test';

let browser: Browser;
export let page: Page; // ✅ este es el que estás usando

setDefaultTimeout(60 * 1000);

Before(async () => {
  browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    viewport: { width: 1300, height: 800 }, // 👈 resolución ideal para MacBook Air
  });
  page = await context.newPage();
});

After(async () => {
  await page.close();
  await browser.close();
});
