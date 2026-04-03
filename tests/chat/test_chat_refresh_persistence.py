import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.pages.chat.chat_page import ChatPage
from src.utils.chat_locators import ChatLocators

STOP_BTN_XPATH = ChatLocators.STOP_BTN[1]


# ────────────────────────────────────────────────────────────────
# CHAT-01-004: 브라우저 새로고침 및 재접속 테스트
# 답변이 생성되는 도중에 브라우저를 새로고침했을 때
# 페이지가 정상 복구되고 답변이 재생성되는지 확인
# ────────────────────────────────────────────────────────────────
class TestRefresh:

    def test_answer_regenerates_after_refresh_during_generation(self, logged_in_driver):
        """답변 생성 도중 새로고침 시 답변이 재생성되는지 확인"""
        driver = logged_in_driver
        wait = WebDriverWait(driver, 60)
        chat_page = ChatPage(driver)

        # ── 1. 질문 전송 ──────────────────────────────────────────────
        chat_page.send_question("대한민국의 근현대사를 아주 상세하게 서술해줘.")
        print("\n  ✅ 질문 전송 완료")

        # ── 2. 답변 생성 시작 확인 후 5초 대기 ──────────────────────
        wait.until(EC.presence_of_element_located((By.XPATH, STOP_BTN_XPATH)))
        print("  ⏳ 답변 생성 중 확인 — 5초 후 새로고침 수행")
        time.sleep(10)

        # ── 3. 답변 생성 도중 새로고침 ───────────────────────────────
        driver.refresh()
        print("  📍 새로고침 수행 완료")

        # ── 4. 새로고침 후 답변 재생성 완료 대기 ─────────────────────
        print("  ⏳ 답변 재생성 대기 중...")
        answer = chat_page.wait_for_answer("재생성 확인", timeout=120)

        # ── 5. 재생성된 답변 내용 확인 ───────────────────────────────
        assert len(answer.text.strip()) > 0, "❌ 새로고침 후 답변이 재생성되지 않았습니다."
        print(f"  ✅ 답변 재생성 확인 완료 (길이: {len(answer.text)}자)")

        print("\n🎉 브라우저 새로고침 및 재접속 테스트 통과!")