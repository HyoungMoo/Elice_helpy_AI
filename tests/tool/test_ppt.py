import pytest
from src.pages.tool.tool_page import ToolPage
from src.pages.tool.ppt_page import PptPage
from selenium.webdriver.support import expected_conditions as EC
from src.utils.logger import setup_logger
import time
logger = setup_logger("TestTool")

def test_ppt_create(logged_in_driver):
    driver = logged_in_driver
    
    logger.info("PPT 생성 테스트 시작")
    
    tool_page = ToolPage(driver)
    ppt_page = PptPage(driver)
    
    tool_page.remove_tooltip()
    tool_page.go_to_tool_page()
    ppt_page.go_to_ppt()
    tool_page.remove_tooltip()
    
    ppt_page.create_ppt()
    logger.info("PPT 생성 테스트 성공")
    is_disabled = ppt_page.check_inputs_disabled_during_creation()
    assert is_disabled, "생성 중 입력 요소가 비활성화되지 않음"
    logger.info("생성 중 입력 요소 비활성화 확인 완료")

    ppt_page.ppt_download()
    logger.info("PPT 다운로드 테스트 확인 완료")
"""
def test_creation_with_stop(logged_in_driver):
    driver = logged_in_driver
    
    logger.info("PPT 생성 중 중단 테스트 시작")
    
    tool_page = ToolPage(driver)
    ppt_page = PptPage(driver)
    
    tool_page.go_to_tool_page()
    ppt_page.go_to_ppt()
    #tool_page.remove_tooltip()
    ppt_page.create_ppt()

    # 잠시 대기 
    time.sleep(2) 

    # 중단 시도
    ppt_page.stop_creation()
    
    alert_text = ppt_page.get_stop_alert_text()
    #assert alert_text is not None, "중단 알림이 표시되지 않음"
    #assert "요청에 의해 답변 생성을 중지했습니다." in alert_text
    logger.info(f"중단 알림 확인: {alert_text}")
    logger.info("PPT 생성 중 중단 테스트 성공")
"""
    

