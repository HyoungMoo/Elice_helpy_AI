# login_page.py - auth module
from src.config import Config
import json
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.auth_locators import CommonAuthLocators, LoginLocators


class LoginPage:
    URL = f"{Config.base_url}/signin"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)   # wait 객체 추가

        with open("./src/resources/credentials.json", "r", encoding="utf-8") as f:
            self.credentials = json.load(f)

    def go_to_login_page(self):
        self.driver.get(self.URL)

    # 테스트 로그인 부분 test_login.py 내 사용
    def test_login(self, email: str, password: str):

        self.wait.until(
            EC.visibility_of_element_located(CommonAuthLocators.LOGIN_ID_INPUT)
        ).send_keys(email)

        self.wait.until(
            EC.visibility_of_element_located(CommonAuthLocators.PASSWORD_INPUT)
        ).send_keys(password)

        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: "ai-helpy-chat" in d.current_url
            )
            return True
        except TimeoutException:
            return False

    # 로그인 버튼 클릭
    def click_login_button(self):
        try:
            self.wait.until(
                EC.element_to_be_clickable(LoginLocators.LOGIN_BTN)
            ).click()
            return True
        except TimeoutException:
            return False

    # 비밀번호 가리기/보기 아이콘 클릭
    def click_toggle_password_visibility(self):
        try:
            self.wait.until(
                EC.element_to_be_clickable(LoginLocators.TOGGLE_PASSWORD_BTN)
            ).click()
            return True
        except TimeoutException:
            return False

    # 자동 로그인
    def login(self, user_key="user_3"):
        user = self.credentials[user_key]

        self.driver.current_password = user["password"]

        self.wait.until(
            EC.visibility_of_element_located(CommonAuthLocators.LOGIN_ID_INPUT)
        ).send_keys(user["email"])

        self.wait.until(
            EC.visibility_of_element_located(CommonAuthLocators.PASSWORD_INPUT)
        ).send_keys(user["password"])

        self.wait.until(
            EC.element_to_be_clickable(LoginLocators.LOGIN_BTN)
        ).click()