import json
import pytest
from playwright.sync_api import Playwright, expect
from utils.api_framework_utils import APIUtils

# JSON -> util -> access into test
with open('data/credentials.json') as f:
    test_data = json.load(f)
    print(test_data)
    user_credentials_list = test_data['user_credentials']

@pytest.mark.parametrize('user_credentials', user_credentials_list)
def test_e2e_web_api(playwright: Playwright, pytestconfig, user_credentials):
    headed = pytestconfig.getoption("--headed")
    browser = playwright.chromium.launch(headless=not headed)
    context=browser.new_context()
    page=context.new_page()

    # Create order -> orderId
    api_utils = APIUtils()
    order_id = api_utils.create_order(playwright, user_credentials)

    # Login
    page.goto('https://rahulshettyacademy.com/client')
    page.get_by_placeholder('email@example.com').fill(user_credentials['user_email'])
    page.get_by_placeholder('enter your passsword').fill(user_credentials['user_password'])
    page.get_by_role('button', name='Login').click()
    page.get_by_role('button', name='ORDERS').click()

    #Orders History page - order is present
    row=page.locator('tr').filter(has_text=order_id)
    expect(row).to_be_visible(timeout=30000)
    row.get_by_role('button',name='View').click()
    expect(page.locator('.tagline')).to_contain_text('Thank you')
    context.close()
