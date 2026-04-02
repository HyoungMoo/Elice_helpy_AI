# signup_page.py
from src.config import Config
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from src.utils.auth_locators import CommonAuthLocators, SignupLocators

import logging
logger = logging.getLogger(__name__)


class SignupPage:
    URL = "https://accounts.elice.io/accounts/signup/method?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat&lang=en-US&org=qaproject"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # 회원가입 페이지로 이동
    def go_to_signup_page(self):
        self.driver.get(self.URL)

    # '이메일로 가입하기' 버튼 클릭
    def click_signup_with_email(self):
        try:
            btn = self.wait.until(
                EC.element_to_be_clickable(SignupLocators.SIGNUP_WITH_EMAIL_BTN)
            )
            btn.click()
            logger.info("이메일로 가입하기 버튼 클릭 성공")
            return True
        except (TimeoutException, NoSuchElementException):
            logger.error("이메일로 가입하기 버튼을 찾지 못했습니다.")
            return False

    # 회원가입 폼이 화면에 표시되는지 확인
    def is_signup_form_displayed(self):
        try:
            form = self.wait.until(
                EC.presence_of_element_located(SignupLocators.SIGNUP_FORM)
            )
            logger.info("회원가입 폼 표시 확인")
            return form.is_displayed()
        except (TimeoutException, NoSuchElementException):
            logger.error("회원가입 폼을 찾지 못했습니다.")
            return False

    # 이메일 · 비밀번호 · 이름 입력
    def fill_signup_form(self, email: str, password: str, name: str):
        try:
            email_input = self.wait.until(
                EC.presence_of_element_located(CommonAuthLocators.LOGIN_ID_INPUT)
            )
            password_input = self.wait.until(
                EC.presence_of_element_located(CommonAuthLocators.PASSWORD_INPUT)
            )
            name_input = self.wait.until(
                EC.presence_of_element_located(CommonAuthLocators.FULLNAME_INPUT)
            )

            email_input.send_keys(email)
            password_input.send_keys(password)
            name_input.send_keys(name)

            logger.info("회원가입 정보 입력 성공")
            return True

        except (TimeoutException, NoSuchElementException):
            logger.error("회원가입 입력 요소를 찾지 못했습니다.")
            return False

    # '전체동의' 체크박스 클릭
    def click_agree_all_checkbox(self):
        try:
            checkbox_span = self.wait.until(
                EC.element_to_be_clickable(SignupLocators.AGREE_ALL_CHECKBOX)
            )
            checkbox_span.click()
            logger.info("전체동의 체크박스 클릭 성공")
            return True
        except TimeoutException:
            logger.error("전체동의 체크박스를 찾지 못했습니다.")
            return False

    # '회원가입' 버튼 클릭
    def click_signup_button(self):
        try:
            signup_btn = self.wait.until(
                EC.element_to_be_clickable(SignupLocators.SIGNUP_BTN)
            )
            signup_btn.click()
            logger.info("회원가입 버튼 클릭 성공")
            return True
        except (TimeoutException, NoSuchElementException):
            logger.error("회원가입 버튼을 찾지 못했습니다.")
            return False