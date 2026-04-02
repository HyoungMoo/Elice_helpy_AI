#logout_page.py
from src.config import Config
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from src.utils.auth_locators import CommonAuthLocators, LogoutLocators


class LogoutPage:

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def logout(self):
        try:
            # 프로필 이미지 클릭
            profile_icon = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(CommonAuthLocators.PROFILE_ICON)
            )
            profile_icon.click()

            # 로그아웃 버튼 클릭
            logout_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(LogoutLocators.LOGOUT_BTN)
            )
            logout_button.click()

            print("로그아웃 성공")

        except TimeoutException:
            print("로그아웃 요소를 찾을 수 없습니다.")

        except NoSuchElementException:
            print("로그아웃 버튼이 존재하지 않습니다.")

    # 로그인 자동완성 기록 삭제
    def remove_history(self):
        try:
            # 기록 삭제 버튼 클릭
            delete_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(LogoutLocators.DELETE_HISTORY_BTN)
            )
            delete_button.click()

            print("기록 삭제 버튼 클릭 성공")

        except TimeoutException:
            print("기록 삭제 버튼을 찾지 못했습니다.")

        except NoSuchElementException:
            print("기록 삭제 요소가 존재하지 않습니다.")

    # 다른 계정으로 로그인
    def sign_different_account(self):
        try:
            # 다른 계정으로 로그인 버튼 클릭
            different_account_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(LogoutLocators.DIFFERENT_ACCOUNT_BTN)
            )
            different_account_button.click()

            print("다른 계정으로 로그인 클릭 성공")

        except TimeoutException:
            print("다른 계정으로 로그인 버튼을 찾지 못했습니다.")

        except NoSuchElementException:
            print("다른 계정으로 로그인 요소가 존재하지 않습니다.")

    # 다중탭 로그아웃 동기화 테스트
    def test_logout_sync(self):
        try:
            # 첫 번째 탭 생성
            first_tab = self.driver.current_window_handle
            time.sleep(5)
            
            # 두 번째 탭 생성
            self.driver.switch_to.new_window('tab')
            self.driver.get(Config.base_url)
            time.sleep(5)
            # 두 번째 탭 저장
            second_tab = self.driver.current_window_handle

            # 첫 번째 탭으로 이동
            self.driver.switch_to.window(first_tab)
            time.sleep(5)

            # 로그아웃 실행
            self.logout()

            time.sleep(5)

            # 두 번째 탭으로 이동
            self.driver.switch_to.window(second_tab)
            time.sleep(5)

            # 새로고침
            self.driver.refresh()

            time.sleep(5)

            # 로그인 페이지로 이동했는지 확인
            if "signin" in self.driver.current_url:
                print("다중 탭 로그아웃 동기화 성공")
            else:
                print("다중 탭 로그아웃 동기화 실패")

        except Exception as e:
            print("다중 탭 로그아웃 테스트 실패:", e)