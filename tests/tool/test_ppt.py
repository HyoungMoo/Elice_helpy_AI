import pytest
from selenium.common import TimeoutException
from src.pages.tool.tool_page import ToolPage
from src.pages.tool.ppt_page import PptPage
from pathlib import Path
from src.utils.logger import setup_logger
import time

logger = setup_logger("TestPPT")

# 필수값(topic)만 입력 / 생성 중 버튼 비활성화 확인 / 정상 다운로드 확인
def test_ppt_create_required_only(logged_in_driver):

    driver = logged_in_driver
    logger.info("PPT 생성 테스트 시작 - 필수값만 입력")

    tool_page = ToolPage(driver)
    ppt_page = PptPage(driver)

    tool_page.go_to_tool_page()
    tool_page.remove_tooltip()
    ppt_page.go_to_ppt()
    tool_page.remove_tooltip()

    ppt_page.create_ppt(topic="파이썬 기초")
    logger.info("PPT 생성 성공 - 필수값만 입력")

    is_disabled = ppt_page.check_inputs_disabled_during_creation()
    assert is_disabled, "생성 중 입력 요소가 비활성화되지 않음"
    logger.info("생성 중 입력 요소 비활성화 확인 완료")
    
    ppt_page.ppt_download()
    logger.info("PPT 다운로드 확인 완료")

# 필수값(topic) 미입력 시 생성 버튼 비활성화 확인
def test_ppt_create_no_topic(logged_in_driver):
    
    driver = logged_in_driver
    logger.info("PPT 생성 테스트 시작 - 필수값 미입력")

    tool_page = ToolPage(driver)
    ppt_page = PptPage(driver)

    tool_page.go_to_tool_page()
    tool_page.remove_tooltip()
    ppt_page.go_to_ppt()
    tool_page.remove_tooltip()

    ppt_page.create_ppt(topic="")

    # 에러 메시지 확인
    error_msg = ppt_page.get_topic_error_message()
    assert error_msg == "1자 이상 500자 이하로 입력해주세요.", f"에러 메시지가 올바르지 않음: {error_msg}"
    logger.info(f"에러 메시지 확인 완료: {error_msg}")

    # 버튼 비활성화 확인
    is_btn_disabled = ppt_page.check_submit_button_disabled()
    assert is_btn_disabled, "필수값(주제) 미입력 시 생성 버튼이 활성화되어 있음"
    logger.info("생성 버튼 비활성화 확인 완료")
    
# 특수문자 및 긴 입력값 입력 시 정상 처리 확인 <<<<< 여기 나중에 나눠서 테스트 해보는 것도 나쁘지 않을듯!!!!!
def test_ppt_create_special_and_long(logged_in_driver):

    driver = logged_in_driver
    logger.info("PPT 생성 테스트 시작 - 특수문자 및 긴 입력값")

    tool_page = ToolPage(driver)
    ppt_page = PptPage(driver)

    tool_page.go_to_tool_page()
    tool_page.remove_tooltip()
    ppt_page.go_to_ppt()
    tool_page.remove_tooltip()

    long_instructions = "파이썬은 매우 유용한 프로그래밍 언어입니다. " * 50  # 1000자 이상

    ppt_page.create_ppt(
        topic="!!!@@@###", #특수문자
        instructions=long_instructions,
    )
    logger.info("PPT 입력 완료 - 특수문자 및 긴 입력값")

    is_disabled = ppt_page.check_inputs_disabled_during_creation()
    assert is_disabled, "생성 중 입력 요소가 비활성화되지 않음"
    logger.info("생성 중 입력 요소 비활성화 확인 완료")

    ppt_page.ppt_download()
    logger.info("PPT 다운로드 확인 완료 - 특수문자 및 긴 입력값 정상 처리")
    
# 선택값 입력(슬라이드 수, 섹션 수 포함) / 정상 다운로드 확인/ 슬라이드 수 확인
# with_all_optional
def test_ppt_slide_count_validation(logged_in_driver):
    
    driver = logged_in_driver
    logger.info("PPT 생성 테스트 시작 - 모든 값 커스텀")

    tool_page = ToolPage(driver)
    ppt_page = PptPage(driver)
    
    tool_page.go_to_tool_page()
    tool_page.remove_tooltip()
    ppt_page.go_to_ppt()
    tool_page.remove_tooltip()

    input_slides = "3"  

    ppt_page.create_ppt(
        topic="파이썬 기초",
        instructions="간단한 설명",
        slides_count=input_slides,
        section_count="1",
    )
    logger.info("PPT 생성 성공 - 모든 값 커스텀")

    is_disabled = ppt_page.check_inputs_disabled_during_creation()
    assert is_disabled, "생성 중 입력 요소가 비활성화되지 않음"
    logger.info("생성 중 입력 요소 비활성화 확인 완료")

    filename = ppt_page.ppt_download()
    logger.info("PPT 다운로드 확인 완료")

    # 다운로드 완료 대기
    time.sleep(3)

    # 슬라이드 수 확인
    file_path = Path.home() / "Downloads" / filename
    slide_count = ppt_page.check_ppt_slide_count(file_path)
    logger.info(f"슬라이드 수 확인 완료: {slide_count}장")
    assert slide_count == int(input_slides), f"슬라이드 수 불일치 (입력값: {input_slides}, 실제: {slide_count})"
   
# PPT 생성 중 중지
def test_ppt_creation_with_stop(logged_in_driver):

    driver = logged_in_driver
    logger.info("PPT 생성 중 중지 테스트 시작")

    tool_page = ToolPage(driver)
    ppt_page = PptPage(driver)


    tool_page.go_to_tool_page()
    tool_page.remove_tooltip()
    ppt_page.go_to_ppt()
    tool_page.remove_tooltip()

    ppt_page.create_ppt(topic="파이썬 기초")
    time.sleep(2)

    ppt_page.stop_creation()

    try:
        ppt_page.ppt_download(timeout=5)
        assert False, "중지했는데 다운로드가 실행됨 → 중단 실패"
    except TimeoutException:
        logger.info("정상 중지 확인 - 다운로드 버튼 미노출")
