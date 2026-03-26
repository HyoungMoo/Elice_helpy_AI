import pytest
from src.pages.tool.tool_page import ToolPage
from src.pages.tool.quiz_page import QuizPage
from src.utils.logger import setup_logger

logger = setup_logger("QuizTool")

def test_quiz_create(logged_in_driver):
    driver = logged_in_driver
    
    logger.info("퀴즈 생성 테스트 시작")
    
    tool_page = ToolPage(driver)
    quiz_page = QuizPage(driver)
    
    tool_page.go_to_tool_page()
    quiz_page.go_to_quiz()
    tool_page.remove_tooltip()
    
    #quiz_page.create_quiz()