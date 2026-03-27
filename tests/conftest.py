import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.pages.auth.login_page import LoginPage

@pytest.fixture
def driver():
    options = Options()

    #options.add_argument("--headless")
    #options.add_argument("--window-size=1920,1080")

    options.add_experimental_option("detach", True)

    # 클립보드 권한 허용 (복사 버튼이 클립보드에 정상적으로 쓸 수 있도록)
    options.add_experimental_option("prefs", {
        "profile.content_settings.exceptions.clipboard": {
            "*": {"setting": 1}
        }
    })

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    #driver.quit()

@pytest.fixture
def logged_in_driver(driver):
    login_page = LoginPage(driver)
    login_page.go_to_login_page()
    login_page.login("user_3")
    return driver

@pytest.fixture
def fresh_driver(driver):
    return driver