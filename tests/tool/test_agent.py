import pytest
from src.pages.tool.tool_page import ToolPage
from src.pages.tool.agent_page import AgentPage
from src.utils.logger import setup_logger

logger = setup_logger("TestAngent")

# 필수값 모두 입력 (정상 생성)
def test_agent_create_required_only(logged_in_driver):
    logger.info("에이전트 생성 테스트 시작 - 필수값 모두 입력")
    driver = logged_in_driver

    tool_page = ToolPage(driver)
    agent_page = AgentPage(driver)

    tool_page.go_to_agent_page()
    agent_page.go_to_builder()
    tool_page.remove_tooltip()

    agent_page.create_agent(
        name="자동화 테스트 에이전트",
        system_prompt="존댓말 사용"
    )
    assert agent_page.is_agent_created(), "에이전트 생성 실패 - 성공 알림 미출력"
    logger.info("에이전트 생성 테스트 완료 - 필수값 모두 입력")
    
# 필수값(이름) 누락 입력
def test_agent_create_missing_name(logged_in_driver):
    logger.info("에이전트 생성 테스트 시작 - 필수값 이름 누락")
    driver = logged_in_driver

    tool_page = ToolPage(driver)
    agent_page = AgentPage(driver)

    tool_page.go_to_agent_page()
    agent_page.go_to_builder()
    tool_page.remove_tooltip()
    agent_page.create_agent(name="", system_prompt="존댓말 사용")
    
    errors = agent_page.get_error_messages()
    assert "이름을 입력해주세요" in errors
    logger.info(f"이름 누락 오류 메시지 확인 완료: {errors}")
    
# 필수값(규칙) 누락 입력
def test_agent_create_missing_system_prompt(logged_in_driver):
    logger.info("에이전트 생성 테스트 시작 - 필수값 규칙 누락")
    driver = logged_in_driver

    tool_page = ToolPage(driver)
    agent_page = AgentPage(driver)

    tool_page.go_to_agent_page()
    agent_page.go_to_builder()
    tool_page.remove_tooltip()
    agent_page.create_agent(name="테스트 에이전트", system_prompt="")
    
    errors = agent_page.get_error_messages()
    assert "규칙을 입력해주세요" in errors
    logger.info(f"규칙 누락 오류 메시지 확인 완료: {errors}")
    
# 선택값(한줄 소개, 카테고리, 시작 대화) 입력 
def test_agent_create_with_all_optional(logged_in_driver):
    logger.info("에이전트 생성 테스트 시작 - 선택값 입력")
    driver = logged_in_driver

    tool_page = ToolPage(driver)
    agent_page = AgentPage(driver)

    tool_page.go_to_agent_page()
    agent_page.go_to_builder()
    tool_page.remove_tooltip()

    agent_page.create_agent(
        name="자동화 테스트 에이전트",
        description="자동화 테스트 한줄 소개 입니다.",
        system_prompt="존댓말 사용",
        purpose="education",
        conversation_starters=["시작 대화 1"]
        )
    assert agent_page.is_agent_created(), "에이전트 생성 실패 - 성공 알림 미출력"
    logger.info("에이전트 생성 테스트 완료 - 선택값 모두 입력")