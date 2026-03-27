import pytest
from selenium import webdriver
from src.pages.auth.logout_page import LogoutPage

def test_logout_sync(logged_in_driver):
    driver = logged_in_driver

    logout_page = LogoutPage(driver)

    # 다중 탭 로그아웃 동기화 테스트 실행
    logout_page.test_logout_sync()