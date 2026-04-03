import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.pages.chat.chat_page import ChatPage
from src.utils.chat_locators import ChatLocators

STOP_BTN_XPATH = ChatLocators.STOP_BTN[1]


# ────────────────────────────────────────────────────────────────
# CHAT-01-001: 생성 중단 및 즉시 재질문 테스트
# 답변이 생성되는 도중 중단 버튼을 눌렀을 때
# 입력창이 다시 활성화되어 바로 재질문이 가능한지 확인
# ────────────────────────────────────────────────────────────────
class TestChatStop:

    def test_input_becomes_active_after_stopping_generation(self, logged_in_driver):
        """답변 생성 중단 후 입력창이 즉시 활성화되는지 확인"""
        driver = logged_in_driver
        wait = WebDriverWait(driver, 15)
        chat_page = ChatPage(driver)

        # ── 1. 질문 전송 ──────────────────────────────────────────────
        # 답변이 길게 생성되는 질문을 전송해서
        # 중단 버튼을 누를 시간을 확보
        chat_page.send_question("QA의 역사를 길게 서술해줘")
        print("\n  ✅ 질문 전송 완료")

        # ── 2. 중단 버튼 나타날 때까지 대기 ─────────────────────────
        # AI 가 답변을 생성하기 시작하면 입력창 옆에 중단(stop) 버튼이 나타남
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