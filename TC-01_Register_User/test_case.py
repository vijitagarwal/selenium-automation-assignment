import sys
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.browser import create_driver, wait_for
from common.config import BASE_URL, CITY, COUNTRY, NAME, PASSWORD, PHONE, PIN_CODE, ADDRESS, TEST_ACCOUNTS
from common.screenshot import save_screenshot


CASE_DIR = Path(__file__).resolve().parent


def run():
    driver = create_driver()
    email = TEST_ACCOUNTS["TC01"]
    try:
        print("Running TC-01: Register User")
        driver.get(BASE_URL)
        save_screenshot(driver, CASE_DIR, "01_homepage.png")
        assert "Automation Exercise" in driver.title

        driver.find_element(By.LINK_TEXT, "Signup / Login").click()
        wait_for(driver, EC.visibility_of_element_located((By.XPATH, "//h2[text()='New User Signup!']")))
        save_screenshot(driver, CASE_DIR, "02_signup_page.png")
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
        save_screenshot(driver, CASE_DIR, "03_registration_form.png")
        driver.find_element(By.CSS_SELECTOR, "button[data-qa='create-account']").click()

        wait_for(driver, EC.visibility_of_element_located((By.XPATH, "//b[text()='Account Created!']")))
        save_screenshot(driver, CASE_DIR, "04_account_created.png")
        assert driver.find_element(By.XPATH, "//b[text()='Account Created!']").is_displayed()
        print("Account created successfully.")

        driver.find_element(By.CSS_SELECTOR, "a[data-qa='continue-button']").click()
        wait_for(driver, EC.visibility_of_element_located((By.XPATH, f"//a[contains(., 'Logged in as')]")))
        driver.find_element(By.LINK_TEXT, "Delete Account").click()
        wait_for(driver, EC.visibility_of_element_located((By.XPATH, "//b[text()='Account Deleted!']")))
        save_screenshot(driver, CASE_DIR, "05_account_deleted.png")
        assert driver.find_element(By.XPATH, "//b[text()='Account Deleted!']").is_displayed()
        print("RESULT: PASSED")
    finally:
        driver.quit()


if __name__ == "__main__":
    run()
