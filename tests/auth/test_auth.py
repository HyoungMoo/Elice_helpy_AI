import pytest
from src.pages.auth.signup_page import SignupPage
from src.pages.auth.accountsetting_page import AccountSetting
def test_signup_email_button_opens_form(fresh_driver):
    
    driver = fresh_driver
    signup_page = SignupPage(driver)
    account_setting = AccountSetting(driver)
    # 1. 회원가입 페이지로 이동
    signup_page.go_to_signup_page()
    account_setting.change_language_to_korean()
    # 2. '이메일로 가입하기' 버튼 클릭
    assert signup_page.click_signup_with_email(), "'이메일로 가입하기' 버튼을 찾을 수 없습니다."

    # 3. 회원가입 폼 화면 표시 확인
    assert signup_page.is_signup_form_displayed(), "회원가입 폼이 화면에 표시되지 않습니다."

    # 4. 이메일, 비밀번호, 이름 입력
    # 이메일  qa4team0106@elicer.com
    # 비밀번호 qa4team0106!!
    # 이름 정은하회원가입테스트
    assert signup_page.fill_signup_form(
        email="qa4team1234@elicer.com",
        password="qa4team1234!!",
        name="정은하회원가입테스트"
    ), "회원가입 폼 입력 실패"
    # 5. 전체 동의 체크
    assert signup_page.click_agree_all_checkbox(), "'전체동의' 체크박스를 찾을 수 없습니다."

    #6. 회원가입 버튼 클릭
    assert signup_page.click_signup_button(),"'회원가입'버튼을 찾을 수 없습니다."
    