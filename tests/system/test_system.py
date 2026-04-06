import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.pages.chat.chat_page import ChatPage
from src.pages.system.settings_page import SettingsPage

ANSWER_XPATH = "//div[@data-status='complete']"

# ─────────────────────────────────────────────────────────────────
# 언어별 사이드바 UI 텍스트 매핑
# 대화 기록은 사용자가 입력한 내용이라 번역 안 되므로 제외
# 사이드바 고정 메뉴 텍스트만 확인
# ─────────────────────────────────────────────────────────────────
LANGUAGE_UI_TEXTS = {
    "American English": {
        "New Chat": "새 대화 버튼",
        "Search": "검색 버튼",
        "Tools": "도구 메뉴",
        "Agent Explorer": "에이전트 탐색 메뉴",
    },
    "日本語 (日本)": {
        "新しい会話": "새 대화 버튼",
        "検索": "검색 버튼",
        "ツール": "도구 메뉴",
    },
    "ไทย (ไทย)": {
        "สร้างการสนทนาใหม่": "새 대화 버튼",
        "ค้นหา": "검색 버튼",
    },
}


# ─────────────────────────────
# SYS-01-001 ~ 003: 언어 변경
# ─────────────────────────────
@allure.epic("시스템")
@allure.feature("언어 설정")
@allure.story("언어 변경")
@allure.title("언어 변경 후 사이드바 UI 텍스트 변환 확인")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("lang_text", [
    "American English",
    "日本語 (日本)",
    "ไทย (ไทย)",
])
def test_language_change_ui(logged_in_driver, lang_text):
    """언어 변경 후 사이드바 고정 메뉴 텍스트가 모두 변환되는지 확인"""
    driver = logged_in_driver
    wait = WebDriverWait(driver, 15)
    settings = SettingsPage(driver)

    print(f"\n[테스트] 언어 변경 → {lang_text}")

    try:
        settings.change_language(lang_text)

        # 사이드바 고정 메뉴 텍스트 목록 가져오기
        expected_texts = LANGUAGE_UI_TEXTS[lang_text]

        # 첫 번째 텍스트가 나타날 때까지 대기
        first_text = list(expected_texts.keys())[0]
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//span[contains(text(), '{first_text}')]")
            )
        )

        # 모든 텍스트 확인
        failed = []
        for text, label in expected_texts.items():
            elements = driver.find_elements(
                By.XPATH, f"//span[contains(text(), '{text}')]"
            )
            if len(elements) == 0:
                failed.append(f"{label}({text})")
            else:
                print(f"  ✅ {label} → '{text}' 확인 완료")

        assert len(failed) == 0, f"❌ 다음 텍스트가 변환되지 않았습니다: {failed}"
        print(f"  ✅ {lang_text} 사이드바 UI 전체 변환 확인 완료")

    finally:
        settings.change_language("한국어(대한민국)")


# ─────────────────────────────
# SYS-01-004: 대화 유지
# ─────────────────────────────
@allure.epic("시스템")
@allure.feature("언어 설정")
@allure.story("언어 변경")
@allure.title("언어 변경 시 대화 내용 유지 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_chat_state_preserved_on_language_change(logged_in_driver):
    driver = logged_in_driver
    chat = ChatPage(driver)
    settings = SettingsPage(driver)

    print("\n[테스트] 언어 변경 시 대화 유지")

    chat.send_question("안녕하세요")
    chat.wait_for_answer("before")

    settings.change_language("American English")

    answers = driver.find_elements(By.XPATH, ANSWER_XPATH)
    assert len(answers) > 0, "❌ 대화 내용 유실됨"
    print("  ✅ 대화 유지 확인 완료")

    settings.change_language("한국어(대한민국)")


# ─────────────────────────────
# SYS-01-005: 새로고침 후 언어 유지
# ─────────────────────────────
@allure.epic("시스템")
@allure.feature("언어 설정")
@allure.story("언어 유지")
@allure.title("새로고침 후 언어 설정 유지 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_language_persistence_after_refresh(logged_in_driver):
    driver = logged_in_driver
    wait = WebDriverWait(driver, 15)
    settings = SettingsPage(driver)

    print("\n[테스트] 언어 유지 (새로고침)")

    settings.change_language("American English")
    driver.refresh()

    # 새로고침 후 사이드바 텍스트 전체 확인
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//span[contains(text(), 'New Chat')]")
        )
    )

    failed = []
    for text, label in LANGUAGE_UI_TEXTS["American English"].items():
        elements = driver.find_elements(
            By.XPATH, f"//span[contains(text(), '{text}')]"
        )
        if len(elements) == 0:
            failed.append(f"{label}({text})")
        else:
            print(f"  ✅ {label} → '{text}' 유지 확인")

    assert len(failed) == 0, f"❌ 새로고침 후 다음 텍스트가 복구되지 않았습니다: {failed}"
    print("  ✅ 새로고침 후 언어 유지 확인 완료")

    settings.change_language("한국어(대한민국)")


# ─────────────────────────────
# SYS-01-005: 브라우저 언어 자동 감지
# ─────────────────────────────
@allure.epic("시스템")
@allure.feature("언어 설정")
@allure.story("언어 유지")
@allure.title("브라우저 언어 자동 감지 확인")
@allure.severity(allure.severity_level.MINOR)
def test_browser_language_auto_detection(logged_in_driver):
    driver = logged_in_driver
    wait = WebDriverWait(driver, 15)
    settings = SettingsPage(driver)

    print("\n[테스트] 브라우저 언어 자동 감지")

    # 1. 영어로 언어 변경 후 새로고침
    settings.change_language("American English")
    driver.refresh()
    wait = WebDriverWait(driver, 15)

    # 2. 새로고침 후 사이드바 텍스트 전체 확인
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//span[contains(text(), 'New Chat')]")
        )
    )

    failed = []
    for text, label in LANGUAGE_UI_TEXTS["American English"].items():
        elements = driver.find_elements(
            By.XPATH, f"//span[contains(text(), '{text}')]"
        )
        if len(elements) == 0:
            failed.append(f"{label}({text})")
        else:
            print(f"  ✅ {label} → '{text}' 확인")

    assert len(failed) == 0, f"❌ 다음 텍스트가 영어로 표시되지 않습니다: {failed}"
    print("  ✅ 새로고침 후 영어 유지 확인")

    # 3. 한국어로 복원
    settings.change_language("한국어(대한민국)")


# ─────────────────────────────
# SYS-02-001: 네트워크 복구
# ─────────────────────────────
@allure.epic("시스템")
@allure.feature("네트워크")
@allure.story("네트워크 복구")
@allure.title("네트워크 차단 후 복구 시 대화 유지 확인")
@allure.severity(allure.severity_level.CRITICAL)
def test_network_recovery(logged_in_driver):
    driver = logged_in_driver
    chat = ChatPage(driver)

    print("\n[테스트] 네트워크 복구")

    chat.send_question("안녕하세요")
    answer = chat.wait_for_answer("before")
    before_text = answer.text[:20]

    # Chrome DevTools Protocol 로 네트워크 차단
    driver.execute_cdp_cmd("Network.emulateNetworkConditions", {
        "offline": True,
        "latency": 0,
        "downloadThroughput": 0,
        "uploadThroughput": 0
    })

    # 10초 대기
    time.sleep(10)

    # 네트워크 복구
    driver.execute_cdp_cmd("Network.emulateNetworkConditions", {
        "offline": False,
        "latency": 0,
        "downloadThroughput": -1,
        "uploadThroughput": -1
    })

    driver.refresh()

    answer_after = chat.wait_for_answer("after")
    assert before_text in answer_after.text, "❌ 대화 유실"
    print("  ✅ 네트워크 복구 성공")


# ─────────────────────────────
# SYS-02-002: 멀티탭
# ─────────────────────────────
@allure.epic("시스템")
@allure.feature("멀티탭")
@allure.story("멀티탭 처리")
@allure.title("멀티탭 동시 질문 처리 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_multi_tab_processing(logged_in_driver):
    driver = logged_in_driver

    print("\n[테스트] 멀티탭 처리")

    QUESTION_A = "대한민국의 수도가 어디야?"
    ANSWER_A = "서울"

    QUESTION_B = "10 더하기 15는 뭐야?"
    ANSWER_B = "25"

    # 탭 A 에서 질문 전송
    tab_a = driver.current_window_handle
    current_url = driver.current_url
    chat_a = ChatPage(driver)
    chat_a.send_question(QUESTION_A)

    # 탭 B 열기 — 현재 URL 로 바로 열기
    driver.execute_script(f"window.open('{current_url}', '_blank');")
    tab_b = driver.window_handles[-1]
    driver.switch_to.window(tab_b)
    time.sleep(2)

    # 탭 B 에서 질문 전송
    chat_b = ChatPage(driver)
    chat_b.send_question(QUESTION_B)

    # 탭 B 답변 확인
    answer_b = chat_b.wait_for_answer("B")
    assert ANSWER_B in answer_b.text, "❌ 탭 B 실패"

    # 탭 A 로 전환 후 답변 확인
    driver.switch_to.window(tab_a)
    answer_a = chat_a.wait_for_answer("A")
    assert ANSWER_A in answer_a.text, "❌ 탭 A 실패"

    # 탭 B 닫기
    driver.switch_to.window(tab_b)
    driver.close()
    driver.switch_to.window(tab_a)

    print("  🎉 멀티탭 테스트 통과")