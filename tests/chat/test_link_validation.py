import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.pages.chat.chat_page import ChatPage


# ────────────────────────────────────────────────────────────────
# CHAT-01-006: 올바른 링크 제공 테스트
# 링크 제공을 요청하는 질문을 보냈을 때
# 답변에 올바른 URL 이 포함되고 클릭 시 정상 접속되는지 확인
# ────────────────────────────────────────────────────────────────
class TestLinkGoogle:

    def test_google_link_opens_in_new_tab_when_requested(self, logged_in_driver):
        """구글 링크 요청 시 답변에 링크가 포함되고 새 탭으로 열리는지 확인"""
        driver = logged_in_driver
        wait = WebDriverWait(driver, 30)
        chat_page = ChatPage(driver)

        print("\n[테스트] 올바른 링크 제공 테스트")

        # ── 1. 질문 전송 ──────────────────────────────────────────────
        chat_page.send_question("구글 홈페이지 링크 알려줘")
        print("  ✅ 질문 전송 완료")

        # ── 2. 답변 완료 대기 ─────────────────────────────────────────
        answer = chat_page.wait_for_answer("링크 테스트")
        print(f"  ✅ 답변 생성 확인 (길이: {len(answer.text)}자)")

        # ── 3. 답변 안에 google.com 링크 존재 여부 확인 ──────────────
        # 답변 컨테이너 안에서 href 에 google.com 이 포함된 a 태그 탐색
        try:
            link = answer.find_element(By.XPATH, ".//a[contains(@href, 'google.com')]")
        except Exception:
            pytest.fail("❌ 답변에 google.com 링크가 없습니다.")

        # 링크가 화면에 실제로 보이는지 확인 (숨겨진 링크는 클릭 불가)
        assert link.is_displayed(), "❌ 링크가 화면에 보이지 않습니다."
        link_href = link.get_attribute("href")
        print(f"  ✅ 링크 확인 완료: {link_href}")

        # ── 4. 링크 클릭 → 새 탭에서 열리는지 확인 ──────────────────
        # 클릭 전 현재 열려있는 탭 목록 저장
        original_window = driver.current_window_handle
        original_windows = set(driver.window_handles)

        link.click()
        time.sleep(2)

        # 클릭 후 새로 생긴 탭이 있는지 확인
        new_windows = set(driver.window_handles) - original_windows
        assert len(new_windows) > 0, "❌ 링크 클릭 후 새 탭이 열리지 않았습니다."

        # 새로 열린 탭으로 전환
        new_window = new_windows.pop()
        driver.switch_to.window(new_window)
        time.sleep(2)

        # ── 5. 새 탭 URL 이 google.com 인지 확인 ─────────────────────
        current_url = driver.current_url
        print(f"  새 탭 URL: {current_url}")
        assert "google.com" in current_url, \
            f"❌ 새 탭이 google.com으로 접속되지 않았습니다. (현재 URL: {current_url})"
        print("  ✅ 새 탭에서 google.com 정상 접속 확인")

        # ── 6. 원래 탭으로 복귀 ──────────────────────────────────────
        driver.close()
        driver.switch_to.window(original_window)

        print("\n🎉 올바른 링크 제공 테스트 통과!")