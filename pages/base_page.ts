// pages/base_page.ts
import { Page, Locator, expect } from '@playwright/test';

export default class BasePage {
  protected page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async openUrl(url: string) {
    await this.page.goto(url);
  }

  async waitForElement(selector: string, timeout = 30000): Promise<Locator> {
    const locator = this.page.locator(selector);
    await locator.waitFor({ state: 'visible', timeout });
    return locator;
  }

  async clickElement(selector: string) {
    await this.page.locator(selector).click();
  }

  async enterText(selector: string, text: string) {
    const input = this.page.locator(selector);
    await input.waitFor({ state: 'visible' });
    await input.fill(text);
  }

  async scrollIntoView(selector: string) {
    await this.page.locator(selector).scrollIntoViewIfNeeded();
  }

  async selectDropdownOption(dropdownSelector: string, optionText: string) {
    await this.page.locator(dropdownSelector).click();
    await this.page.getByText(optionText, { exact: false }).click();
  }
}
