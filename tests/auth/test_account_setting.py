import pytest
import time
from selenium import webdriver
from src.pages.auth.accountsetting_page import AccountSetting
from src.pages.auth.login_page import LoginPage
# pytest tests/auth/test_account_setting.py
def test_account_setting(logged_in_driver):
    driver = logged_in_driver

    account_setting = AccountSetting(driver)

    # 계정 관리 페이지 이동
    account_setting.go_to_account_setting()
    time.sleep(1)
    
    # 프로필 이미지 변경
    account_setting.change_profile_image()
    account_setting.refresh() #새로고침
    time.sleep(1)
    
    # 프로필 이미지 삭제
    account_setting.delete_profile_image()
    account_setting.refresh() #새로고침
    time.sleep(1)
    
    # 이름 변경
    account_setting.change_name("엘리스")

    time.sleep(1)
    # 비밀번호 변경 (현재비밀번호, 새비밀번호, 새비밀번호확인)
    # account_setting.change_password(logged_in_driver.current_password,"qa4team0202!!","qa4team0202!!")
    
    # 선호 언어 변경
    account_setting.change_language()

