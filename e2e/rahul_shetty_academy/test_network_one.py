from playwright.sync_api import Playwright, expect

fake_payload_order_response = {"data":[], "message": "No orders"}

def intercept_response(route):
    route.fulfill(
        json = fake_payload_order_response
    )

def test_network_one(playwright: Playwright, pytestconfig):
    headed = pytestconfig.getoption("--headed")
    browser = playwright.chromium.launch(headless=not headed)
    context=browser.new_context()
    page=context.new_page()

    page.goto('https://rahulshettyacademy.com/client')
    page.route('https://rahulshettyacademy.com/api/ecom/order/get-orders-for-customer/*', intercept_response)
    page.get_by_placeholder('email@example.com').fill('rahulshetty@gmail.com')
    page.get_by_placeholder('enter your passsword').fill('Iamking@000')
    page.get_by_role('button', name='Login').click()
    page.get_by_role('button', name='ORDERS').click()

    order_text = page.locator('.mt-4').text_content()
    print(order_text)