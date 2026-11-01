import sys
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

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


CASE_DIR = Path(__file__).resolve().parent


def run():
    driver = create_driver()
    try:
        print("Running TC-02: Login User with correct credentials")
        driver.get(BASE_URL)
        driver.find_element(By.LINK_TEXT, "Signup / Login").click()
        wait_for(driver, EC.visibility_of_element_located((By.CSS_SELECTOR, "input[data-qa='login-email']")))
        save_screenshot(driver, CASE_DIR, "01_login_page.png")
        email = TEST_ACCOUNTS["TC02"]

        driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-email']").send_keys(email)
        driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-password']").send_keys(PASSWORD)
        driver.find_element(By.CSS_SELECTOR, "button[data-qa='login-button']").click()
        try:
            logged_in = wait_for(
                driver,
                EC.visibility_of_element_located((By.XPATH, "//a[contains(., 'Logged in as')]")),
                timeout=5,
            )
            save_screenshot(driver, CASE_DIR, "03_login_success.png")
            assert logged_in.is_displayed()
            print("RESULT: PASSED")
            return
        except Exception:
            driver.get(BASE_URL)
            driver.find_element(By.LINK_TEXT, "Signup / Login").click()
            wait_for(driver, EC.visibility_of_element_located((By.CSS_SELECTOR, "input[data-qa='signup-email']")))

        # Create the independent account needed by this login test.
        driver.find_element(By.NAME, "name").send_keys(NAME)
        driver.find_element(By.CSS_SELECTOR, "input[data-qa='signup-email']").send_keys(email)
        driver.find_element(By.CSS_SELECTOR, "button[data-qa='signup-button']").click()
        wait_for(driver, EC.visibility_of_element_located((By.ID, "id_gender1")))
        driver.find_element(By.ID, "id_gender1").click()
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.ID, "days").send_keys("10")
        driver.find_element(By.ID, "months").send_keys("May")
        driver.find_element(By.ID, "years").send_keys("2000")
        driver.find_element(By.ID, "first_name").send_keys(NAME.split()[0])
        driver.find_element(By.ID, "last_name").send_keys(NAME.split()[-1])
        driver.find_element(By.ID, "address1").send_keys(ADDRESS)
        driver.find_element(By.ID, "country").send_keys(COUNTRY)
        driver.find_element(By.ID, "state").send_keys("Karnataka")
        driver.find_element(By.ID, "city").send_keys(CITY)
        driver.find_element(By.ID, "zipcode").send_keys(PIN_CODE)
        driver.find_element(By.ID, "mobile_number").send_keys(PHONE)
        driver.find_element(By.CSS_SELECTOR, "button[data-qa='create-account']").click()
        wait_for(driver, EC.visibility_of_element_located((By.XPATH, "//b[text()='Account Created!']")))
        driver.find_element(By.CSS_SELECTOR, "a[data-qa='continue-button']").click()
        wait_for(driver, EC.visibility_of_element_located((By.XPATH, "//a[contains(., 'Logged in as')]")))
        driver.find_element(By.LINK_TEXT, "Logout").click()
        wait_for(driver, EC.visibility_of_element_located((By.CSS_SELECTOR, "input[data-qa='login-email']")))

        driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-email']").send_keys(email)
        driver.find_element(By.CSS_SELECTOR, "input[data-qa='login-password']").send_keys(PASSWORD)
        save_screenshot(driver, CASE_DIR, "02_credentials_entered.png")
        driver.find_element(By.CSS_SELECTOR, "button[data-qa='login-button']").click()

        logged_in = wait_for(driver, EC.visibility_of_element_located((By.XPATH, "//a[contains(., 'Logged in as')]")))
        save_screenshot(driver, CASE_DIR, "03_login_success.png")
        assert logged_in.is_displayed()
        print("RESULT: PASSED")
    except Exception:
        save_screenshot(driver, CASE_DIR, "99_failure_state.png")
        raise
    finally:
        driver.quit()


if __name__ == "__main__":
    run()
