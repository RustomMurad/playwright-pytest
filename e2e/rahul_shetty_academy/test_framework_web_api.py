import json
import pytest
from playwright.sync_api import Playwright, expect
from page_objects.login import LoginPage
from utils.api_framework_utils import APIUtils

# JSON -> util -> access into test
with open('data/credentials.json') as f:
    test_data = json.load(f)
    print(test_data)
    user_credentials_list = test_data['user_credentials']

@pytest.mark.parametrize('user_credentials', user_credentials_list)
def test_e2e_web_api(playwright: Playwright, pytestconfig, user_credentials):
    user_email = user_credentials['user_email']
    user_password = user_credentials['user_password']
    headed = pytestconfig.getoption("--headed")
    browser = playwright.chromium.launch(headless=not headed)
    context=browser.new_context()
    page=context.new_page()

    # Create order -> orderId
    api_utils = APIUtils()
    order_id = api_utils.create_order(playwright, user_credentials)

    # Login
    login_page = LoginPage(page)
    login_page.navigate()
    # Dashboard
    dashboard_page = login_page.login(user_email, user_password)
    # Orders History
    order_history_page = dashboard_page.select_orders_nav_link()
    # Order Details 
    order_details_page=order_history_page.selectOrder(order_id)
    order_details_page.verify_order_message()
    context.close()
