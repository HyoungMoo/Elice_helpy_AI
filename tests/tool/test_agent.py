from pathlib import Path
import pytest
import allure
from src.pages.tool.tool_page import ToolPage
from src.pages.tool.agent_page import AgentPage
from src.pages.auth.logout_page import LogoutPage
from src.pages.auth.login_page import LoginPage
from datetime import datetime
from src.utils.logger import setup_logger

logger = setup_logger("TestAngent")

@pytest.fixture
def created_agent(logged_in_driver):
    name = f"자동화 테스트 에이전트 {datetime.now().strftime('%H%M%S')}"
    tool_page = ToolPage(logged_in_driver)
    agent_page = AgentPage(logged_in_driver)

    tool_page.go_to_agent_page()
    agent_page.go_to_builder()
    agent_page.create_agent(
        name=name,
        system_prompt="존댓말 사용",
    )
    assert agent_page.is_agent_created(), "에이전트 생성 실패"
    tool_page.remove_tooltip() # 팝업 제거
    return name

@allure.epic("도구")
@allure.feature("에이전트")
@allure.story("에이전트 생성")
@allure.title("필수값(이름, 규칙) 입력 후 생성 성공")
@allure.severity(allure.severity_level.CRITICAL)
def test_agent_create_required_only(created_agent):
    logger.info("에이전트 생성 테스트 완료 - 필수값 모두 입력")

@allure.epic("도구")
@allure.feature("에이전트")
@allure.story("에이전트 생성")
@allure.title("필수값(이름) 누락 시 오류 메시지 출력")
@allure.severity(allure.severity_level.NORMAL)
def test_agent_create_missing_name(logged_in_driver):
    logger.info("에이전트 생성 테스트 시작 - 필수값 이름 누락")
    driver = logged_in_driver

    tool_page = ToolPage(driver)
    agent_page = AgentPage(driver)
    
    tool_page.go_to_agent_page()
    agent_page.go_to_builder()
    agent_page.create_agent(name="", system_prompt="존댓말 사용")
    
    error = agent_page.get_name_error_message()
    assert error is not None, "이름 누락 오류 메시지가 표시되지 않음"
    assert "이름을 입력해주세요" in error
    logger.info(f"이름 누락 오류 메시지 확인 완료: {error}")
    
@allure.epic("도구")
@allure.feature("에이전트")
@allure.story("에이전트 생성")
@allure.title("필수값(규칙) 누락 시 오류 메시지 출력")
@allure.severity(allure.severity_level.NORMAL)
def test_agent_create_missing_system_prompt(logged_in_driver):
    logger.info("에이전트 생성 테스트 시작 - 필수값 규칙 누락")
    driver = logged_in_driver

    tool_page = ToolPage(driver)
    agent_page = AgentPage(driver)

    tool_page.go_to_agent_page()
    agent_page.go_to_builder()
    agent_page.create_agent(name="테스트 에이전트", system_prompt="")
    
    error = agent_page.get_rule_error_message()
    assert error is not None, "규칙 누락 오류 메시지가 표시되지 않음"
    assert "규칙을 입력해주세요" in error
    logger.info(f"규칙 누락 오류 메시지 확인 완료: {error}")
   
@allure.epic("도구")
@allure.feature("에이전트")
@allure.story("에이전트 생성")
@allure.title("선택값(소개, 카테고리, 시작대화, 기능) 포함 생성 성공")
@allure.severity(allure.severity_level.NORMAL)
def test_agent_create_with_all_optional(logged_in_driver):
    logger.info("에이전트 생성 테스트 시작 - 선택값 입력")
    driver = logged_in_driver

    tool_page = ToolPage(driver)
    agent_page = AgentPage(driver)

    tool_page.go_to_agent_page()
    agent_page.go_to_builder()

    agent_page.create_agent(
        name="자동화 테스트 에이전트",
        description="자동화 테스트 한줄 소개 입니다.",
        system_prompt="존댓말 사용",
        purpose="education",
        conversation_starters=["시작 대화 1"],
        tool_ids=["web_search", "image_generation"]
        )
    assert agent_page.is_agent_created(), "에이전트 생성 실패 - 성공 알림 미출력"
    logger.info("에이전트 생성 테스트 완료 - 선택값 모두 입력")
    
BASE_DIR = Path(__file__).parent
PROJECT_ROOT = BASE_DIR.parent.parent

@allure.epic("도구")
@allure.feature("에이전트")
@allure.story("에이전트 생성")
@allure.title("파일 업로드 포함 에이전트 생성 성공")
@allure.severity(allure.severity_level.NORMAL)
def test_agent_create_with_file(logged_in_driver):
    logger.info("에이전트 생성 테스트 시작 - 파일 업로드")
    driver = logged_in_driver

    tool_page = ToolPage(driver)
    agent_page = AgentPage(driver)

    file_path = str(PROJECT_ROOT / "src" / "resources" / "test_files" / "sample.pdf")

    tool_page.go_to_agent_page()
    agent_page.go_to_builder()

    agent_page.upload_file(file_path) # 파일 업로드
    agent_page.create_agent(
        name="파일 업로드 테스트 에이전트",
        system_prompt="존댓말 사용",
    )

    assert agent_page.is_agent_created(), "에이전트 생성 실패"
    logger.info("에이전트 생성 성공 - 파일 업로드")

@allure.epic("도구")
@allure.feature("에이전트")
@allure.story("에이전트 생성")
@allure.title("시작 대화 최대 4개 입력 가능 확인")
@allure.severity(allure.severity_level.MINOR)
def test_agent_conversation_starters_max(logged_in_driver):
    logger.info("에이전트 생성 테스트 시작 - 시작 대화 최대 4개")
    driver = logged_in_driver

    tool_page = ToolPage(driver)
    agent_page = AgentPage(driver)

    tool_page.go_to_agent_page()
    agent_page.go_to_builder()

    agent_page.create_agent(
        name="시작 대화 테스트 에이전트",
        system_prompt="존댓말 사용",
        conversation_starters=["시작 대화1", "시작 대화2", "시작 대화3", "시작 대화4"],
    )

    assert agent_page.is_agent_created(), "에이전트 생성 실패"
    logger.info("에이전트 생성 성공 - 시작 대화 4개 입력 확인")
    
@allure.epic("도구")
@allure.feature("에이전트")
@allure.story("에이전트 생성")
@allure.title("필수값 입력 후 정상 생성 확인")
@allure.severity(allure.severity_level.CRITICAL)
def test_agent_create_required_only(logged_in_driver):
    logger.info("에이전트 생성 테스트 시작 - 필수값 모두 입력")
    driver = logged_in_driver

    tool_page = ToolPage(driver)
    agent_page = AgentPage(driver)

    tool_page.go_to_agent_page()
    agent_page.go_to_builder()

    agent_page.create_agent(
        name="자동화 테스트 에이전트",
        system_prompt="존댓말 사용"
    )
    assert agent_page.is_agent_created(), "에이전트 생성 실패 - 성공 알림 미출력"
    logger.info("에이전트 생성 테스트 완료 - 필수값 모두 입력")
    
@allure.epic("도구")
@allure.feature("에이전트")
@allure.story("에이전트 수정")
@allure.title("에이전트 수정 후 목록 반영 확인")
@allure.severity(allure.severity_level.CRITICAL)
def test_agent_edit(logged_in_driver, created_agent):
    logger.info("에이전트 수정 테스트 시작")
    driver = logged_in_driver

    tool_page = ToolPage(driver)
    agent_page = AgentPage(driver)

    tool_page.go_to_agent_page()
    agent_page.go_to_mine()
    agent_page.go_to_edit(created_agent)

    agent_page.create_agent(
        name="수정된 에이전트",
        system_prompt="반말 사용",
        is_edit=True
    )
    
    assert agent_page.is_agent_updated(), "에이전트 수정 실패"
    logger.info("에이전트 수정 성공")
    
    # 목록으로 돌아가서 반영 확인
    tool_page.go_to_agent_page()
    agent_page.go_to_mine()
    assert agent_page.is_agent_in_list("수정된 에이전트"), "수정된 에이전트가 목록에 없음"
    logger.info("수정 후 목록 반영 확인 완료")
    
@allure.epic("도구")
@allure.feature("에이전트")
@allure.story("에이전트 삭제")
@allure.title("에이전트 삭제 후 목록에서 제거 확인")
@allure.severity(allure.severity_level.CRITICAL)
def test_agent_delete(logged_in_driver, created_agent):
    logger.info("에이전트 삭제 테스트 시작")
    driver = logged_in_driver
    
    tool_page = ToolPage(driver)
    agent_page = AgentPage(driver)
    
    tool_page.go_to_agent_page()
    agent_page.go_to_mine()
    agent_page.delete_agent(created_agent)
    
    # 목록으로 돌아가서 반영 확인
    assert agent_page.is_agent_deleted(), "에이전트 삭제 실패"
    assert agent_page.is_agent_in_list(created_agent, should_exist=False), "삭제된 에이전트가 목록에 남아있음"
    logger.info("에이전트 삭제 성공")

@allure.epic("도구")
@allure.feature("에이전트")
@allure.story("에이전트 공개 설정")
@allure.title("나만 보기 설정 시 다른 계정에 미노출 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_agent_private_visibility(logged_in_driver):
    logger.info("에이전트 나만 보기 테스트 시작")
    driver = logged_in_driver

    tool_page = ToolPage(driver)
    agent_page = AgentPage(driver)
    logout_page = LogoutPage(driver)
    login_page = LoginPage(driver)

    # user_2로 에이전트 생성 (나만 보기)
    tool_page.go_to_agent_page()
    agent_page.go_to_builder()

    name = f"비공개 에이전트 {datetime.now().strftime('%H%M%S')}"
    agent_page.create_agent(
        name=name,
        system_prompt="존댓말 사용",
        visibility="private"
    )
    assert agent_page.is_agent_created(), "에이전트 생성 실패"
    logger.info("에이전트 생성 완료")

    # user_2 목록에서 확인
    tool_page.go_to_agent_page()
    agent_page.search_agent(name)
    assert agent_page.is_agent_in_list(name), "user_2 목록에서 에이전트 미확인"
    logger.info("user_2 목록 확인 완료")

    # 로그아웃 후 user_1으로 로그인
    logout_page.logout()
    logout_page.sign_different_account()
    login_page.login("user_1")
    logger.info("user_1 로그인 완료")

    # user_1 목록에서 확인 - 없어야 함
    tool_page.go_to_agent_page()
    agent_page.search_agent(name)
    assert agent_page.is_agent_in_list(name, should_exist=False), "user_1에게 비공개 에이전트가 노출됨"
    logger.info("나만 보기 확인 완료 - user_1에게 미노출")

@allure.epic("도구")
@allure.feature("에이전트")
@allure.story("에이전트 공개 설정")
@allure.title("기관 내 공유 설정 시 다른 계정에 노출 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_agent_organization_visibility(logged_in_driver):
    logger.info("에이전트 기관 내 공유 테스트 시작")
    driver = logged_in_driver
    
    tool_page = ToolPage(driver)
    agent_page = AgentPage(driver)
    login_page = LoginPage(driver)
    logout_page = LogoutPage(driver)
    
    tool_page.go_to_agent_page()
    agent_page.go_to_builder()
    
    name = f"공개 에이전트 {datetime.now().strftime('%H%M%S')}"
    agent_page.create_agent(
        name=name,
        system_prompt="존댓말 사용",
        visibility="organization" # 기관 내 공개
    )
    assert agent_page.is_agent_created(), "에이전트 생성 실패"
    logger.info("에이전트 생성 완료")
    
    # user_2 목록에서 확인
    tool_page.go_to_agent_page()
    agent_page.search_agent(name)
    assert agent_page.is_agent_in_list(name), "user_2 목록에서 에이전트 미확인"
    logger.info("user_2 목록 확인 완료")
    
    # 로그아웃 후 user_1으로 로그인
    logout_page.logout()
    logout_page.sign_different_account()
    login_page.login("user_1")
    logger.info("user_1 로그인 완료")
    
    # user_1 목록에서 확인 - 있어야함
    tool_page.go_to_agent_page()
    agent_page.search_agent(name)
    assert agent_page.is_agent_in_list(name), "user_1 목록에서 에이전트 미확인"
    logger.info("기관 내 공유 확인 완료 - user_1에게 노출")