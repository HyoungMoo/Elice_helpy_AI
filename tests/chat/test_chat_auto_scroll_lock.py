import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import STOP_BTN_XPATH, send_question

# 자동 스크롤 및 뷰 유지 CHAT-01-003
def test_scroll_lock_during_generation(logged_in_driver):
    driver = logged_in_driver
    wait = WebDriverWait(driver, 15)

    # 1. 질문 전송 (helpers 사용)
    send_question(driver, wait, "1부터 100까지 숫자를 하나씩 엔터 치면서 써줘. 아주 천천히.")
    print("\n  ✅ 숫자 출력 요청 전송 완료")

    # 2. 답변이 어느 정도 생성되어 스크롤바가 생길 때까지 대기
    time.sleep(4)

    # 3. 스크롤 정보 가져오기
    def get_scroll_info():
        return driver.execute_script("""
            return {
                sh: document.documentElement.scrollHeight,
                st: window.pageYOffset || document.documentElement.scrollTop,
                ch: window.innerHeight
            };
        """)

    # 4. 위쪽으로 강제 스크롤 시도
    print("  📍 사용자가 위로 스크롤 시도 (-800px)")
    driver.execute_script("window.scrollBy(0, -800);")
    time.sleep(1)

    # 5. 위치 고정 확인
    info = get_scroll_info()
    dist_from_bottom = info['sh'] - (info['st'] + info['ch'])
    print(f"  현재 바닥과의 거리: {dist_from_bottom}px")

    assert dist_from_bottom > 200, \
        "❌ 사용자가 위로 올렸으나 화면이 다시 강제로 하단을 추적 중입니다!"

    # 6. 지속성 확인 — 답변 생성 중에도 위치 고정되는지
    prev_st = info['st']
    time.sleep(3)
    after_info = get_scroll_info()

    assert abs(prev_st - after_info['st']) < 20, \
        "❌ 답변 생성 중에 화면 위치가 고정되지 않고 흔들립니다."
    print("  ✅ 사용자의 스크롤 위치 고정 확인 완료")

    # 7. 답변 종료까지 대기 (stopIcon 사라지면 완료)
    wait.until(EC.invisibility_of_element_located((By.XPATH, STOP_BTN_XPATH)))
    print("  🏁 테스트 최종 성공!")