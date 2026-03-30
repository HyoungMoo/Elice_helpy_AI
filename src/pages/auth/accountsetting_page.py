from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

class AccountSetting:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def go_to_account_setting(self):

        # 프로필 아이콘 클릭
        profile_icon = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.MuiAvatar-root"))
        )
        profile_icon.click()

        # 계정 관리 클릭
        account_setting = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='계정 관리']"))
        )
        account_setting.click()

       # URL 이동 대기
        self.wait.until(
            EC.url_contains("account")
        )

        # 페이지 로딩 완료 대기 
        self.wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

        # 기본 정보 영역 로딩 대기
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'기본 정보')]"))
        )

    def change_name(self, new_name):

        # 수정 아이콘 버튼 찾기 (왜안돼)
        edit_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "svg[data-testid='EditOutlinedIcon']")
            )
        )

        # Material UI는 JS 클릭이 더 안정적
        self.driver.execute_script("arguments[0].scrollIntoView(true);", edit_button)
        self.driver.execute_script("arguments[0].click();", edit_button)

        # 이름 입력창 대기
        name_input = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input"))
        )

        # 기존 이름 삭제 후 입력
        name_input.clear()
        name_input.send_keys(new_name)

        # 완료 버튼 클릭
        save_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(),'완료')]/ancestor::button")
            )
        )

        save_button.click()