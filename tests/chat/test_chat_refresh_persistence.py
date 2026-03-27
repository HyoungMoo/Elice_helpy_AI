import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import STOP_BTN_XPATH, send_question, wait_for_answer


# ────────────────────────────────────────────────────────────────
# CHAT-01-004: 브라우저 새로고침 및 재접속 테스트
# 답변이 생성되는 도중에 브라우저를 새로고침했을 때
# 페이지가 정상 복구되고 답변이 재생성되는지 확인
#
# 검증 포인트:
# 1. 새로고침 후 답변이 다시 생성되는지
# 2. 재생성된 답변이 비어있지 않은지
# ────────────────────────────────────────────────────────────────
def test_refresh_during_generation(logged_in_driver):
    driver = logged_in_driver
    # 최대 60초 동안 요소를 찾을 때까지 대기하는 설정
    # 긴 답변 생성 특성상 여유있게 60초로 설정
    wait = WebDriverWait(driver, 60)

    # ── 1. 질문 전송 ──────────────────────────────────────────────
    # 답변이 길게 생성되는 질문을 전송해서
    # 새로고침할 시간을 확보
    send_question(driver, wait, "대한민국의 근현대사를 아주 상세하게 서술해줘.")
    print("\n  ✅ 질문 전송 완료")

    # ── 2. 답변 생성 시작 확인 후 5초 대기 ──────────────────────
    # stopIcon(중단 버튼)이 나타나면 AI 가 답변을 생성 중인 것
    # 바로 새로고침하면 답변이 거의 없는 상태라 의미가 없으므로
    # 5초 기다려서 답변이 어느 정도 생성된 후 새로고침
    wait.until(EC.presence_of_element_located((By.XPATH, STOP_BTN_XPATH)))
    print("  ⏳ 답변 생성 중 확인 — 5초 후 새로고침 수행")
    time.sleep(5)

    # ── 3. 답변 생성 도중 새로고침 ───────────────────────────────
    # 실제 사용자가 답변 생성 중에 새로고침하는 상황을 재현
    driver.refresh()
    print("  📍 새로고침 수행 완료")

    # ── 4. 새로고침 후 답변 재생성 완료 대기 ─────────────────────
    # 새로고침하면 이전 질문에 대한 답변이 다시 생성됨
    # timeout 을 120초로 넉넉하게 설정 (긴 답변이라 시간이 걸림)
    print("  ⏳ 답변 재생성 대기 중...")
    answer = wait_for_answer(driver, "재생성 확인", timeout=120)

    # ── 5. 재생성된 답변 내용 확인 ───────────────────────────────
    # 답변이 비어있지 않으면 정상적으로 재생성된 것
    assert len(answer.text.strip()) > 0, "❌ 새로고침 후 답변이 재생성되지 않았습니다."
    print(f"  ✅ 답변 재생성 확인 완료 (길이: {len(answer.text)}자)")

    print("\n🎉 브라우저 새로고침 및 재접속 테스트 통과!")