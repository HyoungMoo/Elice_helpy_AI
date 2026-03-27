import pytest
from selenium.webdriver.support.ui import WebDriverWait

from helpers import send_question, wait_for_answer


# ────────────────────────────────────────────────────────────────
# CHAT-01-007: 대용량 텍스트 답변 테스트
# 3000자 이상의 긴 답변을 요청했을 때
# AI 가 실제로 3000자 이상의 답변을 생성하는지 확인
# ────────────────────────────────────────────────────────────────

# 답변이 통과하기 위한 최소 글자 수 기준
MIN_LENGTH = 3000


def test_long_answer(logged_in_driver):
    driver = logged_in_driver
    # 최대 30초 동안 요소를 찾을 때까지 대기하는 설정
    wait = WebDriverWait(driver, 30)

    print("\n[테스트] 대용량 텍스트 답변 테스트")

    # ── 1. 3000자 이상 보고서 요청 ───────────────────────────────
    # 주제를 특정하지 않고 "아무 주제"로 요청해서
    # AI 가 자유롭게 긴 답변을 생성할 수 있도록 함
    send_question(driver, wait, "아무 주제로 3000자 이상의 보고서를 작성해줘")
    print("  ✅ 질문 전송 완료")

    # ── 2. 답변 완료 대기 ─────────────────────────────────────────
    # 3000자 이상의 긴 답변을 생성하는 데 시간이 오래 걸리므로
    # timeout 을 300초(5분)로 넉넉하게 설정
    answer = wait_for_answer(driver, "대용량 답변", timeout=300)

    # ── 3. 답변 길이 검증 ─────────────────────────────────────────
    # strip() 으로 앞뒤 공백 제거 후 실제 텍스트 길이 측정
    answer_length = len(answer.text.strip())
    print(f"  📏 답변 길이: {answer_length}자")

    # MIN_LENGTH(3000자) 이상이면 통과
    assert answer_length >= MIN_LENGTH, (
        f"❌ 답변이 너무 짧습니다. "
        f"(현재: {answer_length}자 / 기준: {MIN_LENGTH}자 이상)"
    )
    print(f"  ✅ 대용량 답변 확인 완료 ({answer_length}자 ≥ {MIN_LENGTH}자)")

    print("\n🎉 대용량 텍스트 답변 테스트 통과!")