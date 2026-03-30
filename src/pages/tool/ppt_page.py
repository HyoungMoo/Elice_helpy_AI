import time

from selenium.common import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pptx import Presentation
from urllib.parse import urlparse
from pathlib import Path
from src.utils.logger import setup_logger

class PptPage:
    def __init__(self, driver:WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver,10)
        self.logger = setup_logger("PptPage")
        
    def go_to_ppt(self):
        self.logger.info("PPT 생성 페이지 이동 시도")
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[.//p[text()='PPT 생성']]"))
        )
        element.click()
        self.logger.info("PPT 생성 페이지 이동 완료")
    
    # 생성 함수
    def create_ppt(
        self,
        topic: str,
        instructions: str = "",
        slides_count: str = "",
        section_count: str = "",
    ):
        self.wait.until(
            EC.visibility_of_element_located((By.NAME, "topic"))
        )

        # 주제 (필수)
        topic_input = self.driver.find_element(By.NAME, "topic")
        topic_input.send_keys(Keys.CONTROL, "a")
        topic_input.send_keys(Keys.DELETE)
        topic_input.send_keys(topic)

        # 지시사항 (선택)
        instructions_input = self.driver.find_element(By.NAME, "instructions")
        instructions_input.send_keys(Keys.CONTROL, "a")
        instructions_input.send_keys(Keys.DELETE)
        instructions_input.send_keys(instructions)

        # 슬라이드 수 (선택)
        slides_input = self.driver.find_element(By.NAME, "slides_count")
        slides_input.send_keys(Keys.CONTROL, "a")
        slides_input.send_keys(Keys.DELETE)
        slides_input.send_keys(slides_count)

        # 섹션 수 (선택)
        section_input = self.driver.find_element(By.NAME, "section_count")
        section_input.send_keys(Keys.CONTROL, "a")
        section_input.send_keys(Keys.DELETE)
        section_input.send_keys(section_count)

        self.logger.info("PPT 입력 완료")
        """
        # 심층 모드 온/오프
        toggle = self.driver.find_element(By.NAME, "simple_mode")
        toggle.click()
        """
        # 생성 버튼
        btn = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@type='submit' and @form='tool-factory-create_pptx']")
            )
        )
        if not btn.is_enabled(): # 필수값 미입력시 오류 방지
            self.logger.info("생성 버튼 비활성화 → 클릭 생략")
            return

        btn.click()

        # 🔥 다시 생성 팝업 발생 시 재시도
        try:
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "[role='dialog']"))
            )
            self.logger.info("팝업 감지 -> 다시 생성 시도")

            self.driver.execute_script("""
            document.querySelectorAll('[role="tooltip"]').forEach(el => el.remove());
            """)

            retry_btn = self.wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "[role='dialog'] button[type='submit']")
                )
            )
            retry_btn.click()
            self.logger.info("다시 생성 클릭 완료")

        except:
            self.logger.info("팝업 없음 -> 정상 진행")

        self.logger.info("PPT 생성 완료")
        
    # 생성 도중 중지 함수
    def stop_creation(self):
        try:
            stop_btn = self.wait.until(       
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[.//*[@data-testid='stopIcon']]")
                )
            )
            self.driver.execute_script("arguments[0].click();", stop_btn)
            self.logger.info("중지 버튼 클릭 완료")
        except Exception as e:
            self.logger.info(f"중지 버튼 없음 (이미 완료된 상태): {e}")

    # 다운로드 함수
    def ppt_download(self):
        try:
            for attempt in range(3):
                try:
                    download_btn = WebDriverWait(self.driver, 300).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//a[contains(text(),'생성 결과 다운받기')]")
                        )
                    )
                    href = download_btn.get_attribute("href")
                    filename = Path(urlparse(href).path).name
                    self.logger.info(f"다운로드 파일명: {filename}")
                    download_btn.click()
                    return filename
                except StaleElementReferenceException:
                    self.logger.warning(f"StaleElementReferenceException 발생, 재시도 {attempt + 1}/3")
                    time.sleep(1)
        except TimeoutException:
            self.logger.error("생성 실패: 5분 내 '생성 결과 다운받기' 버튼 미확인")
            raise AssertionError("생성 실패 - '생성 결과 다운받기' 버튼이 나타나지 않았습니다.")

        raise AssertionError("다운로드 버튼 클릭 실패 - StaleElementReferenceException 3회 반복")

    def verify_ppt_generated(self):
        try:
            WebDriverWait(self.driver, 300).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//p[contains(text(),'입력하신 내용 기반으로 PPT를 생성했습니다.')]")
                )
            )
            self.logger.info("PPT 생성 성공 확인됨")
        except TimeoutException:
            self.logger.error("PPT 생성 실패: 5분 내 생성 완료 메시지 미확인")
            raise AssertionError("PPT 생성 실패 - 생성 완료 메시지가 나타나지 않았습니다.")
        
    # 슬라이드 수 카운드 함수   
    def check_ppt_slide_count(self, file_path, expected_count=None):

        file_path = Path(file_path)
        assert file_path.exists(), f"파일이 존재하지 않음: {file_path}"
        
        prs = Presentation(file_path)
        slide_count = len(prs.slides)
        self.logger.info(f"슬라이드 수: {slide_count}")
        
        assert slide_count > 0, "슬라이드가 없음"
        
        if expected_count:
            assert slide_count == expected_count, f"슬라이드 수 불일치 (입력값: {expected_count}, 실제값: {slide_count})"
        
        return slide_count
        
    def get_stop_alert_text(self):
        try:
            alert = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//div[@role='alert']"))
            )
            self.logger.info(f"알림 메시지: {alert.text}")
            return alert.text
        except Exception as e:
            self.logger.info(f"알림 없음: {e}")
            return None
        
    def check_inputs_disabled_during_creation(self):
        try:
            selectors = {
                "주제 입력": (By.NAME, "topic"),
                "지시사항 입력": (By.NAME, "instructions"),
                "슬라이드 수 입력": (By.NAME, "slides_count"),
                "섹션 수 입력": (By.NAME, "section_count"),
               #"심층조사 모드 토글": (By.NAME, "simple_mode"),
                "다시 생성 버튼": (By.XPATH, "//button[@type='submit' and @form='tool-factory-create_pptx']"),
            }

            all_disabled = True
            for name, selector in selectors.items():
                element = self.wait.until(EC.presence_of_element_located(selector))
                is_disabled = not element.is_enabled()
                self.logger.info(f"{name} 비활성화 여부: {is_disabled}")
                if not is_disabled:
                    all_disabled = False

            return all_disabled

        except Exception as e:
            self.logger.info(f"요소 확인 실패: {e}")
            return False
    
    def check_submit_button_disabled(self):
        btn = self.driver.find_element(
            By.XPATH, "//button[@type='submit' and @form='tool-factory-create_pptx']"
        )
        return not btn.is_enabled()
    
    # 필수값(주제) 미입력시 오류 메시지 확인
    def get_topic_error_message(self):
        try:
            error = self.wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "p.MuiFormHelperText-root.Mui-error[id$='-helper-text']")
                )
            )
            self.logger.info(f"에러 메시지: {error.text}")
            return error.text
        except Exception as e:
            self.logger.info(f"에러 메시지 없음: {e}")
            return None
        
