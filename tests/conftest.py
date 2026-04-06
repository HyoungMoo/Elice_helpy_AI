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
    options.add_argument("--no-sandbox")           # CI 리눅스 환경 필수
    options.add_argument("--disable-dev-shm-usage") # 공유 메모리 부족 방지
    options.add_argument("--disable-gpu")
    # detach=True 제거: CI에서 Chrome 프로세스가 테스트 종료 후에도 남아 메모리 누수 유발

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
    login_page.login("user_2")
    return driver

@pytest.fixture
def fresh_driver(driver):
    return driver