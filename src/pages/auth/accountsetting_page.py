from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from selenium.webdriver.support.ui import Select


class AccountSetting:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    # 새로고침 매서드
    def refresh(self):
        self.driver.refresh()
    # 메인 → 계정관리 페이지 이동
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

        # 새 탭으로 전환
        self.wait.until(EC.number_of_windows_to_be(2))
        self.driver.switch_to.window(self.driver.window_handles[-1])

        # 새 탭에서 URL 확인
        self.wait.until(EC.url_contains("accounts.elice.io/members/account"))

        # 테이블 완전 로딩 대기
        self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//td[text()='이름']"))
        )
    # 프로필 아이콘 클릭
    def click_profile_image_icon(self):
        icon = self.wait.until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR, '[data-testid="pen-to-squareIcon"]'
                ))
            )
        icon.click()
       
    # # 프로필 이미지 변경
    # def change_profile_image(self):
    #     # 프로필 아이콘 클릭
    #     self.click_profile_image_icon()
    #     # '프로필 이미지 변경' 버튼 클릭
    #     edit_btn = self.wait.until(
    #             EC.element_to_be_clickable((
    #                 By.XPATH,  "//li[.//p[text()='프로필 이미지 변경']]"
    #             ))
    #         )
    #     edit_btn.click()
    #     # 프로필 이미지 삽입
    #     upload = self.wait.until(
    #             EC.presence_of_element_located((
    #                 By.XPATH, "//input[@type='file']"))
    #         )
    #     # 절대 경로로 이미지 삽입
    #     upload.send_keys(r"C:\Users\user\eliceqa_first_project\src\resources\assets\frog.png")
    # 프로필 이미지 변경
    def change_profile_image(self):
        # 프로필 아이콘 클릭
        self.click_profile_image_icon()

        # '프로필 이미지 변경' 버튼 클릭
        edit_btn = self.wait.until(
            EC.element_to_be_clickable((
                By.XPATH, "//li[.//p[text()='프로필 이미지 변경']]"
            ))
        )
        edit_btn.click()

        # 파일 업로드 input
        upload = self.wait.until(
            EC.presence_of_element_located((
                By.XPATH, "//input[@type='file']"
            ))
        )

        # 프로젝트 기준 이미지 경로
        img_path = Path(__file__).resolve().parent.parent.parent / "resources" / "assets" / "frog.png"

        upload.send_keys(str(img_path))
    # # 프로필 이미지 삭제
    def delete_profile_image(self):
        # 프로필 아이콘 클릭
        self.click_profile_image_icon()
        # '프로필 이미지 제거' 버튼 클릭
        delete_btn = self.wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,  "//li[.//p[text()='프로필 이미지 제거']]"
                ))
            )
        delete_btn.click()
        

    # 이름 변경 아이콘 클릭
    def click_edit_name_icon(self):
        # 이름 행의 수정 버튼만 정확하게 찾기
        edit_btn = self.wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//td[text()='이름']/following-sibling::td//button"
            ))
        )
        edit_btn.click()
    # 이름 변경
    def change_name(self, new_name):
        # 수정 아이콘 클릭
        self.click_edit_name_icon()

        # 이름 입력창 대기
        name_input = self.wait.until(
            EC.visibility_of_element_located((By.NAME, "fullname"))
        )

        # 기존 이름 삭제 후 새 이름 입력
        name_input.click()
        name_input.send_keys(Keys.CONTROL, 'a')
        name_input.send_keys(Keys.DELETE)
        name_input.send_keys(new_name)

        # 완료 버튼 클릭
        save_button = self.wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[normalize-space(text())='완료']"
            ))
        )
        save_button.click()
    # 비밀번호 변경 아이콘 클릭
    def click_edit_password_icon(self):
        edit_btn = self.wait.until(
        EC.element_to_be_clickable((
            By.XPATH, "//td[normalize-space()='비밀번호']/following-sibling::td//button"))
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", edit_btn
        )
        edit_btn.click()
    # 비밀번호 변경
    def change_password(self,current_pw,new_pw,confirm_pw):
        # 비밀번호 변경 아이콘 클릭
        self.click_edit_password_icon()
        # 현재 비밀번호 입력
        current = self.wait.until(
            EC.element_to_be_clickable((By.NAME,"password"))
        )
        current.clear()
        current.send_keys(current_pw)
        # 새 비밀번호 입력
        new = self.wait.until(
            EC.element_to_be_clickable((By.NAME, "newPassword"))
        )
        new.clear()
        new.send_keys(new_pw)
        # 새 비밀번호 확인
        confirm = self.wait.until(
            EC.element_to_be_clickable((By.NAME, "confirmPassword"))
        )
        confirm.clear()
        confirm.send_keys(confirm_pw)

        # 완료 버튼 클릭
        btn = self.wait.until(
            EC.element_to_be_clickable((
                By.XPATH, "//button[normalize-space()='완료']"
            ))
        )
        btn.click()

    # 선호 언어 변경 (한국어->영어->한국어)
    def change_language(self):
        # 토글 열기
        toggle = self.wait.until(
            EC.element_to_be_clickable((By.ID,"mui-component-select-locale"))
        )
        toggle.click()
        # 옵션 선택
        option = self.wait.until(
            EC.element_to_be_clickable((By.XPATH,"//li[@data-value='en-US']"))
        )
        option.click()
        # 토글 열기
        toggle = self.wait.until(
            EC.element_to_be_clickable((By.ID,"mui-component-select-locale"))
        )
        toggle.click()
        # 옵션 선택
        option = self.wait.until(
            EC.element_to_be_clickable((By.XPATH,"//li[@data-value='ko-KR']"))
        )
        option.click()

    # 계정 탈퇴 '탈퇴하기' 버튼 클릭
    def click_auth_delete_btn(self):
        btn = self.wait.until(
            EC.element_to_be_clickable((
                By.XPATH, "//button[text()='탈퇴하기']"
            ))
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
            EC.element_to_be_clickable((By.NAME,'email'))
        )
        input_delete_email.clear()
        input_delete_email.send_keys("Delete "+email)
        
        # 탈퇴하기 버튼 클릭
        self.click_auth_delete_btn()
    # 회원가입 페이지 한국어로 변경 
    def change_language_to_korean(self):
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'select[aria-label="Change Languages"]'))
        )

        select = Select(dropdown)
        select.select_by_value("ko-KR")