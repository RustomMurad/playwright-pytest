from playwright.sync_api import Playwright, expect
import time

def test_ui_checks(playwright: Playwright, pytestconfig):
    headed = pytestconfig.getoption("--headed")
    browser = playwright.chromium.launch(headless=not headed)
    context = browser.new_context()
    page = context.new_page()

    # hide/show placeholder
    page.goto('https://rahulshettyacademy.com/AutomationPractice/')
    hide_show_placeholder = page.get_by_placeholder('Hide/Show Example')
    expect(hide_show_placeholder).to_be_visible()
    page.get_by_role('button', name='Hide').click()
    expect(page.get_by_placeholder('Hide/Show Example')).to_be_hidden()

    # Allert handling - accept
    page.on('dialog', lambda dialog: dialog.accept())
    page.get_by_role('button', name='Confirm').click()

    # Mouse hover
    page.locator('#mousehover').hover()
    page.get_by_role('link', name='Top')

    # IFrame handling
    iframe_page = page.frame_locator("#courses-iframe")
    iframe_page.get_by_role('link',name="All Access Plan").click()
    expect(iframe_page.locator('body')).to_contain_text('Happy Subscibers')

    # Check price of rice is equal to 37.
    page.goto('https://rahulshettyacademy.com/seleniumPractise/#/offers')
    for index in range(page.locator('th').count()):
        if page.locator('th').nth(index).filter(has_text='Price').count() > 0:
            price_colomn_index = index
            print(f"Price column index is {price_colomn_index}")
            break
    rice_row = page.locator('tr').filter(has_text='Rice')
    expect(rice_row.locator('td').nth(price_colomn_index), "Rice price isn't mach 37").to_have_text('37')

    time.sleep(2)