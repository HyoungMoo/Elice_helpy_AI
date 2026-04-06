from pathlib import Path
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.pages.auth.login_page import LoginPage

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    #options.add_argument('--start-maximized')          # 브라우저 창을 시작 시 최대화
    options.add_experimental_option("detach", True)

    download_path = str(Path("reports/downloads").resolve())

    options.add_experimental_option("prefs", {
        "profile.content_settings.exceptions.clipboard": {
            "*": {"setting": 1}
        },
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
    })

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    try:
        driver.quit()
    except Exception:
        pass

@pytest.fixture
def logged_in_driver(driver):
    login_page = LoginPage(driver)
    login_page.go_to_login_page()
    login_page.login("user_2") # 각자 계정 입력
    return driver

@pytest.fixture
def fresh_driver(driver):
    return driver