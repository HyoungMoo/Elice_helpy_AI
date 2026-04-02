from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from src.utils.logger import setup_logger
from src.utils.tool_locators import QuizLocators, CommonLocators

class QuizPage:
    
    def __init__(self, driver:WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver,10)
        self.logger = setup_logger("QuizPage")
    
    def go_to_quiz(self):
        self.logger.info("quiz 생성 페이지 이동 시도")
        element = self.wait.until(
            EC.element_to_be_clickable(QuizLocators.GO_TO_QUIZ)
        )
        element.click()
        self.logger.info("quiz 생성 페이지 이동 완료")

    # 퀴즈 생성 함수
    def create_quiz(
        self,
        option_type: str,
        difficulty: str,
        content: str,
    ):
        OPTION_TYPE_MAP = { # 이거 토글이라고 하나 그거 땜시
            "객관식(단일 선택)": "0",
            "객관식(복수 선택)": "1",
            "주관식": "3",
        }
        DIFFICULTY_MAP = { # 이거 토글이라고 하나 그거 땜시2
            "상": "Level3",
            "중": "Level2",
            "하": "Level1",
        }

        self.wait.until(
            EC.visibility_of_element_located(QuizLocators.OPTION_TYPE_SELECT)
        )

        # 유형 선택 (필수)
        self.driver.find_element(*QuizLocators.OPTION_TYPE_SELECT).click()
        self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f"li[role='option'][data-value='{OPTION_TYPE_MAP[option_type]}']")
            )
        ).click()
        self.logger.info(f"유형 선택 완료: {option_type}")

        # 난이도 선택 (필수)
        self.driver.find_element(*QuizLocators.DIFFICULTY_SELECT).click()
        self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f"li[role='option'][data-value='{DIFFICULTY_MAP[difficulty]}']")
            )
        ).click()
        self.logger.info(f"난이도 선택 완료: {difficulty}")

        # 주제 (필수)
        content_input = self.driver.find_element(*QuizLocators.CONTENT_INPUT)
        content_input.send_keys(Keys.CONTROL, "a")
        content_input.send_keys(Keys.DELETE)
        content_input.send_keys(content)
        self.logger.info("주제 입력 완료")

        # 생성 버튼
        btn = self.wait.until(
            EC.presence_of_element_located(QuizLocators.SUBMIT_BTN)
        )
        if not btn.is_enabled(): # 버튼 비활성화 확인 -> 클릭 생략 /// 이거 밑에 따로 함수 있음 나중에 정리
            self.logger.info("생성 버튼 비활성화")
            return
        btn.click()

        # 🔥 다시 생성 팝업 발생 시 재시도
        try:
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(CommonLocators.DIALOG)
            )
            self.logger.info("팝업 감지 -> 다시 생성 시도")

            self.driver.execute_script("""
            document.querySelectorAll('[role="tooltip"]').forEach(el => el.remove());
            """)

            retry_btn = self.wait.until(
                EC.element_to_be_clickable(CommonLocators.RETRY_BTN)
            )
            retry_btn.click()
            self.logger.info("다시 생성 클릭 완료")

        except TimeoutException:
            self.logger.info("팝업 없음 -> 정상 진행")

    def verify_quiz_generated(self):
        try:
            WebDriverWait(self.driver, 300).until(
                EC.visibility_of_element_located(QuizLocators.SUCCESS_MSG)
            )
            self.logger.info("퀴즈 생성 성공 확인됨")
        except TimeoutException:
            self.logger.error("퀴즈 생성 실패: 5분 내 생성 완료 메시지 미확인")
            raise AssertionError("퀴즈 생성 실패 - 생성 완료 메시지가 나타나지 않았습니다.")
    
    # 필수값(주제) 미입력 시 오류 메시지 확인 함수
    def get_content_error_message(self):
        try:
            error = self.wait.until(
                EC.visibility_of_element_located(CommonLocators.ERROR_MSG)
            )
            self.logger.info(f"에러 메시지: {error.text}")
            return error.text
        except Exception as e:
            self.logger.info(f"에러 메시지 없음: {e}")
            return None
    
    # 생성 중 입력란 비활성화 확인 함수
    def check_inputs_disabled_during_creation(self):
        try:
            # 중지 버튼이 나타날 때까지 대기 (생성 중 상태 기준)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(CommonLocators.STOP_BTN)
            )

            # 비활성화 상태 확인
            option_type = self.driver.find_element(*QuizLocators.OPTION_TYPE_SELECT)
            is_option_disabled = option_type.get_attribute("aria-disabled") == "true"
            self.logger.info(f"유형 선택 비활성화 여부: {is_option_disabled}")

            difficulty = self.driver.find_element(*QuizLocators.DIFFICULTY_SELECT)
            is_difficulty_disabled = difficulty.get_attribute("aria-disabled") == "true"
            self.logger.info(f"난이도 선택 비활성화 여부: {is_difficulty_disabled}")

            content = self.driver.find_element(*QuizLocators.CONTENT_INPUT)
            is_content_disabled = not content.is_enabled()
            self.logger.info(f"주제 입력 비활성화 여부: {is_content_disabled}")

            btn = self.driver.find_element(*QuizLocators.SUBMIT_BTN)
            is_btn_disabled = not btn.is_enabled()
            self.logger.info(f"생성 버튼 비활성화 여부: {is_btn_disabled}")

            return all([is_option_disabled, is_difficulty_disabled, is_content_disabled, is_btn_disabled])

        except Exception as e:
            self.logger.info(f"요소 확인 실패: {e}")
            return False

    # 생성 버튼 비활성화 확인 함수
    def check_submit_button_disabled(self):
        btn = self.driver.find_element(*QuizLocators.SUBMIT_BTN)
        return not btn.is_enabled()
    
    # 생성 도중 중지 함수
    def stop_creation(self):
        try:
            stop_btn = self.wait.until(       
                EC.element_to_be_clickable(CommonLocators.STOP_BTN)
            )
            self.driver.execute_script("arguments[0].click();", stop_btn)
            self.logger.info("중지 버튼 클릭 완료")
        except Exception as e:
            self.logger.info(f"중지 버튼 없음 (이미 완료된 상태): {e}")
    
    # 생성 도중 중지 완료 후 알림 메시지 함수
    def get_stop_alert_text(self):
        try:
            alert = self.wait.until(
                EC.visibility_of_element_located(CommonLocators.STOP_ALERT)
            )
            self.logger.info(f"알림 메시지: {alert.text}")
            return alert.text
        except Exception as e:
            self.logger.info(f"알림 없음: {e}")
            return None

    # 생성 도중 네트워크 오류 발생 시 알림 메시지 함수
    def get_network_error_message(self):
        # TODO: 버그 수정 후 실제 에러 메시지 요소 구현
        return None