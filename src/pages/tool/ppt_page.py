from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
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
        self.logger.info("PPT 생성 페이지 이동 시도")
    
    # 생성 함수
    def create_ppt(self):
        self.wait.until(
            EC.visibility_of_element_located((By.NAME, "topic"))
        )

        # topic
        topic = self.driver.find_element(By.NAME, "topic")
        topic.send_keys(Keys.CONTROL, "a")
        topic.send_keys(Keys.DELETE)
        topic.send_keys("파이썬 기초")
        """
        # instructions
        instructions = self.driver.find_element(By.NAME, "instructions")
        instructions.send_keys(Keys.CONTROL, "a")
        instructions.send_keys(Keys.DELETE)
        instructions.send_keys("설명")

        # slides_count
        slides = self.driver.find_element(By.NAME, "slides_count")
        slides.send_keys(Keys.CONTROL, "a")
        slides.send_keys(Keys.DELETE)
        slides.send_keys("3")

        # section_count
        section = self.driver.find_element(By.NAME, "section_count")
        section.send_keys(Keys.CONTROL, "a")
        section.send_keys(Keys.DELETE)
        section.send_keys("1")
        """
        self.logger.info("PPT 입력 완료")

        # 심층 모드 온/오프
        toggle = self.driver.find_element(
            By.NAME, "simple_mode"
        )
        toggle.click()
        
        # 생성 버튼
        btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='submit' and @form='tool-factory-create_pptx']")
            )
        )
        btn.click()
        # 🔥 다시 생성 팝업 발생 시 재시도
        try:
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "[role='dialog']"))
            )

            self.logger.info("팝업 감지 → 다시 생성 시도")

            # 팝업 제거
            self.driver.execute_script("""
            document.querySelectorAll('[role="tooltip"]').forEach(el => el.remove());
            """)

            # 다시 생성 버튼 클릭
            retry_btn = self.wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "[role='dialog'] button[type='submit']")
                )
            )
            retry_btn.click()

            self.logger.info("다시 생성 클릭 완료")

        except:
            self.logger.info("팝업 없음 → 정상 진행")

        self.logger.info("PPT 생성 완료")

    # 생성 도중 중단 함수
    def stop_creation(self):
        try:
            stop_btn = self.wait.until(       
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[.//*[@data-testid='stopIcon']]")
                )
            )
            self.driver.execute_script("arguments[0].click();", stop_btn)
            self.logger.info("중단 버튼 클릭 완료")
        except Exception as e:
            self.logger.info(f"중단 버튼 없음 (이미 완료된 상태): {e}")

    # 다운로드 함수
    def ppt_download(self):
        download_btn = WebDriverWait(self.driver, 120).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(text(),'생성 결과 다운받기')]")
            )
        )
        download_btn.click()
        
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
                "심층조사 모드 토글": (By.NAME, "simple_mode"),
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