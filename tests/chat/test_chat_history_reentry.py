import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import ANSWER_XPATH, send_question, wait_for_answer, click_new_chat


# ────────────────────────────────────────────────────────────────
# CHAT-01-012: 새 대화 세션 생성 테스트
# 기존 대화방에 있다가 [새 대화] 버튼을 눌렀을 때
# 새로운 빈 대화 화면으로 정상 전환되는지 확인
# ────────────────────────────────────────────────────────────────
def test_new_chat_and_history_reentry(logged_in_driver):
    driver = logged_in_driver
    # 최대 15초 동안 요소를 찾을 때까지 대기하는 설정
    wait = WebDriverWait(driver, 15)

    print("\n  📍 대화 목록 상태 확인 중...")

    # ── 1. 사이드바 대화 목록 가져오기 ───────────────────────────
    # MuiListItemButton-root 클래스를 가진 a 태그가 대화 목록 항목
    # 0번 인덱스는 [새 대화] 버튼이고 1번부터 실제 대화방 목록
    chat_lists = driver.find_elements(By.CSS_SELECTOR, "a.MuiListItemButton-root")

    # ── 2. 기존 대화가 없으면 테스트용 대화 생성 ─────────────────
    # 사이드바에 [새 대화] 버튼만 있고 기존 대화가 없는 경우
    # 테스트를 위해 대화를 하나 만들어놓음
    if len(chat_lists) <= 1:
        print("  ⏳ 기존 대화가 없으므로 테스트용 대화를 생성.")
        send_question(driver, wait, "테스트용 자동 생성 메시지.")
        wait_for_answer(driver, "사전 준비")
        time.sleep(2)  # 사이드바 UI 갱신 대기
        chat_lists = driver.find_elements(By.CSS_SELECTOR, "a.MuiListItemButton-root")

    # ── 3. 기존 대화방 진입 ───────────────────────────────────────
    # index=1 이 첫 번째 실제 대화방 (index=0 은 [새 대화] 버튼)
    print("  📍 기존 대화방 진입 중...")
    chat_lists[1].click()
    time.sleep(2)  # 대화방 로딩 대기

    # ── 4. [새 대화] 버튼 클릭 ───────────────────────────────────
    # helpers 의 click_new_chat() 사용
    # 클릭 후 빈 새 대화 화면으로 전환되어야 함
    print("  📍 [새 대화] 버튼 클릭")
    click_new_chat(driver, wait)

    # ── 5. URL 이 새 대화 경로로 바뀌었는지 확인 ─────────────────
    # 새 대화 클릭 시 URL 이 /ai-helpy-chat 으로 변경되어야 함
    wait.until(lambda d: "/ai-helpy-chat" in d.current_url)
    print(f"  ✅ 전환된 URL: {driver.current_url}")

    # ── 6. 이전 대화 내용이 사라졌는지 확인 ─────────────────────
    # 새 대화 화면에는 이전 대화방의 메시지가 보이면 안 됨
    time.sleep(1)  # 화면 전환 완료 대기
    messages = driver.find_elements(By.CSS_SELECTOR, ".elice-aichat__markdown")
    assert len(messages) == 0, \
        f"❌ 새 대화 클릭 후에도 이전 메시지 {len(messages)}개가 남아있습니다!"

    # ── 7. 입력창이 비어있고 활성화 상태인지 확인 ────────────────
    # 새 대화 화면의 입력창은 비어있어야 하고 클릭 가능한 상태여야 함
    input_box = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "textarea[name='input']")
    ))
    assert input_box.get_attribute("value") == "", \
        "❌ 새 대화창의 입력창에 텍스트가 남아있습니다!"
    assert input_box.is_enabled(), \
        "❌ 새 대화창의 입력창이 비활성화 상태입니다!"

    print("  ✅ [PASS] 기존 방 진입 후 새 대화 전환 테스트 성공!")