import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SettingsPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open_language_menu(self):
        # 1. 프로필 아이콘 JS 클릭 (다른 요소에 가려질 수 있으므로 JS 클릭 사용)
        profile_icon = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.MuiAvatar-root"))
        )
        self.driver.execute_script("arguments[0].click();", profile_icon)
        time.sleep(1)  # 프로필 메뉴 열릴 때까지 대기

        # 2. 언어 설정 메뉴 JS 클릭
        # backdrop(반투명 배경)이 버튼 위에 겹쳐있으면 클릭이 막히므로
        # JS 클릭으로 강제 실행
        lang_menu = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-menu-id='locale_setting']"))
        )
        self.driver.execute_script("arguments[0].click();", lang_menu)
        time.sleep(0.5)  # 언어 선택 서브메뉴 열릴 때까지 대기

    def change_language(self, language_text):
        # 프로필 → 언어 메뉴까지 자동 처리
        self.open_language_menu()

        # 언어 선택 JS 클릭
        # backdrop 이 완전히 사라지기 전에 클릭하면 실패하므로 JS 클릭 사용
        lang_btn = self.wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                f"//p[contains(text(),'{language_text}')]/ancestor::div[@role='button']"
            ))
        )
        self.driver.execute_script("arguments[0].click();", lang_btn)
        time.sleep(1)  # 언어 변경 적용 대기