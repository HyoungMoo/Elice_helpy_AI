import pytest
from selenium.webdriver.support.ui import WebDriverWait

from src.pages.chat.chat_page import ChatPage


# ────────────────────────────────────────────────────────────────
# CHAT-01-007: 대용량 텍스트 답변 테스트
# ────────────────────────────────────────────────────────────────

MIN_LENGTH = 3000


class TestLongAnswer:

    def test_long_answer(self, logged_in_driver):
        """3000자 이상 답변 생성 여부 확인"""
        driver = logged_in_driver
        wait = WebDriverWait(driver, 30)
        chat_page = ChatPage(driver)

        print("\n[테스트] 대용량 텍스트 답변 테스트")

        # ── 1. 질문 전송 ──────────────────────────────────────────────
        chat_page.send_question("아무 주제로 3000자 이상의 보고서를 작성해줘")
        print("  ✅ 질문 전송 완료")

        # ── 2. 답변 완료 대기 ─────────────────────────────────────────
        answer = chat_page.wait_for_answer("대용량 답변", timeout=300)
        answer_text = answer.text.strip()

        print(f"  ✅ 답변 생성 완료 (길이: {len(answer_text)}자)")

        # ── 3. 답변 길이 검증 ─────────────────────────────────────────
        assert len(answer_text) >= MIN_LENGTH, (
            f"❌ 답변이 너무 짧습니다. "
            f"(현재: {len(answer_text)}자 / 기준: {MIN_LENGTH}자 이상)"
        )

        print(f"  📏 답변 길이: {len(answer_text)}자")
        print(f"  ✅ 대용량 답변 확인 완료 ({len(answer_text)}자 ≥ {MIN_LENGTH}자)")

        print("\n🎉 대용량 텍스트 답변 테스트 통과!")