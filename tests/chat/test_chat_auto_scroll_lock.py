import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.pages.chat.chat_page import ChatPage, STOP_BTN_XPATH


# ────────────────────────────────────────────────────────────────
# CHAT-01-003: 자동 스크롤 및 뷰 유지 테스트
# 답변이 생성되는 도중 사용자가 위로 스크롤했을 때
# 화면이 강제로 아래로 내려가지 않고 사용자 위치를 유지하는지 확인
# ────────────────────────────────────────────────────────────────
class TestScrollLock:

    def test_scroll_position_stays_fixed_when_user_scrolls_up_during_generation(self, logged_in_driver):
        """답변 생성 중 사용자가 위로 스크롤하면 화면 위치가 고정되는지 확인"""
        driver = logged_in_driver
        wait = WebDriverWait(driver, 15)
        chat_page = ChatPage(driver)

        # ── 1. 질문 전송 ──────────────────────────────────────────────
        # 숫자를 천천히 출력하도록 요청해서
        # 답변이 길게 생성되어 스크롤바가 생기도록 유도
        chat_page.send_question("1부터 100까지 숫자를 하나씩 엔터 치면서 써줘. 아주 천천히.")
        print("\n  ✅ 숫자 출력 요청 전송 완료")

        # ── 2. 스크롤바가 생길 때까지 대기 ──────────────────────────
        # 답변이 어느 정도 쌓여야 스크롤이 생기므로 4초 대기
        time.sleep(4)

        # ── 3. 현재 스크롤 위치 정보를 가져오는 함수 ─────────────────
        # sh: 페이지 전체 높이
        # st: 현재 스크롤된 위치 (위에서 얼마나 내려왔는지)
        # ch: 현재 화면에 보이는 높이
        def get_scroll_info():
            return driver.execute_script("""
                return {
                    sh: document.documentElement.scrollHeight,
                    st: window.pageYOffset || document.documentElement.scrollTop,
                    ch: window.innerHeight
                };
            """)

        # ── 4. 사용자가 위로 스크롤하는 상황 재현 ────────────────────
        # 800px 위로 강제 스크롤해서 사용자가 스크롤을 올린 상황을 만듦
        print("  📍 사용자가 위로 스크롤 시도 (-800px)")
        driver.execute_script("window.scrollBy(0, -800);")
        time.sleep(1)  # 스크롤 후 화면이 반응할 때까지 잠깐 대기

        # ── 5. 화면이 아래로 강제 이동되지 않았는지 확인 ─────────────
        # 바닥과의 거리가 200px 이상이면 자동 스크롤이 발생하지 않은 것
        info = get_scroll_info()
        dist_from_bottom = info['sh'] - (info['st'] + info['ch'])
        print(f"  현재 바닥과의 거리: {dist_from_bottom}px")

        assert dist_from_bottom > 200, \
            "❌ 사용자가 위로 올렸으나 화면이 다시 강제로 하단을 추적 중입니다!"

        # ── 6. 3초 후에도 스크롤 위치가 유지되는지 확인 ─────────────
        # 답변이 계속 생성되는 동안에도 스크롤 위치가 흔들리지 않아야 함
        # 허용 오차 20px 이내면 고정된 것으로 판단
        prev_st = info['st']
        time.sleep(3)
        after_info = get_scroll_info()

        assert abs(prev_st - after_info['st']) < 20, \
            "❌ 답변 생성 중에 화면 위치가 고정되지 않고 흔들립니다."
        print("  ✅ 사용자의 스크롤 위치 고정 확인 완료")

        # ── 7. 답변 생성이 완전히 끝날 때까지 대기 ──────────────────
        # stopIcon(중단 버튼)이 사라지면 답변 생성이 완료된 것
        wait.until(EC.invisibility_of_element_located((By.XPATH, STOP_BTN_XPATH)))
        print("  🏁 테스트 최종 성공!")