from playwright.sync_api import Playwright, expect
from utils.api_utils import APIUtils
import time

def test_session_storage(playwright: Playwright, pytestconfig):
    api_utils = APIUtils()
    token = api_utils.get_token(playwright)
    headed = pytestconfig.getoption("--headed")
    browser = playwright.chromium.launch(headless=not headed)
    context=browser.new_context()
    page=context.new_page()

    # script to inject token in session local store
    page.add_init_script(f"""localStorage.setItem('token','{token}')""")
    page.goto('https://rahulshettyacademy.com/client')
    page.get_by_role('button', name='ORDERS').click()
    expect(page.get_by_text('Your Orders')).to_be_visible()
    time.sleep(5)