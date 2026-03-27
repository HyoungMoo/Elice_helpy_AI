from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.logger import setup_logger

class ToolPage:
    
    def __init__(self, driver:WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver,10)
        self.logger = setup_logger("ToolPage")
    
    def go_to_tool_page(self):
        self.logger.info("도구 페이지 이동 시도")
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH,"//a[@href='/ai-helpy-chat/tools']"))
        )
        
        element.click()
        self.logger.info("도구 페이지 이동 완료")
    
    def go_to_agent_page(self):
        self.logger.info("에이전트 탐색 페이지 이동 시도")
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH,"//a[@href='/ai-helpy-chat/agents']"))
        )
        
        element.click()
        self.logger.info("에이전트 탐색 페이지 이동 완료")
    
    def remove_tooltip(self):
        try:
            WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[role='tooltip']"))
            )
        except:
            pass

        self.driver.execute_script("""
            document.querySelectorAll('[role="tooltip"]').forEach(el => el.remove());
            document.querySelectorAll('.notistack-MuiContent').forEach(el => el.remove());
        """)
        self.logger.info("툴팁 및 알림 제거 완료")