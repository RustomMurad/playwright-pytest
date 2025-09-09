import time
from playwright.sync_api import Playwright, expect


def test_playwright_basic(playwright: Playwright,pytestconfig):
    headed = pytestconfig.getoption("--headed")
    browser = playwright.chromium.launch(headless=not headed)
    context = browser.new_context()
    page = context.new_page()
    page.goto('https://rahulshettyacademy.com/loginpagePractise/')
    page.get_by_label('Username:').fill('rahulshettyacademy')
    page.get_by_label('Password:').fill('learning')
    page.get_by_role('combobox').select_option('teach')
    page.locator('#terms').check()
    page.get_by_role('link',name='terms and conditions').click()
    page.get_by_role('button',name='Sign In').click()
    iphone_product = page.locator('app-card').filter(has_text='iphone X')
    iphone_product.get_by_role('button').click()
    nokia_product = page.locator('app-card').filter(has_text='Nokia Edge')
    nokia_product.get_by_role('button').click()
    page.get_by_text('Checkout').click()
    expect(page.locator('.media-body'),'Product count in checkout should be equal 2!').to_have_count(2)