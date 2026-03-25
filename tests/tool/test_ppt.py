import pytest
from src.pages.auth.login_page import LoginPage


def test_login_success(driver):
    driver = driver

    # 1. 로그인 페이지 객체 생성
    login_page = LoginPage(driver)

    # 2. 로그인 페이지 이동
    login_page.go_to_login_page()

    # 3. 로그인 수행
    login_page.login()

    # 4. 로그인 성공 검증
    # 👉 예: URL 변경 or 특정 요소 존재
    #assert "chat" in driver.current_url