import pytest
from src.pages.tool.tool_page import ToolPage
from src.pages.tool.quiz_page import QuizPage
from src.utils.logger import setup_logger

logger = setup_logger("TestQuiz")

@pytest.fixture
def quiz_ready(logged_in_driver):
    tool_page = ToolPage(logged_in_driver)
    quiz_page = QuizPage(logged_in_driver)

    tool_page.go_to_tool_page()
    tool_page.remove_tooltip()
    quiz_page.go_to_quiz()
    tool_page.remove_tooltip()

    return quiz_page

# 필수값 모두 입력 (정상 생성)
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

# 주제 미입력 시 생성 버튼 비활성화/에러 메시지 출력 확인
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

# 퀴즈 생성 중 중지
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

# 유형별 정상 생성 확인
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

# 난이도별 테스트
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

# 다양한 입력값(특수문자, 긴 문자열) 테스트
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
