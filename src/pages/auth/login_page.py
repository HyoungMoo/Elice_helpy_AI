from src.config import Config
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException

class LoginPage:
    URL = f"{Config.base_url}/signin"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        with open("./src/resources/credentials.json", "r", encoding="utf-8") as f:
            self.credentials = json.load(f)

    def go_to_login_page(self):
        self.driver.get(self.URL)

    # 테스트 로그인 부분 test_login.py 내 사용
    def test_login(self, email: str, password: str):
        from selenium.webdriver.support.ui import WebDriverWait

        self.driver.find_element(By.NAME, "loginId").send_keys(email)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        # 로그인 성공 확인: URL에 ai-helpy-chat 포함되면 True 반환
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: "ai-helpy-chat" in d.current_url
            )
            return True
        except:
            return False
    # 로그인 버튼 클릭
    def click_login_button(self):
        try:
            button = self.driver.find_element(By.XPATH, "//button[text()='Login']").click()
            return True
        except NoSuchElementException:
            return False
    #비밀번호 가리기/보기 아이콘 클릭
    def click_toggle_password_visibility(self):
        try:
            button = self.driver.find_element(By.XPATH, "//button[@aria-label='View password']")
            button.click()
            return True
        except Exception:
            return False
    # 자동 로그인
    def login(self, user_key="user_3"):
        user = self.credentials[user_key]
        self.driver.find_element(By.NAME, "loginId").send_keys(user["email"])
        self.driver.find_element(By.NAME, "password").send_keys(user["password"])
        self.driver.find_element(By.XPATH, "//button[text()='Login']").click()