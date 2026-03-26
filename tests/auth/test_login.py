import pytest
from src.pages.auth.login_page import LoginPage
from selenium.webdriver.common.keys import Keys
import time
# 로그인 정보 입력 위해 fresh_driver 사용
def test_login(fresh_driver):
    driver = fresh_driver
    login_page = LoginPage(driver)

    # 1. 로그인 페이지 접속 
    login_page.go_to_login_page()

    # 2. 이메일/비밀번호 입력
    # 이메일 :  qa4team0103@elicer.com
    # 비밀번호 : qa4team0103!!
    assert login_page.test_login(
        email = "qa4team0103@elicer.com",
        password= "qa4team0103!!",
    ), "이메일과 비밀번호를 찾을 수 없습니다"


    # 비밀번호 가리기/보기 아이콘 클릭
    assert login_page.click_toggle_password_visibility(),"비밀번호 가리기/보기 아이콘을 찾을 수 없습니다."
    time.sleep(3)
    # 로그인 버튼 클릭
    assert login_page.click_login_button(),"로그인 실패"

    