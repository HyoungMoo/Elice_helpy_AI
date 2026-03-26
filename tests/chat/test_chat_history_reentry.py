import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_new_chat_and_history_reentry(logged_in_driver):
    driver = logged_in_driver
    wait = WebDriverWait(driver, 15)

    print("\n 대화 목록 상태 확인 중...")
    
    # 1. 사이드바 목록 가져오기 (MUI ListItemButton 구조)
    # 0번은 보통 '새 대화' 버튼, 1번부터가 실제 대화 목록입니다.
    chat_lists = driver.find_elements(By.CSS_SELECTOR, "a.MuiListItemButton-root")
    
    # 2. [데이터 준비] 예전 대화가 없는 경우 하나 생성
    if len(chat_lists) <= 1:
        print(" 기존 대화가 없으므로 테스트용 대화를 생성합니다.")
        input_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[name='input']")))
        input_box.send_keys("테스트용 자동 생성 메시지입니다.")
        input_box.send_keys(Keys.ENTER)
        
        # 답변이 출력될 때까지 대기하여 목록에 반영되도록 함
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".elice-aichat__markdown")))
        time.sleep(2) # 사이드바 UI 갱신 대기
        
        # 목록 다시 로드
        chat_lists = driver.find_elements(By.CSS_SELECTOR, "a.MuiListItemButton-root")

    # 3. [액션 1] 기존 대화방 진입
    print(" 기존 대화방(목록의 첫 번째 방) 진입 중...")
    # 인덱스 1번 클릭 (0번은 '새 대화' 버튼)
    chat_lists[1].click()
    time.sleep(2) # 방 이동 및 메시지 로딩 대기
    
    # 4. [액션 2] 왼쪽 상단 [새 대화] 버튼 클릭하여 빠져나오기
    print(" [새 대화] 버튼 클릭 수행 (전환 테스트)")
    new_chat_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@class, 'MuiListItemButton-root') and .//span[text()='새 대화']]")
    ))
    new_chat_btn.click()

    # 5. [검증 1] URL이 초기화되었는지 확인
    wait.until(lambda d: "/ai-helpy-chat" in d.current_url)
    print(f" 전환된 URL: {driver.current_url}")

    # 6. [검증 2] 화면에 이전 대화 내용(Markdown)이 사라졌는지 확인
    # DOM 로딩 시간을 고려해 잠시 대기 후 체크
    time.sleep(1)
    messages = driver.find_elements(By.CSS_SELECTOR, ".elice-aichat__markdown")
    
    assert len(messages) == 0, f" 새 대화 클릭 후에도 이전 메시지 {len(messages)}개가 남아있습니다!"
    
    # 7. [검증 3] 입력창이 비어있고 활성화되어 있는지 확인
    input_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[name='input']")))
    assert input_box.get_attribute("value") == "", " 새 대화창의 입력창에 텍스트가 남아있습니다!"
    assert input_box.is_enabled(), " 새 대화창의 입력창이 비활성화 상태입니다!"

    print(" [PASS] 기존 방 진입 후 새 대화 전환 테스트 성공!")