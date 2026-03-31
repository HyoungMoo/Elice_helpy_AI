import pytest
from selenium import webdriver
from src.pages.auth.logout_page import LogoutPage
from selenium.webdriver.common.by import By
from src.pages.auth.login_page import LoginPage

def test_logout(logged_in_driver):
    driver = logged_in_driver

    logout_page = LogoutPage(driver)
    login_page = LoginPage(driver)    
    logout_page.logout()

    # # 로그인 자동 완성기록삭제
    # logout_page.remove_history()

    # 다른계정으로 로그인
    logout_page.sign_different_account( )
    login_page.login()

