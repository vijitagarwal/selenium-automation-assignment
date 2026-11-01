import sys
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from common.browser import create_driver, wait_for
from common.config import (
    ADDRESS,
    BASE_URL,
    CITY,
    COUNTRY,
    NAME,
    PASSWORD,
    PHONE,
    PIN_CODE,
    TEST_ACCOUNTS,
)
from common.screenshot import save_screenshot


def click(driver, locator):
    wait_for(driver, EC.element_to_be_clickable(locator)).click()


def visible(driver, locator):
    return wait_for(driver, EC.visibility_of_element_located(locator))


def screenshot(driver, case_dir, number, name):
    save_screenshot(driver, case_dir, f"{number:02d}_{name}.png")


def home(driver, case_dir):
    driver.get(BASE_URL)
    assert "Automation Exercise" in driver.title
    screenshot(driver, case_dir, 1, "homepage")


def signup_account(driver, email):
    click(driver, (By.LINK_TEXT, "Signup / Login"))
    visible(driver, (By.CSS_SELECTOR, "input[data-qa='signup-email']"))
    driver.find_element(By.NAME, "name").send_keys(NAME)
    driver.find_element(By.CSS_SELECTOR, "input[data-qa='signup-email']").send_keys(email)
    click(driver, (By.CSS_SELECTOR, "button[data-qa='signup-button']"))
    try:
        visible(driver, (By.XPATH, "//p[contains(., 'Email Address already exist!')]"), timeout=3)
        driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-email']").send_keys(email)
        driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-password']").send_keys(PASSWORD)
        click(driver, (By.CSS_SELECTOR, "button[data-qa='login-button']"))
        visible(driver, (By.XPATH, "//a[contains(., 'Logged in as')]"))
        return
    except Exception:
        pass
    visible(driver, (By.ID, "id_gender1"))
    driver.find_element(By.ID, "id_gender1").click()
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "days").send_keys("10")
    driver.find_element(By.ID, "months").send_keys("May")
    driver.find_element(By.ID, "years").send_keys("2000")
    driver.find_element(By.ID, "first_name").send_keys("Vijit")
    driver.find_element(By.ID, "last_name").send_keys("Agarwal")
    driver.find_element(By.ID, "address1").send_keys(ADDRESS)
    driver.find_element(By.ID, "country").send_keys(COUNTRY)
    driver.find_element(By.ID, "state").send_keys("Karnataka")
    driver.find_element(By.ID, "city").send_keys(CITY)
    driver.find_element(By.ID, "zipcode").send_keys(PIN_CODE)
    driver.find_element(By.ID, "mobile_number").send_keys(PHONE)
    click(driver, (By.CSS_SELECTOR, "button[data-qa='create-account']"))
    visible(driver, (By.XPATH, "//b[text()='Account Created!']"))
    click(driver, (By.CSS_SELECTOR, "a[data-qa='continue-button']"))
    visible(driver, (By.XPATH, "//a[contains(., 'Logged in as')]"))


def login(driver, email):
    click(driver, (By.LINK_TEXT, "Signup / Login"))
    visible(driver, (By.CSS_SELECTOR, "input[data-qa='login-email']"))
    driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-email']").send_keys(email)
    driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-password']").send_keys(PASSWORD)
    click(driver, (By.CSS_SELECTOR, "button[data-qa='login-button']"))


def add_first_product(driver):
    click(driver, (By.LINK_TEXT, "Products"))
    visible(driver, (By.CSS_SELECTOR, ".productinfo"))
    click(driver, (By.CSS_SELECTOR, ".productinfo a.add-to-cart"))
    visible(driver, (By.XPATH, "//button[contains(., 'Continue Shopping')]"))
    click(driver, (By.XPATH, "//button[contains(., 'Continue Shopping')]"))


def checkout(driver, email=None, register=False):
    home(driver, Path.cwd())
    add_first_product(driver)
    click(driver, (By.LINK_TEXT, "Cart"))
    click(driver, (By.LINK_TEXT, "Proceed To Checkout"))
    if register:
        click(driver, (By.LINK_TEXT, "Register / Login"))
        signup_account(driver, email)
        click(driver, (By.LINK_TEXT, "Cart"))
        click(driver, (By.LINK_TEXT, "Proceed To Checkout"))
    elif email:
        login(driver, email)
        click(driver, (By.LINK_TEXT, "Cart"))
        click(driver, (By.LINK_TEXT, "Proceed To Checkout"))
    visible(driver, (By.ID, "address_delivery"))
    visible(driver, (By.ID, "order_review"))


def run_case(number, name, case_dir):
    driver = create_driver()
    try:
        print(f"Running TC-{number:02d}: {name}")
        if number == 3:
            home(driver, case_dir)
            login(driver, "wrong@example.com")
            driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-password']").send_keys("wrong")
            click(driver, (By.CSS_SELECTOR, "button[data-qa='login-button']"))
            assert visible(driver, (By.XPATH, "//p[contains(., 'Your email or password is incorrect!')]"))
            screenshot(driver, case_dir, 2, "incorrect_login")
        elif number == 4:
            home(driver, case_dir)
            signup_account(driver, TEST_ACCOUNTS["TC04"])
            click(driver, (By.LINK_TEXT, "Logout"))
            assert visible(driver, (By.CSS_SELECTOR, "input[data-qa='login-email']"))
            screenshot(driver, case_dir, 2, "logged_out")
        elif number == 5:
            home(driver, case_dir)
            email = TEST_ACCOUNTS["TC05"]
            signup_account(driver, email)
            click(driver, (By.LINK_TEXT, "Delete Account"))
            visible(driver, (By.XPATH, "//b[text()='Account Deleted!']"))
            driver.get(BASE_URL)
            click(driver, (By.LINK_TEXT, "Signup / Login"))
            driver.find_element(By.NAME, "name").send_keys(NAME)
            driver.find_element(By.CSS_SELECTOR, "input[data-qa='signup-email']").send_keys(email)
            click(driver, (By.CSS_SELECTOR, "button[data-qa='signup-button']"))
            assert visible(driver, (By.XPATH, "//p[contains(., 'Email Address already exist!')]"))
            screenshot(driver, case_dir, 2, "existing_email")
        elif number == 6:
            home(driver, case_dir)
            click(driver, (By.LINK_TEXT, "Contact us"))
            visible(driver, (By.XPATH, "//h2[contains(., 'Get In Touch')]"))
            driver.find_element(By.NAME, "name").send_keys(NAME)
            driver.find_element(By.NAME, "email").send_keys(TEST_ACCOUNTS["TC06"])
            driver.find_element(By.NAME, "subject").send_keys("Assignment contact test")
            driver.find_element(By.ID, "message").send_keys("Automation Exercise contact form test")
            click(driver, (By.NAME, "submit"))
            try:
                driver.switch_to.alert.accept()
            except Exception:
                pass
            assert visible(driver, (By.XPATH, "//*[contains(., 'Success! Your details have been submitted successfully.')]"))
            screenshot(driver, case_dir, 2, "contact_success")
        elif number == 7:
            home(driver, case_dir)
            click(driver, (By.LINK_TEXT, "Test Cases"))
            assert visible(driver, (By.XPATH, "//h2[contains(., 'Test Cases')]"))
            screenshot(driver, case_dir, 2, "test_cases_page")
        elif number == 8:
            home(driver, case_dir)
            click(driver, (By.LINK_TEXT, "Products"))
            assert visible(driver, (By.XPATH, "//h2[contains(., 'All Products')]"))
            click(driver, (By.CSS_SELECTOR, "a[href*='/product_details/1']"))
            assert visible(driver, (By.XPATH, "//div[contains(@class, 'product-information')]"))
            screenshot(driver, case_dir, 2, "product_detail")
        elif number == 9:
            home(driver, case_dir)
            click(driver, (By.LINK_TEXT, "Products"))
            field = visible(driver, (By.ID, "search_product"))
            field.send_keys("Blue Top")
            click(driver, (By.ID, "submit_search"))
            assert visible(driver, (By.XPATH, "//h2[contains(., 'Searched Products')]"))
            assert driver.find_elements(By.XPATH, "//*[contains(., 'Blue Top')]")
            screenshot(driver, case_dir, 2, "search_results")
        elif number == 10:
            home(driver, case_dir)
            field = visible(driver, (By.ID, "susbscribe_email"))
            field.send_keys(TEST_ACCOUNTS["TC10"])
            field.send_keys(Keys.ENTER)
            assert visible(driver, (By.XPATH, "//*[contains(., 'You have been successfully subscribed!')]"))
            screenshot(driver, case_dir, 2, "subscription")
        elif number == 11:
            home(driver, case_dir)
            click(driver, (By.LINK_TEXT, "Cart"))
            field = visible(driver, (By.ID, "susbscribe_email"))
            field.send_keys(TEST_ACCOUNTS["TC11"])
            field.send_keys(Keys.ENTER)
            assert visible(driver, (By.XPATH, "//*[contains(., 'You have been successfully subscribed!')]"))
            screenshot(driver, case_dir, 2, "cart_subscription")
        elif number in (12, 13, 17):
            home(driver, case_dir)
            add_first_product(driver)
            click(driver, (By.LINK_TEXT, "Cart"))
            row = visible(driver, (By.CSS_SELECTOR, "#cart_info_table"))
            if number == 12:
                assert row.is_displayed()
            elif number == 13:
                quantity = visible(driver, (By.CSS_SELECTOR, ".cart_quantity button"))
                assert quantity.text == "1"
            else:
                click(driver, (By.CSS_SELECTOR, ".cart_quantity_delete"))
                assert visible(driver, (By.XPATH, "//b[contains(., 'Cart is empty!')]"))
            screenshot(driver, case_dir, 2, "cart_result")
        elif number in (18, 19):
            home(driver, case_dir)
            if number == 18:
                click(driver, (By.XPATH, "//a[contains(@href, 'category_products/2')]"))
            else:
                click(driver, (By.LINK_TEXT, "Products"))
                click(driver, (By.CSS_SELECTOR, "a[href*='brand_products/Polo']"))
            assert visible(driver, (By.CSS_SELECTOR, ".features_items"))
            screenshot(driver, case_dir, 2, "product_listing")
        elif number == 20:
            home(driver, case_dir)
            click(driver, (By.LINK_TEXT, "Products"))
            visible(driver, (By.ID, "search_product")).send_keys("Blue Top")
            click(driver, (By.ID, "submit_search"))
            click(driver, (By.CSS_SELECTOR, ".productinfo a.add-to-cart"))
            click(driver, (By.XPATH, "//button[contains(., 'Continue Shopping')]"))
            click(driver, (By.LINK_TEXT, "Signup / Login"))
            login(driver, TEST_ACCOUNTS["TC02"])
            click(driver, (By.LINK_TEXT, "Cart"))
            assert visible(driver, (By.CSS_SELECTOR, "#cart_info_table"))
            screenshot(driver, case_dir, 2, "cart_after_login")
        elif number == 21:
            home(driver, case_dir)
            click(driver, (By.LINK_TEXT, "Products"))
            click(driver, (By.CSS_SELECTOR, "a[href*='/product_details/1']"))
            visible(driver, (By.ID, "name")).send_keys(NAME)
            driver.find_element(By.ID, "email").send_keys(TEST_ACCOUNTS["TC21"])
            driver.find_element(By.ID, "review").send_keys("Good product for testing.")
            click(driver, (By.ID, "button-review"))
            assert visible(driver, (By.XPATH, "//*[contains(., 'Thank you for your review.')]"))
            screenshot(driver, case_dir, 2, "review_submitted")
        elif number == 22:
            home(driver, case_dir)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            visible(driver, (By.XPATH, "//*[contains(., 'RECOMMENDED ITEMS')]"))
            click(driver, (By.CSS_SELECTOR, ".recommended_items .add-to-cart"))
            click(driver, (By.XPATH, "//button[contains(., 'Continue Shopping')]"))
            click(driver, (By.LINK_TEXT, "Cart"))
            assert visible(driver, (By.CSS_SELECTOR, "#cart_info_table"))
            screenshot(driver, case_dir, 2, "recommended_cart")
        elif number in (14, 15, 16, 23):
            email = TEST_ACCOUNTS.get(f"TC{number:02d}", TEST_ACCOUNTS["TC02"])
            if number == 14:
                checkout(driver, email=email, register=True)
            elif number == 16:
                checkout(driver, email=TEST_ACCOUNTS["TC02"])
            else:
                signup_account(driver, email)
                click(driver, (By.LINK_TEXT, "Cart"))
                click(driver, (By.LINK_TEXT, "Proceed To Checkout"))
                visible(driver, (By.ID, "address_delivery"))
                visible(driver, (By.ID, "order_review"))
            assert ADDRESS in driver.find_element(By.ID, "address_delivery").text
            screenshot(driver, case_dir, 2, "checkout_address")
        elif number == 24:
            checkout(driver, email=TEST_ACCOUNTS["TC02"])
            driver.find_element(By.NAME, "message").send_keys("Invoice test order")
            click(driver, (By.LINK_TEXT, "Place Order"))
            visible(driver, (By.NAME, "name_on_card")).send_keys(NAME)
            driver.find_element(By.NAME, "card_number").send_keys("4111111111111111")
            driver.find_element(By.NAME, "cvc").send_keys("123")
            driver.find_element(By.NAME, "expiry_month").send_keys("12")
            driver.find_element(By.NAME, "expiry_year").send_keys("2030")
            click(driver, (By.ID, "submit"))
            visible(driver, (By.XPATH, "//b[contains(., 'Order Placed!')]"))
            click(driver, (By.LINK_TEXT, "Download Invoice"))
            screenshot(driver, case_dir, 2, "invoice_download")
        elif number in (25, 26):
            home(driver, case_dir)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            visible(driver, (By.XPATH, "//*[contains(., 'SUBSCRIPTION')]"))
            assert driver.execute_script("return window.scrollY") > 0
            if number == 25:
                click(driver, (By.ID, "scrollUp"))
            else:
                driver.execute_script("window.scrollTo(0, 0)")
            assert driver.execute_script("return window.scrollY") == 0
            screenshot(driver, case_dir, 2, "scroll_top")
        else:
            raise NotImplementedError(f"Checkout flow TC-{number:02d} needs live payment execution.")
        print("RESULT: PASSED")
    except Exception:
        screenshot(driver, case_dir, 99, "failure_state")
        raise
    finally:
        driver.quit()


if __name__ == "__main__":
    run_case(int(sys.argv[1]), sys.argv[2], Path.cwd())
