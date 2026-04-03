import pytest
from selenium import webdriver
from src.pages.auth.logout_page import LogoutPage
from selenium.webdriver.common.by import By
from src.pages.auth.login_page import LoginPage
from src.pages.auth.accountsetting_page import AccountSetting
# pytest tests/auth/test_logout.py

# 로그아웃 후 다른 계정으로 로그인
def test_logout_after_other_auth_login(logged_in_driver):
    driver = logged_in_driver
    logout_page = LogoutPage(driver)
    login_page = LoginPage(driver)    
    logout_page.logout()

    # 다른계정으로 로그인
    logout_page.sign_different_account( )
    login_page.login()

# 로그인 자동 완성 기록 삭제
def test_logout_remove_history(logged_in_driver):
    driver = logged_in_driver
    logout_page = LogoutPage(driver)
    accountsetting_page = AccountSetting(driver)
    logout_page.logout()

    # 로그인 자동 완성기록삭제
    accountsetting_page.change_language_to_korean()
    logout_page.remove_history()
