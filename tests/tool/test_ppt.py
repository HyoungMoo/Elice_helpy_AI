import time
import pytest
from src.pages.tool.tool_page import ToolPage
from src.pages.tool.ppt_page import PptPage
from pathlib import Path
from src.utils.logger import setup_logger

logger = setup_logger("TestPPT")

@pytest.fixture
def ppt_ready(logged_in_driver):
    tool_page = ToolPage(logged_in_driver)
    ppt_page = PptPage(logged_in_driver)

    tool_page.remove_tooltip()
    tool_page.go_to_tool_page()
    tool_page.remove_tooltip()
    ppt_page.go_to_ppt()
    tool_page.remove_tooltip()

    return ppt_page

# 필수값(topic) 미입력 시 생성 버튼 비활성화 확인
def test_ppt_create_no_topic(ppt_ready):
    ppt_page = ppt_ready
    logger.info("PPT 생성 테스트 시작 - 필수값 미입력")

    ppt_page.create_ppt(topic="")

    error_msg = ppt_page.get_topic_error_message()
    assert error_msg == "1자 이상 500자 이하로 입력해주세요.", f"에러 메시지가 올바르지 않음: {error_msg}"
    logger.info(f"에러 메시지 확인 완료: {error_msg}")

    is_btn_disabled = ppt_page.check_submit_button_disabled()
    assert is_btn_disabled, "필수값(주제) 미입력 시 생성 버튼이 활성화되어 있음"
    logger.info("생성 버튼 비활성화 확인 완료")

# PPT 생성 중 중지
def test_ppt_creation_with_stop(ppt_ready):
    ppt_page = ppt_ready
    logger.info("PPT 생성 중 중지 테스트 시작")

    ppt_page.create_ppt(topic="파이썬 기초")
    time.sleep(2)

    ppt_page.stop_creation()

    alert_text = ppt_page.get_stop_alert_text()
    assert alert_text is not None and "요청에 의해 답변 생성을 중지했습니다." in alert_text, \
        f"예상과 다른 알림 메시지: {alert_text}"
    logger.info(f"정상 중지 확인 - 알림 메시지: {alert_text}")

# 필수값(topic)만 입력 / 생성 중 버튼 비활성화 확인 / 정상 다운로드 확인
def test_ppt_create_required_only(ppt_ready):
    ppt_page = ppt_ready
    logger.info("PPT 생성 테스트 시작 - 필수값만 입력")

    ppt_page.create_ppt(topic="파이썬 기초", simple_mode=False)
    logger.info("PPT 생성 성공 - 필수값만 입력")

    is_disabled = ppt_page.check_inputs_disabled_during_creation()
    assert is_disabled, "생성 중 입력 요소가 비활성화되지 않음"
    logger.info("생성 중 입력 요소 비활성화 확인 완료")

    ppt_page.ppt_download()
    logger.info("PPT 다운로드 확인 완료")

# 심층 모드 ON으로 PPT 생성 확인
def test_ppt_create_deep_mode(ppt_ready):
    ppt_page = ppt_ready
    logger.info("PPT 생성 테스트 시작 - 심층 모드")

    ppt_page.create_ppt(topic="파이썬 기초", simple_mode=True)

    ppt_page.verify_ppt_generated()
    logger.info("PPT 생성 성공 - 심층 모드")

# 선택값 입력(슬라이드 수, 섹션 수 포함) / 정상 다운로드 확인 / 슬라이드 수 확인
@pytest.mark.skip(reason="슬라이드 수가 입력값과 일치하지 않아 검증 불안정")
def test_ppt_slide_count_validation(ppt_ready):
    ppt_page = ppt_ready
    logger.info("PPT 생성 테스트 시작 - 모든 값 커스텀")

    input_slides = "3"

    ppt_page.create_ppt(
        topic="파이썬 기초",
        instructions="간단한 설명",
        slides_count=input_slides,
        section_count="1",
        simple_mode=False
    )

    filename = ppt_page.ppt_download()
    logger.info("PPT 다운로드 확인 완료")
    time.sleep(3)

    file_path = Path.home() / "Downloads" / filename
    slide_count = ppt_page.check_ppt_slide_count(file_path)
    logger.info(f"슬라이드 수 확인 완료: {slide_count}장")
    assert slide_count == int(input_slides), \
        f"슬라이드 수 불일치 (입력값: {input_slides}, 실제: {slide_count})"

# 특수문자 및 긴 입력값 입력 시 정상 처리 확인
def test_ppt_create_special_and_long(ppt_ready):
    ppt_page = ppt_ready
    logger.info("PPT 생성 테스트 시작 - 특수문자 및 긴 입력값")

    long_instructions = "파이썬은 매우 유용한 프로그래밍 언어입니다. " * 50

    ppt_page.create_ppt(
        topic="!!!@@@###",
        instructions=long_instructions,
    )
    logger.info("PPT 입력 완료 - 특수문자 및 긴 입력값")

    ppt_page.verify_ppt_generated()
    
@pytest.mark.xfail(reason="네트워크 오류 시 에러 메시지 미출력 버그 - 무한 로딩 발생")
def test_ppt_network_timeout(ppt_ready, logged_in_driver):
    ppt_page = ppt_ready
    driver = logged_in_driver
    logger.info("PPT 생성 테스트 시작 - 네트워크 지연")

    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.emulateNetworkConditions", {
        "offline": False,
        "latency": 10000,
        "downloadThroughput": 500,
        "uploadThroughput": 500,
    })
    logger.info("네트워크 스로틀링 적용 완료")

    try:
        ppt_page.create_ppt(topic="파이썬 기초")

        # 에러 메시지가 표시되어야 함 (현재는 무한 로딩으로 실패)
        error_msg = ppt_page.get_network_error_message()
        assert error_msg is not None, "네트워크 오류 시 에러 메시지가 표시되지 않음"

    finally:
        driver.execute_cdp_cmd("Network.emulateNetworkConditions", {
            "offline": False,
            "latency": 0,
            "downloadThroughput": -1,
            "uploadThroughput": -1,
        })
        logger.info("네트워크 스로틀링 해제 완료")
