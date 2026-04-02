import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.chat_locators import ChatLocators


class ChatPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def hover_element(self, element):
        """JS 이벤트로 요소에 호버 효과 적용.
        headless Chrome에서 ActionChains.move_to_element()은 CSS :hover를
        트리거하지 않으므로 mouseover/mouseenter 이벤트를 직접 디스패치한다."""
        self.driver.execute_script("""
            arguments[0].dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));
            arguments[0].dispatchEvent(new MouseEvent('mouseenter', {bubbles: true}));
        """, element)

    def _find_file_input(self):
        """shadow DOM 포함 전체 DOM에서 input[type='file'] 탐색.
        일반 XPath는 shadow DOM 내부를 탐색하지 못하므로 JS로 직접 순회한다."""
        return self.driver.execute_script("""
            function findInput(root) {
                for (const el of root.querySelectorAll('input')) {
                    if (el.type === 'file') return el;
                }
                for (const el of root.querySelectorAll('*')) {
                    if (el.shadowRoot) {
                        const found = findInput(el.shadowRoot);
                        if (found) return found;
                    }
                }
                return null;
            }
            return findInput(document);
        """)

    def send_question(self, question):
        """질문 입력 및 전송"""
        input_box = self.wait.until(EC.element_to_be_clickable(ChatLocators.INPUT))
        input_box.send_keys(question)
        send_btn = self.wait.until(EC.element_to_be_clickable(ChatLocators.SEND_BTN))
        send_btn.click()

    def send_large_text(self, text):
        """대용량 텍스트를 JS로 textarea에 직접 주입 후 전송
        send_keys()는 글자 단위로 입력해 느리므로, React의 합성 이벤트를
        직접 발생시켜 상태를 업데이트한다. pyperclip 없이 headless에서도 동작."""
        input_box = self.wait.until(EC.element_to_be_clickable(ChatLocators.INPUT))
        self.driver.execute_script(
            """
            var setter = Object.getOwnPropertyDescriptor(
                window.HTMLTextAreaElement.prototype, 'value'
            ).set;
            setter.call(arguments[0], arguments[1]);
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            """,
            input_box, text
        )
        send_btn = self.wait.until(EC.element_to_be_clickable(ChatLocators.SEND_BTN))
        send_btn.click()

    def wait_for_answer(self, label, timeout=60):
        """
        답변 완료 대기
        1) stopIcon 나타났다가 사라지면 완료
        2) data-status='complete' div 확인
        """
        wait = WebDriverWait(self.driver, timeout)
        try:
            wait.until(EC.presence_of_element_located(ChatLocators.STOP_BTN))
            print(f"  ⏳ [{label}] 답변 생성 중...")
            wait.until(EC.invisibility_of_element_located(ChatLocators.STOP_BTN))
            print(f"  ✅ [{label}] 답변 생성 완료")
        except Exception:
            pass
        time.sleep(1)
        try:
            wait.until(EC.presence_of_element_located(ChatLocators.ANSWER))
        except Exception:
            pytest.fail(f"❌ [{label}] {timeout}초 내에 답변이 완료되지 않았습니다.")
        containers = self.driver.find_elements(*ChatLocators.ANSWER)
        assert len(containers) > 0 and len(containers[-1].text.strip()) > 0, \
            f"❌ [{label}] 답변이 비어있습니다."
        return containers[-1]

    def get_last_answer(self):
        """마지막 답변 컨테이너 반환"""
        containers = self.driver.find_elements(*ChatLocators.ANSWER)
        assert len(containers) > 0, "❌ 답변 요소를 찾을 수 없습니다."
        return containers[-1]

    def click_new_chat(self):
        """새 대화 버튼 클릭"""
        new_chat_btn = self.wait.until(EC.element_to_be_clickable(ChatLocators.NEW_CHAT_BTN))
        new_chat_btn.click()
        time.sleep(1)

    def get_sidebar_items(self, min_count=1):
        """사이드바 항목이 min_count 이상 로딩될 때까지 대기 후 반환"""
        try:
            self.wait.until(
                lambda d: len(d.find_elements(*ChatLocators.SIDEBAR_ITEMS)) >= min_count
            )
        except Exception:
            pass
        time.sleep(0.5)
        return self.driver.find_elements(*ChatLocators.SIDEBAR_ITEMS)

    def get_sidebar_titles(self):
        """사이드바 전체 대화 제목 목록 반환"""
        items = self.driver.find_elements(*ChatLocators.SIDEBAR_ITEMS)
        return [item.find_element(*ChatLocators.CHAT_TITLE).text.strip() for item in items]

    def click_more_menu(self, chat_item):
        """대화 항목 호버 후 ellipsis 버튼 클릭"""
        self.driver.execute_script("""
            arguments[0].dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));
            arguments[0].dispatchEvent(new MouseEvent('mouseenter', {bubbles: true}));
        """, chat_item)
        time.sleep(0.5)
        try:
            more_btn = chat_item.find_element(*ChatLocators.ELLIPSIS_BTN)
        except Exception:
            more_btn = self.wait.until(
                EC.presence_of_element_located(ChatLocators.ELLIPSIS_BTN_GLOBAL)
            )
        self.driver.execute_script("arguments[0].click();", more_btn)
        time.sleep(0.5)

    # ────────────────────────────────────────────────────────────
    # 예외 테스트용 메서드
    # ────────────────────────────────────────────────────────────

    def send_keys_only(self, text):
        """전송하지 않고 입력창에 텍스트만 입력"""
        input_box = self.wait.until(EC.element_to_be_clickable(ChatLocators.INPUT))
        input_box.clear()
        input_box.send_keys(text)

    def is_send_button_enabled(self):
        """전송 버튼 활성화 여부 확인"""
        try:
            btn = self.driver.find_element(*ChatLocators.SEND_BTN)
            return btn.is_enabled()
        except Exception:
            return False

    def click_send_button(self):
        """전송 버튼 클릭 (입력 없이 연속 클릭용)"""
        try:
            btn = self.driver.find_element(*ChatLocators.SEND_BTN)
            self.driver.execute_script("arguments[0].click();", btn)
        except Exception:
            pass

    def get_toast_message(self, timeout=5):
        """토스트 메시지 텍스트 반환"""
        try:
            toast = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(ChatLocators.TOAST)
            )
            return toast.text.strip()
        except Exception:
            return ""

    def wait_for_stop_button(self, timeout=15):
        """중단 버튼이 나타날 때까지 대기"""
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(ChatLocators.STOP_BTN)
        )

    def is_input_available(self):
        """입력창 활성화 여부 확인"""
        try:
            input_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(ChatLocators.INPUT)
            )
            return input_box.is_enabled()
        except Exception:
            return False

    def upload_file(self, file_path):
        """파일 업로드.

        - 텍스트 파일(.txt): 내용을 읽어 JS로 textarea에 직접 주입 후 전송.
          OS 네이티브 파일 다이얼로그를 완전히 우회하며 headless/CI에서도 동작.
        - 바이너리 파일(jpg/pdf/xlsx 등): + 버튼 → 파일 업로드 메뉴 클릭 후
          shadow DOM 포함 전체 DOM에서 file input을 탐색해 send_keys()로 경로 전달.
          (일반 XPath는 shadow DOM 내부를 탐색하지 못하므로 JS 탐색을 사용)
        """
        import mimetypes
        mime_type, _ = mimetypes.guess_type(file_path)
        is_text = (mime_type or "").startswith("text/")

        if is_text:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            message = f"아래 내용을 핵심 위주로 요약해주고, 불렛포인트(-)를 사용해줘:\n\n{content}"
            self.send_large_text(message)
            return

        import os
        abs_path = os.path.abspath(file_path)

        self.driver.execute_cdp_cmd(
            "Page.setInterceptFileChooserDialog", {"enabled": True}
        )
        try:
            plus_btn = self.wait.until(EC.element_to_be_clickable(ChatLocators.PLUS_BTN))
            plus_btn.click()
            time.sleep(1)

            upload_menu = self.wait.until(EC.element_to_be_clickable(ChatLocators.UPLOAD_MENU))
            upload_menu.click()
            time.sleep(1)

            file_input = self._find_file_input()
            if file_input:
                self.driver.execute_script(
                    "arguments[0].style.display='block'; arguments[0].style.visibility='visible';",
                    file_input
                )
                file_input.send_keys(abs_path)
            else:
                self.driver.execute_cdp_cmd(
                    "Page.handleFileChooser",
                    {"action": "accept", "files": [abs_path]}
                )
            time.sleep(2)
        finally:
            self.driver.execute_cdp_cmd(
                "Page.setInterceptFileChooserDialog", {"enabled": False}
            )

    def get_upload_error_text(self, timeout=5):
        """파일 업로드 에러 메시지 반환"""
        try:
            error = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(ChatLocators.UPLOAD_ERROR)
            )
            return error.text.strip()
        except Exception:
            return ""

    def is_char_limit_warning_visible(self, timeout=3):
        """글자 수 초과 경고 UI 표시 여부 확인"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(ChatLocators.CHAR_LIMIT)
            )
            return True
        except Exception:
            return False
