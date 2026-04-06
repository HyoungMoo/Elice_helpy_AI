import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.pages.chat.chat_page import ChatPage


# ────────────────────────────────────────────────────────────────
# CHAT 입력 예외 케이스 테스트
# ────────────────────────────────────────────────────────────────


class TestEmptyInput:
    """CHAT-EX-001: 빈 메시지 전송 관련"""

    @allure.epic("채팅")
    @allure.feature("입력 검증")
    @allure.story("빈 입력")
    @allure.title("빈 입력창에서 전송 버튼 비활성화 확인")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_send_button_disabled_when_empty(self, logged_in_driver):
        """입력창이 비어있을 때 전송 버튼이 비활성화 상태인지 확인"""
        chat_page = ChatPage(logged_in_driver)

        assert not chat_page.is_send_button_enabled(), \
            "❌ 빈 입력창에서 전송 버튼이 활성화되어 있습니다."
        print("✅ 빈 입력창 → 전송 버튼 비활성화 확인")

    @allure.epic("채팅")
    @allure.feature("입력 검증")
    @allure.story("빈 입력")
    @allure.title("텍스트 입력 후 전송 버튼 활성화 확인")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_send_button_enabled_after_input(self, logged_in_driver):
        """텍스트 입력 후 전송 버튼이 활성화되는지 확인"""
        chat_page = ChatPage(logged_in_driver)

        chat_page.send_keys_only("안녕하세요")
        assert chat_page.is_send_button_enabled(), \
            "❌ 텍스트 입력 후에도 전송 버튼이 비활성화 상태입니다."
        print("✅ 텍스트 입력 후 → 전송 버튼 활성화 확인")

    @allure.epic("채팅")
    @allure.feature("입력 검증")
    @allure.story("빈 입력")
    @allure.title("입력 내용 삭제 후 전송 버튼 비활성화 확인")
    @allure.severity(allure.severity_level.NORMAL)
    def test_send_button_disabled_after_clearing_input(self, logged_in_driver):
        """입력 후 내용을 지우면 전송 버튼이 다시 비활성화되는지 확인"""
        driver = logged_in_driver
        chat_page = ChatPage(driver)
        wait = WebDriverWait(driver, 10)

        chat_page.send_keys_only("안녕하세요")
        assert chat_page.is_send_button_enabled(), "❌ 입력 후 버튼 활성화 실패"

        input_box = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[name='input']"))
        )
        driver.execute_script(
            """
            var setter = Object.getOwnPropertyDescriptor(
                window.HTMLTextAreaElement.prototype, 'value'
            ).set;
            setter.call(arguments[0], '');
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            """,
            input_box
        )
        time.sleep(0.5)

        assert not chat_page.is_send_button_enabled(), \
            "❌ 입력 내용 삭제 후에도 전송 버튼이 활성화되어 있습니다."
        print("✅ 입력 삭제 후 → 전송 버튼 비활성화 확인")

    @allure.epic("채팅")
    @allure.feature("입력 검증")
    @allure.story("빈 입력")
    @allure.title("공백만 입력 시 전송 버튼 비활성화 확인")
    @allure.severity(allure.severity_level.NORMAL)
    def test_whitespace_only_input_disabled_send(self, logged_in_driver):
        """공백만 입력했을 때 전송 버튼이 비활성화 상태인지 확인"""
        driver = logged_in_driver
        chat_page = ChatPage(driver)
        wait = WebDriverWait(driver, 10)

        input_box = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[name='input']"))
        )
        driver.execute_script(
            """
            var setter = Object.getOwnPropertyDescriptor(
                window.HTMLTextAreaElement.prototype, 'value'
            ).set;
            setter.call(arguments[0], '   ');
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            """,
            input_box
        )
        time.sleep(0.5)

        assert not chat_page.is_send_button_enabled(), \
            "❌ 공백만 입력했는데 전송 버튼이 활성화되어 있습니다."
        print("✅ 공백만 입력 → 전송 버튼 비활성화 확인")

    @allure.epic("채팅")
    @allure.feature("입력 검증")
    @allure.story("빈 입력")
    @allure.title("줄바꿈만 입력 시 전송 버튼 비활성화 확인")
    @allure.severity(allure.severity_level.NORMAL)
    def test_newline_only_input_disabled_send(self, logged_in_driver):
        """줄바꿈만 있는 입력 시 전송 버튼이 비활성화 상태인지 확인"""
        driver = logged_in_driver
        chat_page = ChatPage(driver)
        wait = WebDriverWait(driver, 10)

        input_box = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[name='input']"))
        )
        driver.execute_script(
            """
            var setter = Object.getOwnPropertyDescriptor(
                window.HTMLTextAreaElement.prototype, 'value'
            ).set;
            setter.call(arguments[0], '\\n\\n');
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            """,
            input_box
        )
        time.sleep(0.5)

        assert not chat_page.is_send_button_enabled(), \
            "❌ 줄바꿈만 입력했는데 전송 버튼이 활성화되어 있습니다."
        print("✅ 줄바꿈만 입력 → 전송 버튼 비활성화 확인")

    @allure.epic("채팅")
    @allure.feature("입력 검증")
    @allure.story("빈 입력")
    @allure.title("질문 전송 후 입력창 자동 초기화 확인")
    @allure.severity(allure.severity_level.NORMAL)
    def test_input_cleared_after_send(self, logged_in_driver):
        """질문 전송 후 입력창이 자동으로 비워지는지 확인"""
        driver = logged_in_driver
        chat_page = ChatPage(driver)
        wait = WebDriverWait(driver, 10)

        chat_page.send_question("안녕")

        input_box = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='input']"))
        )
        assert input_box.get_attribute("value") == "", \
            "❌ 전송 후 입력창이 초기화되지 않았습니다."
        print("✅ 전송 후 입력창 초기화 확인")


class TestSpecialInput:
    """CHAT-EX-002: 특수 입력 케이스"""

    @allure.epic("채팅")
    @allure.feature("입력 검증")
    @allure.story("특수 입력")
    @allure.title("특수문자 포함 질문 정상 전송 확인")
    @allure.severity(allure.severity_level.NORMAL)
    def test_special_characters_send_successfully(self, logged_in_driver):
        """특수문자 포함 질문이 정상 전송되는지 확인"""
        chat_page = ChatPage(logged_in_driver)

        chat_page.send_question("!@#$%^&*() 이 특수문자들의 의미를 설명해줘")
        answer = chat_page.wait_for_answer("특수문자")

        assert len(answer.text.strip()) > 0, "❌ 특수문자 질문에 대한 답변이 없습니다."
        print(f"✅ 특수문자 입력 → 정상 답변 확인 (길이: {len(answer.text)}자)")

    @allure.epic("채팅")
    @allure.feature("입력 검증")
    @allure.story("특수 입력")
    @allure.title("이모지 포함 질문 정상 전송 확인")
    @allure.severity(allure.severity_level.NORMAL)
    def test_emoji_input_send_successfully(self, logged_in_driver):
        """이모지 포함 질문이 정상 전송되는지 확인"""
        chat_page = ChatPage(logged_in_driver)

        
        chat_page.send_large_text("🍎 이 이모지가 뭔지 설명해줘")
        answer = chat_page.wait_for_answer("이모지")

        assert len(answer.text.strip()) > 0, "❌ 이모지 질문에 대한 답변이 없습니다."
        print(f"✅ 이모지 입력 → 정상 답변 확인 (길이: {len(answer.text)}자)")

    @allure.epic("채팅")
    @allure.feature("입력 검증")
    @allure.story("특수 입력")
    @allure.title("한 글자 질문 정상 전송 및 답변 확인")
    @allure.severity(allure.severity_level.MINOR)
    def test_single_character_input_send_successfully(self, logged_in_driver):
        """한 글자 질문이 정상 전송되고 답변이 오는지 확인"""
        chat_page = ChatPage(logged_in_driver)

        chat_page.send_question("안")
        answer = chat_page.wait_for_answer("한글자")

        assert len(answer.text.strip()) > 0, "❌ 한 글자 질문에 대한 답변이 없습니다."
        print(f"✅ 한 글자 입력 → 정상 답변 확인 (길이: {len(answer.text)}자)")


class TestKeyboardInput:
    """CHAT-EX-003: 키보드 입력 방식 케이스"""

    @allure.epic("채팅")
    @allure.feature("입력 검증")
    @allure.story("키보드 입력")
    @allure.title("Enter 키 입력 시 메시지 전송 확인")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_enter_key_sends_message(self, logged_in_driver):
        """Enter 키 입력 시 메시지가 전송되는지 확인"""
        driver = logged_in_driver
        chat_page = ChatPage(driver)
        wait = WebDriverWait(driver, 10)

        input_box = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[name='input']"))
        )
        input_box.send_keys("안녕하세요")
        input_box.send_keys(Keys.ENTER)

        # 전송되면 Stop 버튼이 나타남
        chat_page.wait_for_stop_button()
        print("✅ Enter 키 → 메시지 전송 확인")

    @allure.epic("채팅")
    @allure.feature("입력 검증")
    @allure.story("키보드 입력")
    @allure.title("Shift+Enter 입력 시 줄바꿈 추가 및 전송 안 됨 확인")
    @allure.severity(allure.severity_level.NORMAL)
    def test_shift_enter_adds_newline_not_send(self, logged_in_driver):
        """Shift+Enter 입력 시 전송되지 않고 줄바꿈이 추가되는지 확인"""
        driver = logged_in_driver
        chat_page = ChatPage(driver)
        wait = WebDriverWait(driver, 10)

        input_box = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[name='input']"))
        )
        input_box.send_keys("첫 번째 줄")
        input_box.send_keys(Keys.SHIFT + Keys.ENTER)
        input_box.send_keys("두 번째 줄")

        value = input_box.get_attribute("value")
        assert "\n" in value, "❌ Shift+Enter가 줄바꿈을 추가하지 않았습니다."
        assert chat_page.is_send_button_enabled(), \
            "❌ Shift+Enter 입력 후 전송 버튼이 비활성화되었습니다."
        print("✅ Shift+Enter → 줄바꿈 추가, 전송 안 됨 확인")
