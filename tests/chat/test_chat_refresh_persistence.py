import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_refresh_during_generation(logged_in_driver):
    driver = logged_in_driver
    wait = WebDriverWait(driver, 15)

   # 1. 질문 전송 (팀장님이 강조하신 그 Selector!)
    input_box = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[name='input']"))
    )
    input_box.send_keys("대한민국의 근현대사를 상세히 써줘.")
    input_box.send_keys(Keys.ENTER)
    print("\n 질문 전송 완료.")

    # 2. 답변이 최소 10자 이상 써질 때까지 정밀 대기 (타이밍 조절)
    wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, ".elice-aichat__markdown")[-1].text.strip()) > 10)
    time.sleep(2) # 데이터가 조금 더 쌓이게 2초만 더 기다림
    
    before_text = driver.find_elements(By.CSS_SELECTOR, ".elice-aichat__markdown")[-1].text.strip()
    
    # 3. [액션] 답변 도중 새로고침
    print(" 답변 생성 도중 새로고침 수행!")
    driver.refresh()
    
    # 4. [검증 1] 새로고침 후 다시 그 '입력창'이 나타나고 클릭 가능한가?
    print(" 새로고침 후 입력창 상태 확인 중...")
    try:
        # 팀장님이 짚어주신 바로 그 Selector로 재확인
        re_input_box = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[name='input']"))
        )
        assert re_input_box.is_enabled(), " 새로고침 후 입력창이 비활성화(disabled) 상태입니다!"
        print(" 입력창 재활성화 확인 완료.")
        
    except Exception as e:
        pytest.fail(f" 새로고침 후 입력창을 찾을 수 없거나 사용할 수 없습니다: {str(e)}")

    # 5. [검증 2] 기존 답변 내용이 보존되었는가?
    after_messages = driver.find_elements(By.CSS_SELECTOR, ".elice-aichat__markdown")
    after_text = after_messages[-1].text.strip()
    
    assert before_text[:20] in after_text, " 데이터 유실! 새로고침 전 내용이 사라졌습니다."
    print("데이터 보존 및 UI 복구 확인 성공!")