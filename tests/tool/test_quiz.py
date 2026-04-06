import time

import pytest
import allure
from src.pages.tool.tool_page import ToolPage
from src.pages.tool.quiz_page import QuizPage
from src.utils.logger import setup_logger

logger = setup_logger("TestQuiz")

@pytest.fixture
def quiz_ready(logged_in_driver):
    tool_page = ToolPage(logged_in_driver)
    quiz_page = QuizPage(logged_in_driver)

    tool_page.go_to_tool_page()
    quiz_page.go_to_quiz()

    return quiz_page

@allure.epic("도구")
@allure.feature("퀴즈")
@allure.story("퀴즈 생성")
@allure.title("퀴즈 생성 중 중지 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_quiz_creation_with_stop(quiz_ready):
    quiz_page = quiz_ready
    logger.info("quiz 생성 중 중지 테스트 시작")

    quiz_page.create_quiz(
        option_type="객관식(단일 선택)",
        difficulty="중",
        content="영단어",
    )

    quiz_page.stop_creation()

    alert_text = quiz_page.get_stop_alert_text()
    assert alert_text is not None, "중단 알림이 표시되지 않음"
    assert "중지" in alert_text
    logger.info("퀴즈 생성 중 중지 테스트 완료")
    
@allure.epic("도구")
@allure.feature("퀴즈")
@allure.story("퀴즈 생성")
@allure.title("필수값 입력 후 정상 생성 확인")
@allure.severity(allure.severity_level.CRITICAL)
def test_quiz_create_required_only(quiz_ready):
    quiz_page = quiz_ready
    logger.info("퀴즈 생성 테스트 시작 - 필수값 모두 입력")

    quiz_page.create_quiz(
        option_type="객관식(단일 선택)",
        difficulty="중",
        content="영단어",
    )

    is_disabled = quiz_page.check_inputs_disabled_during_creation()
    assert is_disabled, "생성 중 입력 요소가 비활성화되지 않음"
    logger.info("생성 중 입력 요소 비활성화 확인 완료")

    quiz_page.verify_quiz_generated()
    logger.info("퀴즈 생성 성공 - 필수값 모두 입력")

@allure.epic("도구")
@allure.feature("퀴즈")
@allure.story("퀴즈 생성")
@allure.title("주제 미입력 시 에러 메시지 및 버튼 비활성화 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_quiz_create_no_content(quiz_ready):
    quiz_page = quiz_ready
    logger.info("퀴즈 생성 테스트 시작 - 주제 미입력")

    quiz_page.create_quiz(
        option_type="객관식(단일 선택)",
        difficulty="중",
        content="",
    )

    error_msg = quiz_page.get_content_error_message()
    assert error_msg == "1자 이상 입력해주세요.", f"에러 메시지가 올바르지 않음: {error_msg}"
    logger.info(f"에러 메시지 확인 완료: {error_msg}")

    is_btn_disabled = quiz_page.check_submit_button_disabled()
    assert is_btn_disabled, "주제 미입력 시 생성 버튼이 활성화되어 있음"
    logger.info("생성 버튼 비활성화 확인 완료")

@allure.epic("도구")
@allure.feature("퀴즈")
@allure.story("퀴즈 생성")
@allure.title("유형별 퀴즈 생성 및 형식 확인")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("option_type", [
    "객관식(단일 선택)",
    "객관식(복수 선택)",
    "주관식",
])
def test_quiz_create_by_option_type(quiz_ready, option_type):
    quiz_page = quiz_ready
    logger.info(f"퀴즈 생성 테스트 시작 - 유형: {option_type}")

    quiz_page.create_quiz(
        option_type=option_type,
        difficulty="중",
        content="영단어",
    )
    quiz_page.verify_quiz_generated()
    logger.info(f"퀴즈 생성 성공 - 유형: {option_type}")

    item_count = quiz_page.get_answer_item_count() # 답안 항목 개수
    correct_count = quiz_page.get_correct_answer_count() # 정답 개수

    if option_type == "객관식(단일 선택)":
        assert item_count >= 2, f"항목 개수 오류(2개 이상 X), 실제: {item_count}"
        assert correct_count == 1, f"정답 개수 오류(1개 X), 실제: {correct_count}"
    elif option_type == "객관식(복수 선택)":
        assert item_count >= 2, f"항목 개수 오류(2개 이상 X), 실제: {item_count}"
        assert correct_count >= 2, f"정답 개수 오류(2개 이상 X), 실제: {correct_count}"
    elif option_type == "주관식":
        assert item_count == 1, f"항목 개수 오류(1개 X), 실제: {item_count}"
        assert correct_count == 1, f"정답 개수 오류(1개 X), 실제: {correct_count}"

    logger.info(f"퀴즈 형식 검증 완료 - 유형: {option_type}, 항목: {item_count}, 정답: {correct_count}")
    
@allure.epic("도구")
@allure.feature("퀴즈")
@allure.story("퀴즈 생성")
@allure.title("난이도별 퀴즈 생성 확인")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("difficulty", ["상", "중", "하"])
def test_quiz_create_by_difficulty(quiz_ready, difficulty):
    quiz_page = quiz_ready
    logger.info(f"퀴즈 생성 테스트 시작 - 난이도: {difficulty}")

    quiz_page.create_quiz(
        option_type="객관식(단일 선택)",
        difficulty=difficulty,
        content="영단어",
    )
    quiz_page.verify_quiz_generated()
    logger.info(f"퀴즈 생성 성공 - 난이도: {difficulty}")

@allure.epic("도구")
@allure.feature("퀴즈")
@allure.story("퀴즈 생성")
@allure.title("특수문자 및 긴 입력값 처리 확인")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.parametrize("case", [
    {"name": "정상", "content": "영단어 테스트"},
    {"name": "특수문자", "content": "!@#$%^&*()_+"},
    {"name": "긴문자열", "content": "영단어 테스트" * 150},
])
def test_quiz_create_special_and_long_input(quiz_ready, case):
    quiz_page = quiz_ready
    logger.info(f"퀴즈 생성 테스트 시작 - {case['name']}")

    quiz_page.create_quiz(
        option_type="객관식(단일 선택)",
        difficulty="중",
        content=case["content"],
    )
    quiz_page.verify_quiz_generated()
    logger.info(f"퀴즈 생성 성공 - {case['name']} 입력")
    
@allure.epic("도구")
@allure.feature("퀴즈")
@allure.story("퀴즈 생성")
@allure.title("네트워크 오류 시 에러 메시지 출력 확인")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.xfail(reason="네트워크 오류 시 에러 메시지 미출력 버그")
def test_quiz_network_timeout(quiz_ready, logged_in_driver):
    quiz_page = quiz_ready
    driver = logged_in_driver
    logger.info("퀴즈 생성 테스트 시작 - 네트워크 지연")

    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.emulateNetworkConditions", {
        "offline": False,
        "latency": 10000,
        "downloadThroughput": 500,
        "uploadThroughput": 500,
    })
    logger.info("네트워크 스로틀링 적용 완료")

    try:
        quiz_page.create_quiz(
            option_type="객관식(단일 선택)",
            difficulty="중",
            content="영단어",
        )

        # 에러 메시지가 표시되어야 함
        error_msg = quiz_page.get_network_error_message()
        assert error_msg is not None, "네트워크 오류 시 에러 메시지가 표시되지 않음"

    finally:
        driver.execute_cdp_cmd("Network.emulateNetworkConditions", {
            "offline": False,
            "latency": 0,
            "downloadThroughput": -1,
            "uploadThroughput": -1,
        })
        logger.info("네트워크 스로틀링 해제 완료")