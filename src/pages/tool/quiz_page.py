from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from src.utils.logger import setup_logger

class QuizPage:
    
    def __init__(self, driver:WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver,10)
        self.logger = setup_logger("QuizPage")
    
    def go_to_quiz(self):
        self.logger.info("quiz 생성 페이지 이동 시도")
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[.//p[text()='퀴즈 생성']]"))
        )
        element.click()
        self.logger.info("quiz 생성 페이지 이동 시도")
            
    def remove_tooltip(self):
        try:
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[role='tooltip']"))
            )
        except:
            pass

        self.driver.execute_script("""
        document.querySelectorAll('[role="tooltip"]').forEach(el => el.remove());
        """)