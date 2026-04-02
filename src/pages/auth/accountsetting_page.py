#accountsetting_page.py
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from src.utils.auth_locators import CommonAuthLocators, AccountSettingLocators
import time

class AccountSetting:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # 새로고침 메서드
    def refresh(self):
        self.refresh()

    # 메인 → 계정관리 페이지 이동
    def go_to_account_setting(self):
        # 프로필 아이콘 클릭
        profile_icon = self.wait.until(
            EC.element_to_be_clickable(CommonAuthLocators.PROFILE_ICON)
        )
        profile_icon.click()

        # 계정 관리 클릭
        account_setting = self.wait.until(
            EC.element_to_be_clickable(AccountSettingLocators.ACCOUNT_SETTING_BTN)
        )
        account_setting.click()

        # 새 탭으로 전환
        self.wait.until(EC.number_of_windows_to_be(2))
        self.driver.switch_to.window(self.driver.window_handles[-1])

        # 새 탭에서 URL 확인
        self.wait.until(EC.url_contains("accounts.elice.io/members/account"))

        # 테이블 완전 로딩 대기
        self.wait.until(
            EC.visibility_of_element_located(AccountSettingLocators.TABLE_LOADED)
        )

    # 프로필 아이콘 클릭
    def click_profile_image_icon(self):
        icon = self.wait.until(
            EC.element_to_be_clickable(AccountSettingLocators.PROFILE_IMAGE_ICON)
        )
        icon.click()

    # 프로필 이미지 변경
    def change_profile_image(self):
        # 프로필 아이콘 클릭
        self.click_profile_image_icon()

        # '프로필 이미지 변경' 버튼 클릭
        edit_btn = self.wait.until(
            EC.element_to_be_clickable(AccountSettingLocators.CHANGE_PROFILE_IMAGE_BTN)
        )
        edit_btn.click()

        # 파일 업로드 input
        upload = self.wait.until(
            EC.presence_of_element_located(AccountSettingLocators.FILE_UPLOAD_INPUT)
        )

        # 프로젝트 기준 이미지 경로
        img_path = Path(__file__).resolve().parent.parent.parent / "resources" / "assets" / "frog.png"
        upload.send_keys(str(img_path))

    # 프로필 이미지 삭제
    def delete_profile_image(self):
        # 프로필 아이콘 클릭
        self.click_profile_image_icon()

        # '프로필 이미지 제거' 버튼 클릭
        delete_btn = self.wait.until(
            EC.element_to_be_clickable(AccountSettingLocators.DELETE_PROFILE_IMAGE_BTN)
        )
        delete_btn.click()

    # 이름 변경 아이콘 클릭
    def click_edit_name_icon(self):
        # 이름 행의 수정 버튼만 정확하게 찾기
        edit_btn = self.wait.until(
            EC.element_to_be_clickable(AccountSettingLocators.EDIT_NAME_BTN)
        )
        edit_btn.click()

    # 이름 변경
    def change_name(self, new_name):
        # 수정 아이콘 클릭
        self.click_edit_name_icon()

        # 이름 입력창 대기
        name_input = self.wait.until(
            EC.visibility_of_element_located(CommonAuthLocators.FULLNAME_INPUT)
        )

        # 기존 이름 삭제 후 새 이름 입력
        name_input.click()
        name_input.send_keys(Keys.CONTROL, 'a')
        name_input.send_keys(Keys.DELETE)
        name_input.send_keys(new_name)

        # 완료 버튼 클릭
        save_button = self.wait.until(
            EC.element_to_be_clickable(CommonAuthLocators.CONFIRM_BTN)
        )
        save_button.click()

    # 비밀번호 변경 아이콘 클릭
    def click_edit_password_icon(self):
        edit_btn = self.wait.until(
            EC.element_to_be_clickable(AccountSettingLocators.EDIT_PASSWORD_BTN)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", edit_btn
        )
        edit_btn.click()

    # 비밀번호 변경
    def change_password(self, current_pw, new_pw, confirm_pw):
        # 비밀번호 변경 아이콘 클릭
        self.click_edit_password_icon()

        # 현재 비밀번호 입력
        current = self.wait.until(
            EC.element_to_be_clickable(CommonAuthLocators.PASSWORD_INPUT)
        )
        current.clear()
        current.send_keys(current_pw)

        # 새 비밀번호 입력
        new = self.wait.until(
            EC.element_to_be_clickable(AccountSettingLocators.NEW_PASSWORD_INPUT)
        )
        new.clear()
        new.send_keys(new_pw)

        # 새 비밀번호 확인
        confirm = self.wait.until(
            EC.element_to_be_clickable(AccountSettingLocators.CONFIRM_PASSWORD_INPUT)
        )
        confirm.clear()
        confirm.send_keys(confirm_pw)

        # 완료 버튼 클릭
        btn = self.wait.until(
            EC.element_to_be_clickable(CommonAuthLocators.CONFIRM_BTN)
        )
        btn.click()

    # 선호 언어 변경 (한국어->영어)
    def change_language_to_english_setting(self):

        # 토글 열기
        toggle = self.wait.until(
            EC.element_to_be_clickable(AccountSettingLocators.LANGUAGE_SELECT)
        )
        toggle.click()

        # 옵션 선택
        option = self.wait.until(
            EC.element_to_be_clickable(AccountSettingLocators.language_option("en-US"))
        )
        option.click()
        # dropdown 닫힘 대기
        self.wait.until(
            EC.invisibility_of_element_located(("css selector", ".MuiBackdrop-root"))
        )
    # 선호 언어 변경 (영어->한국어)
    def change_language_to_korean_setting(self):
        # 토글 열기
        toggle = self.wait.until(
            EC.element_to_be_clickable(AccountSettingLocators.LANGUAGE_SELECT)
        )
        toggle.click()

        # 옵션 선택
        option = self.wait.until(
            EC.element_to_be_clickable(AccountSettingLocators.language_option("ko-KR"))
        )
        option.click()

    # 계정 탈퇴 '탈퇴하기' 버튼 클릭
    def click_auth_delete_btn(self):
        btn = self.wait.until(
            EC.element_to_be_clickable(AccountSettingLocators.WITHDRAWAL_BTN)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", btn
        )
        btn.click()

    # 계정 탈퇴 진행
    def account_withdrawal(self, email):
        # 탈퇴하기 버튼 클릭
        self.click_auth_delete_btn()

        # 계정 탈퇴 입력 필드 'Delete "이메일"' 입력
        input_delete_email = self.wait.until(
            EC.element_to_be_clickable(AccountSettingLocators.WITHDRAWAL_EMAIL_INPUT)
        )
        input_delete_email.clear()
        input_delete_email.send_keys("Delete " + email)

        # 탈퇴하기 버튼 클릭
        self.click_auth_delete_btn()

    # 회원가입 페이지 한국어로 변경 (푸터바)
    def change_language_to_korean(self):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(AccountSettingLocators.LANGUAGE_DROPDOWN)
        )
        select = Select(dropdown)
        select.select_by_value("ko-KR")
    
    # 프로모션 알림 받기
    def open_toggle_promotion(self):
        toggle = self.wait.until(
            EC.presence_of_element_located(AccountSettingLocators.PROMOTION_TOGGLE)
        )
        toggle.click()
        # dropdown 닫힘 대기
        self.wait.until(
            EC.invisibility_of_element_located(("css selector", ".MuiBackdrop-root"))
        )
    
    # 프로모션 알림 해지
    def close_toggle_promotion(self):
        toggle = self.wait.until(
            EC.presence_of_element_located(AccountSettingLocators.PROMOTION_TOGGLE)
        )
        toggle.click()