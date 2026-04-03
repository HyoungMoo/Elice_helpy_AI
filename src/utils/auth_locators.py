from selenium.webdriver.common.by import By


class CommonAuthLocators:
    # 공통 입력 필드
    LOGIN_ID_INPUT = (By.NAME, "loginId")
    PASSWORD_INPUT = (By.NAME, "password")
    FULLNAME_INPUT = (By.NAME, "fullname")

    # 공통 버튼
    PROFILE_ICON = (By.CSS_SELECTOR, "button.MuiAvatar-root")
    CONFIRM_BTN = (By.XPATH, "//button[normalize-space(text())='완료']")

class LoginLocators:
    # 버튼
    LOGIN_BTN = (By.XPATH, "//button[text()='Login']")
    TOGGLE_PASSWORD_BTN = (By.XPATH, "//button[@aria-label='View password']")

class LogoutLocators:
    # 버튼
    LOGOUT_BTN = (By.XPATH, "//div[contains(@class,'MuiListItemButton-root') and .//p[text()='로그아웃']]")
    DELETE_HISTORY_BTN = (By.XPATH, "//a[text()='기록 삭제']")
    DIFFERENT_ACCOUNT_BTN = (By.XPATH, "//a[text()='Sign in with a different account']")

class SignupLocators:
    # 버튼
    SIGNUP_WITH_EMAIL_BTN = (By.XPATH, "//button[text()='이메일로 가입하기']")
    AGREE_ALL_CHECKBOX = (By.CSS_SELECTOR, "span.MuiCheckbox-root")
    SIGNUP_BTN = (By.XPATH, "//button[contains(text(),'회원가입')]")

    # 폼
    SIGNUP_FORM = (By.TAG_NAME, "form")

class AccountSettingLocators:
    # 페이지 이동
    ACCOUNT_SETTING_BTN = (By.XPATH, "//span[text()='계정 관리']")
    TABLE_LOADED = (By.XPATH, "//td[text()='이름']")
    BILLING_HISTORY = (By.XPATH, "//span[text()='결제 내역']")

    # 프로필 이미지
    PROFILE_IMAGE_ICON = (By.CSS_SELECTOR, '[data-testid="pen-to-squareIcon"]')
    CHANGE_PROFILE_IMAGE_BTN = (By.XPATH, "//li[.//p[text()='프로필 이미지 변경']]")
    DELETE_PROFILE_IMAGE_BTN = (By.XPATH, "//li[.//p[text()='프로필 이미지 제거']]")
    FILE_UPLOAD_INPUT = (By.XPATH, "//input[@type='file']")

    # 이름 변경
    EDIT_NAME_BTN = (By.XPATH, "//td[text()='이름']/following-sibling::td//button")

    # 비밀번호 변경
    EDIT_PASSWORD_BTN = (By.XPATH, "//td[normalize-space()='비밀번호']/following-sibling::td//button")
    NEW_PASSWORD_INPUT = (By.NAME, "newPassword")
    CONFIRM_PASSWORD_INPUT = (By.NAME, "confirmPassword")

    # 언어 변경
    LANGUAGE_SELECT = (By.ID, "mui-component-select-locale")
    LANGUAGE_DROPDOWN = (By.CSS_SELECTOR, 'select[aria-label="Change Languages"]')

    # 계정 탈퇴
    WITHDRAWAL_BTN = (By.XPATH, "//button[text()='탈퇴하기']")
    WITHDRAWAL_EMAIL_INPUT = (By.NAME, "email")

    # 프로모션
    PROMOTION_TOGGLE = (By.XPATH, "//input[@name='marketing']")

    # 동적 locator
    @staticmethod
    def language_option(value: str):
        return (By.XPATH, f"//li[@data-value='{value}']")