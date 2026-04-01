import pytest
import time
from selenium import webdriver
from src.pages.auth.accountsetting_page import AccountSetting
from src.pages.auth.login_page import LoginPage
from src.pages.auth.signup_page import SignupPage


# 계정탈퇴 테스트
# 테스트 계정 qa4team9999@elicer.com
# 테스트 비밀번호 qa4team9999!!
# 계정탈퇴 테스트로 테스트 수행 시 임시 계정 생성 필요
# 테스트 재수행 시 테스트 계정 신규 가입 필요
# 아래 코드는 가입부터 탈퇴까지 진행 
# pytest tests/auth/test_account_withdrawal.py
def test_account_withdrawal(fresh_driver):
    driver = fresh_driver
    
    signup_page = SignupPage(driver)
    account_setting = AccountSetting(driver)

    # 1. 계정탈퇴용 테스트 계정 생성 - 회원가입 페이지 이동
    signup_page.go_to_signup_page()
    account_setting.change_language_to_korean()
    # 2. 계정탈퇴용 테스트 계정 생성 - '이메일로 가입하기' 버튼 클릭
    assert signup_page.click_signup_with_email(), "'이메일로 가입하기' 버튼을 찾을 수 없습니다."
    # 3. 계정탈퇴용 테스트 계정 생성 -  회원가입 폼 화면 표시 확인
    assert signup_page.is_signup_form_displayed(), "회원가입 폼이 화면에 표시되지 않습니다."
    # 4. 이메일 , 비밀번호, 이름 입력
    # 테스트 계정 qa4team9999@elicer.com
    # 테스트 비밀번호 qa4team9999!!
    # 이름 계정탈퇴용 테스트
    assert signup_page.fill_signup_form(
        email="qa4team9999@elicer.com",
        password="qa4team9999!",
        name="계정탈퇴용 테스트"
    ), "회원가입 폼 입력 실패"
    # 5. 계정탈퇴용 테스트 계정 생성 - 전체 동의 체크
    assert signup_page.click_agree_all_checkbox(), "'전체동의' 체크박스를 찾을 수 없습니다."
    #6. 계정탈퇴용 테스트 계정 생성 - 회원가입 버튼 클릭
    assert signup_page.click_signup_button(),"'회원가입'버튼을 찾을 수 없습니다."

    #7. 계정 관리 페이지 이동
    account_setting.go_to_account_setting()
    time.sleep(1)

    #8. 계정 탈퇴 '탈퇴하기' 버튼 클릭
    account_setting.account_withdrawal("qa4team9999@elicer.com")