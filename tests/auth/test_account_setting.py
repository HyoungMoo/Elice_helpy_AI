import pytest
from selenium import webdriver
from src.pages.auth.accountsetting_page import AccountSetting
# pytest tests/auth/test_account_setting.py
def test_account_setting(logged_in_driver):
    driver = logged_in_driver

    account_setting = AccountSetting(driver)

    # 계정 관리 페이지 이동
    account_setting.go_to_account_setting()

    
    # # 이름 변경 (실패)
    account = AccountSetting(driver)
    account.go_to_account_setting()
    account.change_name("엘리스")

    # # 프로필 이미지 변경 (실패)
    # account_setting.profile_icon_set()

   