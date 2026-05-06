import { expect, test } from "@playwright/test";

test("page has correct title", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveTitle("TestPilot AI");
});

test("header eyebrow shows TestPilot AI", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator(".eyebrow")).toHaveText("TestPilot AI");
});

test("test generator form is present", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("form, [role='form']").first()).toBeVisible();
});
