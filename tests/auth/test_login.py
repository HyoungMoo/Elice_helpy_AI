import pytest
import allure
from src.pages.auth.login_page import LoginPage
from selenium.webdriver.common.keys import Keys
from src.utils.auth_locators import CommonAuthLocators, LoginLocators
import time
import pyperclip
# 로그인 정보 입력 위해 자동로그인 아닌 fresh_driver 사용
@allure.epic("인증")
@allure.feature("로그인")
@allure.story("정상 로그인")
@allure.title("이메일/비밀번호 입력 후 로그인 성공")
@allure.severity(allure.severity_level.BLOCKER)
def test_login(fresh_driver):
    driver = fresh_driver
    login_page = LoginPage(driver)
    # 1. 로그인 페이지 접속
    login_page.go_to_login_page()
    # 2. 이메일/비밀번호 입력
    # 이메일 :  qa4team0103@elicer.com
    # 비밀번호 : qa4team0103!!
    assert login_page.test_login(
        email = "eunhajeong707@gmail.com",
        password= "qa4team0103!!",
    ), "이메일과 비밀번호를 찾을 수 없습니다"
    # 비밀번호 가리기/보기 아이콘 클릭
    assert login_page.click_toggle_password_visibility(),"비밀번호 가리기/보기 아이콘을 찾을 수 없습니다."
    time.sleep(3)
    # 로그인 버튼 클릭
    assert login_page.click_login_button(),"로그인 실패"

@allure.epic("인증")
@allure.feature("로그인")
@allure.story("비밀번호 복사")
@allure.title("마스킹 상태 비밀번호 복사 확인")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.xfail(reason="비밀번호 복사 기능 Selenium 환경에서 확인 불가")
def test_login_copy_password(fresh_driver):
    driver = fresh_driver
    login_page = LoginPage(driver)
    # 1. 로그인 페이지 접속
    login_page.go_to_login_page()
    assert login_page.test_login(
        email="eunhajeong707@gmail.com",
        password="qa4team0103!!"
    ), "이메일과 비밀번호를 찾을 수 없습니다."
    password_input = driver.find_element(*CommonAuthLocators.PASSWORD_INPUT)
    # copy 이벤트 감지 변수 생성
    driver.execute_script("""
    window.copied = false;
    document.addEventListener('copy', function() {
        window.copied = true;
    });
    """)
    # 비밀번호 필드 선택
    password_input.click()
    password_input.send_keys(Keys.CONTROL,"a")
    password_input.send_keys(Keys.CONTROL,"c")
   # copy 이벤트 발생 여부 확인
    copied = driver.execute_script("return window.copied")

    assert copied == True
