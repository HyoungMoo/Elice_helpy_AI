import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


# ────────────────────────────────────────────────────────────────
# 공통 XPath 상수
# ────────────────────────────────────────────────────────────────
STOP_BTN_XPATH      = "//button[.//*[@data-testid='stopIcon']]"
ANSWER_XPATH        = "//div[contains(@class,'elice-aichat__markdown') and @data-status='complete']"
SEND_BTN_XPATH      = "//button[.//*[@data-testid='arrow-upIcon']]"
NEW_CHAT_XPATH      = "//a[contains(@href,'/ai-helpy-chat') and .//span[text()='새 대화']]"
SIDEBAR_ITEMS_XPATH = "//ul[@data-testid='virtuoso-item-list']//a[@data-index]"
CHAT_TITLE_XPATH    = ".//p[contains(@class,'css-ff35j5')]"


class ChatPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def send_question(self, question):
        """질문 입력 및 전송"""
        input_box = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[name='input']"))
        )
        input_box.send_keys(question)
        send_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, SEND_BTN_XPATH))
        )
        send_btn.click()

    def wait_for_answer(self, label, timeout=60):
        """
        답변 완료 대기
        1) stopIcon 나타났다가 사라지면 완료
        2) data-status='complete' div 확인
        """
        wait = WebDriverWait(self.driver, timeout)
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
        containers = self.driver.find_elements(By.XPATH, ANSWER_XPATH)
        assert len(containers) > 0 and len(containers[-1].text.strip()) > 0, \
            f"❌ [{label}] 답변이 비어있습니다."
        return containers[-1]

    def get_last_answer(self):
        """마지막 답변 컨테이너 반환"""
        containers = self.driver.find_elements(By.XPATH, ANSWER_XPATH)
        assert len(containers) > 0, "❌ 답변 요소를 찾을 수 없습니다."
        return containers[-1]

    def click_new_chat(self):
        """새 대화 버튼 클릭"""
        new_chat_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, NEW_CHAT_XPATH))
        )
        new_chat_btn.click()
        time.sleep(1)

    def get_sidebar_items(self, min_count=1):
        """사이드바 항목이 min_count 이상 로딩될 때까지 대기 후 반환"""
        try:
            self.wait.until(
                lambda d: len(d.find_elements(By.XPATH, SIDEBAR_ITEMS_XPATH)) >= min_count
            )
        except Exception:
            pass
        time.sleep(0.5)
        return self.driver.find_elements(By.XPATH, SIDEBAR_ITEMS_XPATH)

    def get_sidebar_titles(self):
        """사이드바 전체 대화 제목 목록 반환"""
        items = self.driver.find_elements(By.XPATH, SIDEBAR_ITEMS_XPATH)
        return [item.find_element(By.XPATH, CHAT_TITLE_XPATH).text.strip() for item in items]

    def click_more_menu(self, chat_item):
        """대화 항목 호버 후 ellipsis 버튼 클릭"""
        self.driver.execute_script("""
            arguments[0].dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));
            arguments[0].dispatchEvent(new MouseEvent('mouseenter', {bubbles: true}));
        """, chat_item)
        time.sleep(0.5)
        try:
            more_btn = chat_item.find_element(
                By.XPATH, ".//button[.//*[@data-testid='ellipsis-verticalIcon']]"
            )
        except Exception:
            more_btn = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//button[.//*[@data-testid='ellipsis-verticalIcon']]")
            ))
        self.driver.execute_script("arguments[0].click();", more_btn)
        time.sleep(0.5)

    # ────────────────────────────────────────────────────────────
    # 예외 테스트용 메서드
    # ────────────────────────────────────────────────────────────

    def send_keys_only(self, text):
        """전송하지 않고 입력창에 텍스트만 입력"""
        input_box = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[name='input']"))
        )
        input_box.clear()
        input_box.send_keys(text)

    def is_send_button_enabled(self):
        """전송 버튼 활성화 여부 확인"""
        try:
            btn = self.driver.find_element(By.XPATH, SEND_BTN_XPATH)
            return btn.is_enabled()
        except Exception:
            return False

    def click_send_button(self):
        """전송 버튼 클릭 (입력 없이 연속 클릭용)"""
        try:
            btn = self.driver.find_element(By.XPATH, SEND_BTN_XPATH)
            self.driver.execute_script("arguments[0].click();", btn)
        except Exception:
            pass

    def get_toast_message(self, timeout=5):
        """토스트 메시지 텍스트 반환"""
        try:
            toast = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@role='alert'] | //div[contains(@class,'MuiAlert')]")
                )
            )
            return toast.text.strip()
        except Exception:
            return ""

    def wait_for_stop_button(self, timeout=15):
        """중단 버튼이 나타날 때까지 대기"""
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, STOP_BTN_XPATH))
        )

    def is_input_available(self):
        """입력창 활성화 여부 확인"""
        try:
            input_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[name='input']"))
            )
            return input_box.is_enabled()
        except Exception:
            return False

    def upload_file(self, file_path):
        """파일 업로드 — plusIcon 클릭 후 파일 경로 전달"""
        plus_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//*[@data-testid='plusIcon']]"))
        )
        plus_btn.click()
        time.sleep(1)

        upload_menu = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(@class,'MuiListItemText-primary') and contains(text(),'파일 업로드')]")
            )
        )
        upload_menu.click()
        time.sleep(1)

        # JS 로 input 요소 보이게 한 후 파일 경로 전달
        # OS 파일 탐색기를 Selenium 으로 제어할 수 없으므로 이 방식 사용
        file_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        self.driver.execute_script(
            "arguments[0].style.display = 'block'; arguments[0].style.visibility = 'visible';",
            file_input
        )
        file_input.send_keys(file_path)
        time.sleep(2)

        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(1)

    def get_upload_error_text(self, timeout=5):
        """파일 업로드 에러 메시지 반환"""
        try:
            error = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@role='alert'] | //p[contains(@class,'Mui-error')]")
                )
            )
            return error.text.strip()
        except Exception:
            return ""

    def is_char_limit_warning_visible(self, timeout=3):
        """글자 수 초과 경고 UI 표시 여부 확인"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//p[contains(@class,'Mui-error')] | //div[contains(text(),'글자')]")
                )
            )
            return True
        except Exception:
            return False