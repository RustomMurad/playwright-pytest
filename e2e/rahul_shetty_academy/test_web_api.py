from playwright.sync_api import Playwright, expect
from utils.api_utils import APIUtils

def test_e2e_web_api(playwright: Playwright, pytestconfig):
    headed = pytestconfig.getoption("--headed")
    browser = playwright.chromium.launch(headless=not headed)
    context=browser.new_context()
    page=context.new_page()

    # Create order -> orderId
    api_utils = APIUtils()
    order_id = api_utils.create_order(playwright)


    # Login
    page.goto('https://rahulshettyacademy.com/client')
    page.get_by_placeholder('email@example.com').fill('rahulshetty@gmail.com')
    page.get_by_placeholder('enter your passsword').fill('Iamking@000')
    page.get_by_role('button', name='Login').click()
    page.get_by_role('button', name='ORDERS').click()

    #Orders History page - order is present
    row=page.locator('tr').filter(has_text=order_id)
    row.get_by_role('button',name='View').click()
    expect(page.locator('.tagline')).to_contain_text('Thank you')
    context.close()

    