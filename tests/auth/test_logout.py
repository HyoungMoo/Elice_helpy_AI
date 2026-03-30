import pytest
from selenium import webdriver
from src.pages.auth.logout_page import LogoutPage

def test_logout(logged_in_driver):
    driver = logged_in_driver

    logout_page = LogoutPage(driver)

    logout_page.logout()

    # 로그인 자동 완성 기록삭제
    logout_page.remove_history()

    # 다른계정으로 로그인
    logout_page.sign_different_account()
    #driver.quit()
