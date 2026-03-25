import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.pages.auth.login_page import LoginPage

@pytest.fixture
def driver():
    options = Options()
    #options.add_argument("--headless")
    options.add_experimental_option("detach", True) 
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    #driver.quit()

@pytest.fixture
def logged_in_driver(driver):
    login_page = LoginPage(driver)
    login_page.go()
    login_page.login("user_1")  # 여기서 원하는 계정 선택
    return driver