import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_chat_stop_and_reenter(logged_in_driver):
    driver = logged_in_driver

    # 1. 질문 입력 후 전송
    input_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[name='input']"))
    )
    input_box.send_keys("QA의 역사를 길게 서술해줘")

    send_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='보내기']")
    send_button.click()

    # 2. 중단 버튼 나타날 때까지 대기
    stop_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//*[@data-testid='stopIcon']]"))
    )

    # 3. 3초 뒤 중단 버튼 클릭
    time.sleep(10)
    stop_button.click()

    # 4. 입력창 다시 활성화 확인
    input_box = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[name='input']"))
    )
    assert input_box.is_enabled()