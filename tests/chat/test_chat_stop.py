import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import STOP_BTN_XPATH, send_question


# ────────────────────────────────────────────────────────────────
# CHAT-01-001: 생성 중단 및 즉시 재질문 테스트
# 답변이 생성되는 도중 중단 버튼을 눌렀을 때
# 입력창이 다시 활성화되어 바로 재질문이 가능한지 확인
#
# 검증 포인트:
# 1. 중단 버튼이 정상적으로 동작하는지
# 2. 중단 후 입력창이 즉시 활성화 상태로 돌아오는지
# ────────────────────────────────────────────────────────────────
def test_chat_stop_and_reenter(logged_in_driver):
    driver = logged_in_driver
    # 최대 15초 동안 요소를 찾을 때까지 대기하는 설정
    wait = WebDriverWait(driver, 15)

    # ── 1. 질문 전송 ──────────────────────────────────────────────
    # 답변이 길게 생성되는 질문을 전송해서
    # 중단 버튼을 누를 시간을 확보
    send_question(driver, wait, "QA의 역사를 길게 서술해줘")
    print("\n  ✅ 질문 전송 완료")

    # ── 2. 중단 버튼 나타날 때까지 대기 ─────────────────────────
    # AI 가 답변을 생성하기 시작하면 입력창 옆에 중단(stop) 버튼이 나타남
    # 이 버튼이 클릭 가능한 상태가 될 때까지 대기
    stop_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, STOP_BTN_XPATH))
    )

    # ── 3. 5초 후 중단 버튼 클릭 ─────────────────────────────────
    # 바로 중단하면 답변이 거의 없는 상태라 의미가 없으므로
    # 5초 기다려서 답변이 어느 정도 생성된 후 중단
    time.sleep(5)
    stop_button.click()
    print("  ✅ 생성 중단 완료")

    # ── 4. 입력창 재활성화 확인 ──────────────────────────────────
    # 중단 후 입력창이 다시 활성화되어야 바로 재질문이 가능
    # 5초 안에 입력창이 클릭 가능한 상태가 되지 않으면 실패
    input_box = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[name='input']"))
    )
    # is_enabled() 로 입력창이 실제로 사용 가능한 상태인지 확인
    assert input_box.is_enabled(), "❌ 중단 후 입력창이 비활성화 상태입니다."
    print("  ✅ 입력창 재활성화 확인 완료")