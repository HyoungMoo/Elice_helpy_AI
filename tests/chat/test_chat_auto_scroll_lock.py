import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_scroll_lock_during_generation(logged_in_driver):
    driver = logged_in_driver  # 기존 로그인 세션 그대로 사용
    wait = WebDriverWait(driver, 15)

    # 1. 입력창 확보 (팀장님 코드 스타일대로 WebDriverWait 적용)
    input_box = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[name='input']"))
    )
    
    # 2. 숫자 100까지 출력 요청 (스크롤 발생을 위해 엔터 포함)
    input_box.send_keys("1부터 100까지 숫자를 하나씩 엔터 치면서 써줘. 아주 천천히.")
    input_box.send_keys(Keys.ENTER)
    print("\n 숫자 출력 요청 전송 완료")

    # 3. 답변이 어느 정도 생성되어 스크롤바가 생길 때까지 대기
    time.sleep(4)

    # 4. 스크롤 정보 가져오기 함수 (JS 실행)
    def get_scroll_info():
        return driver.execute_script("""
            return {
                sh: document.documentElement.scrollHeight,
                st: window.pageYOffset || document.documentElement.scrollTop,
                ch: window.innerHeight
            };
        """)

    # 5. [액션] 위쪽으로 강제 스크롤 시도 (자동 추적 방해)
    print(" 사용자가 위로 스크롤 시도 (-800px)")
    driver.execute_script("window.scrollBy(0, -800);")
    time.sleep(1) # 이동 후 고정되는지 관찰

    # 6. [검증] 위치 고정 확인
    info = get_scroll_info()
    dist_from_bottom = info['sh'] - (info['st'] + info['ch'])
    print(f" 현재 바닥과의 거리: {dist_from_bottom}px")

    # 바닥에서 200px 이상 떨어져 있다면 '자동 추적 정지' 성공
    assert dist_from_bottom > 200, " 사용자가 위로 올렸으나 화면이 다시 강제로 하단을 추적 중입니다!"

    # 7. [지속성 확인] 답변이 계속 생성되는 중에도 그 자리에 멈춰있는지 확인
    prev_st = info['st']
    time.sleep(3)
    after_info = get_scroll_info()
    
    # 스크롤 위치(scrollTop)가 변하지 않아야 함 (허용 오차 20px)
    assert abs(prev_st - after_info['st']) < 20, " 답변 생성 중에 화면 위치가 고정되지 않고 흔들립니다."
    print(" 사용자의 스크롤 위치 고정 확인 완료")

    # 8. 마지막으로 전송 버튼이 다시 활성화(답변 종료)될 때까지 대기
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='보내기']")))
    print("🏁테스트 최종 성공!")