from src.config import Config
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
# from src.utils.logger import setup_logger

class SignupPage:
    URL = "https://accounts.elice.io/accounts/signup/method?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat&lang=en-US&org=qaproject"
    def __init__(self, driver:WebDriver):
        self.driver = driver
    # 회원가입 페이지로 이동
    def go_to_signup_page(self):
        self.driver.get(self.URL)
    
    # '이메일로 가입하기' 버튼 클릭
    def click_signup_with_email(self):
        try:
            button = self.driver.find_element(By.XPATH, "//button[text()='이메일로 가입하기']")
            button.click()
            return True
        except NoSuchElementException:
            return False
    # 회원가입 폼이 화면에 표시되는지 확인
    def is_signup_form_displayed(self):
        try:
            form = self.driver.find_element(By.TAG_NAME, "form")
            return form.is_displayed()
        except NoSuchElementException:
            return False
    
    # 이메일 · 비밀번호 · 이름 입력
    def fill_signup_form(self, email:str, password:str, name:str):
        try:
            self.driver.find_element(By.NAME,"loginId").send_keys(email)
            self.driver.find_element(By.NAME,"password").send_keys(password)
            self.driver.find_element(By.NAME,"fullname").send_keys(name)
            return True
        except NoSuchElementException:
            return False
    # '전체동의' 체크박스 클릭
    def click_agree_all_checkbox(self):
        try:
        # span 요소가 클릭 가능할 때까지 기다림
            checkbox_span = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span.MuiCheckbox-root"))
        )
            checkbox_span.click()
            return True
        except:
            return False
        
    # '회원가입' 버튼 클릭
    def click_signup_button(self):
        try:
            button = self.driver.find_element(By.XPATH, "//button[contains(text(),'회원가입')]")
            button.click()
            return True
        except NoSuchElementException:
            return False
    
