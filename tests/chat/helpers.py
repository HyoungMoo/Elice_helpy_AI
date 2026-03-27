import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ────────────────────────────────────────────────────────────────
# 공통 XPath 상수
# ────────────────────────────────────────────────────────────────
STOP_BTN_XPATH      = "//button[.//*[@data-testid='stopIcon']]"
ANSWER_XPATH        = "//div[contains(@class,'elice-aichat__markdown') and @data-status='complete']"
SEND_BTN_XPATH      = "//button[.//*[@data-testid='arrow-upIcon']]"
NEW_CHAT_XPATH      = "//a[contains(@href,'/ai-helpy-chat') and .//span[text()='새 대화']]"
SIDEBAR_ITEMS_XPATH = "//ul[@data-testid='virtuoso-item-list']//a[@data-index]"
CHAT_TITLE_XPATH    = ".//p[contains(@class,'css-ff35j5')]"


# ────────────────────────────────────────────────────────────────
# 헬퍼 함수
# ────────────────────────────────────────────────────────────────

def send_question(driver, wait, question):
    """질문 입력 및 전송"""
    input_box = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[name='input']"))
    )
    input_box.send_keys(question)
    send_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, SEND_BTN_XPATH))
    )
    send_btn.click()


def wait_for_answer(driver, label, timeout=60):
    """
    답변 완료 대기
    1) stopIcon 나타났다가 사라지면 완료
    2) data-status='complete' div 확인
    """
    wait = WebDriverWait(driver, timeout)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, STOP_BTN_XPATH)))
        print(f"  ⏳ [{label}] 답변 생성 중...")
        wait.until(EC.invisibility_of_element_located((By.XPATH, STOP_BTN_XPATH)))
        print(f"  ✅ [{label}] 답변 생성 완료")
    except Exception:
        pass
    time.sleep(1)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, ANSWER_XPATH)))
    except Exception:
        pytest.fail(f"❌ [{label}] {timeout}초 내에 답변이 완료되지 않았습니다.")
    containers = driver.find_elements(By.XPATH, ANSWER_XPATH)
    assert len(containers) > 0 and len(containers[-1].text.strip()) > 0, \
        f"❌ [{label}] 답변이 비어있습니다."
    return containers[-1]


def get_last_answer(driver):
    """마지막 답변 컨테이너 반환"""
    containers = driver.find_elements(By.XPATH, ANSWER_XPATH)
    assert len(containers) > 0, "❌ 답변 요소를 찾을 수 없습니다."
    return containers[-1]


def click_new_chat(driver, wait):
    """새 대화 버튼 클릭"""
    new_chat_btn = wait.until(EC.element_to_be_clickable((By.XPATH, NEW_CHAT_XPATH)))
    new_chat_btn.click()
    time.sleep(1)


def get_sidebar_items(driver, wait, min_count=1):
    """사이드바 항목이 min_count 이상 로딩될 때까지 대기 후 반환"""
    try:
        wait.until(lambda d: len(d.find_elements(By.XPATH, SIDEBAR_ITEMS_XPATH)) >= min_count)
    except Exception:
        pass
    time.sleep(0.5)
    return driver.find_elements(By.XPATH, SIDEBAR_ITEMS_XPATH)


def get_sidebar_titles(driver):
    """사이드바 전체 대화 제목 목록 반환"""
    items = driver.find_elements(By.XPATH, SIDEBAR_ITEMS_XPATH)
    return [item.find_element(By.XPATH, CHAT_TITLE_XPATH).text.strip() for item in items]


def click_more_menu(driver, wait, chat_item):
    """대화 항목 호버 후 ellipsis 버튼 클릭"""
    driver.execute_script("""
        arguments[0].dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));
        arguments[0].dispatchEvent(new MouseEvent('mouseenter', {bubbles: true}));
    """, chat_item)
    time.sleep(0.5)
    try:
        more_btn = chat_item.find_element(
            By.XPATH, ".//button[.//*[@data-testid='ellipsis-verticalIcon']]"
        )
    except Exception:
        more_btn = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//button[.//*[@data-testid='ellipsis-verticalIcon']]")
        ))
    driver.execute_script("arguments[0].click();", more_btn)
    time.sleep(0.5)