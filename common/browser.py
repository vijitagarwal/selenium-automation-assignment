from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


def create_driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    return driver


def wait_for(driver, condition, timeout=15):
    return WebDriverWait(driver, timeout).until(condition)
