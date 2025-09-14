from playwright.sync_api import Playwright, expect, Route
import time

def intercept_response(route: Route):
    route.continue_(url='https://rahulshettyacademy.com/api/ecom/order/get-orders-details?id=6711e249ae2afd4c0b9f6fb0')

def test_network_one(playwright: Playwright, pytestconfig):
    headed = pytestconfig.getoption("--headed")
    browser = playwright.chromium.launch(headless=not headed)
    context=browser.new_context()
    page=context.new_page()

    page.goto('https://rahulshettyacademy.com/client')
    page.route('https://rahulshettyacademy.com/api/ecom/order/get-orders-details?id=*', intercept_response)
    page.get_by_placeholder('email@example.com').fill('rahulshetty@gmail.com')
    page.get_by_placeholder('enter your passsword').fill('Iamking@000')
    page.get_by_role('button', name='Login').click()
    page.get_by_role('button', name='ORDERS').click()
    page.get_by_role('button', name='View').first.click()
    message = page.locator('.blink_me').text_content()
    print(message)

