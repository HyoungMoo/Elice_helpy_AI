import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from src.pages.chat.chat_page import ChatPage, ANSWER_XPATH, SIDEBAR_ITEMS_XPATH


# ────────────────────────────────────────────────────────────────
# CHAT-02-002~006: 과거 대화 히스토리 통합 테스트
# 과거 대화 내용 조회 → 추가 질문 → 이름 변경 → 삭제 → 검색
# 순서대로 하나의 흐름으로 테스트
# ────────────────────────────────────────────────────────────────

# 사이드바 대화 제목을 가져오는 XPath
CHAT_TITLE_XPATH    = ".//p[contains(@class,'css-ff35j5')]"

# 검색 결과는 일반 사이드바와 다른 ul 구조로 렌더링되므로 별도 XPath 사용
SEARCH_RESULT_XPATH = "//ul[contains(@class,'css-1baokfq')]//a[contains(@href,'/ai-helpy-chat/chats/')]"
SEARCH_TITLE_XPATH  = ".//span[contains(@class,'MuiListItemText-primary')]"

# 검색 테스트에 사용할 키워드 (이 키워드가 포함된 대화가 사전에 존재해야 함)
TEST_KEYWORD  = "사과"

# 이름 변경 테스트에 사용할 새 이름
RENAME_TARGET = "새 대화방 이름 변경"


class TestChatHistory:

    def test_chat_history_full(self, logged_in_driver):
        """CHAT-02-002~006: 과거 대화 조회 → 추가 질문 → 이름 변경 → 삭제 → 검색"""
        driver = logged_in_driver
        wait = WebDriverWait(driver, 30)
        chat_page = ChatPage(driver)

        # ── CHAT-02-002: 과거 대화 내용 누락 없이 기록 확인 ──────────
        print("\n[CHAT-02-002] 과거 대화 내용 누락 확인")

        items = chat_page.get_sidebar_items(min_count=2)
        assert len(items) >= 2, "❌ [CHAT-02-002] 과거 대화가 없습니다. 사전에 대화를 생성해주세요."

        latest_chat = items[0]
        latest_chat_title = latest_chat.find_element(By.XPATH, CHAT_TITLE_XPATH).text.strip()
        latest_chat.click()
        time.sleep(1.5)
        print(f"  최신 대화 '{latest_chat_title}' 진입")

        answers = driver.find_elements(By.XPATH, ANSWER_XPATH)
        assert len(answers) > 0, \
            f"❌ [CHAT-02-002] 과거 대화 '{latest_chat_title}'에 대화 내용이 없습니다."
        print(f"  ✅ 과거 대화 내용 확인 완료 ({len(answers)}개 답변 존재)")

        # ── CHAT-02-003: 과거 대화에 추가 질문 ───────────────────────
        print("\n[CHAT-02-003] 과거 대화에 추가 질문")

        chat_page.send_question("저번에 무슨 대화를 나누었더라")
        chat_page.wait_for_answer("추가 질문")

        containers = driver.find_elements(By.XPATH, ANSWER_XPATH)
        assert len(containers[-1].text.strip()) > 0, \
            "❌ [CHAT-02-003] 추가 질문에 대한 답변이 없습니다."
        print("  ✅ 추가 질문 답변 확인 완료")

        # ── CHAT-02-004: 현재 대화방 이름 변경 ───────────────────────
        print("\n[CHAT-02-004] 대화 이름 변경 테스트")

        items = chat_page.get_sidebar_items(min_count=1)
        chat_page.click_more_menu(items[0])

        rename_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//li[@role='menuitem'][.//*[@data-testid='penIcon']]")
        ))
        driver.execute_script("arguments[0].click();", rename_btn)
        time.sleep(0.5)

        rename_input = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@name='name']")
        ))
        rename_input.send_keys(Keys.CONTROL + "a")
        rename_input.send_keys(Keys.DELETE)
        time.sleep(0.2)
        rename_input.send_keys(RENAME_TARGET)
        time.sleep(0.3)

        confirm_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., '확인') or contains(., '저장') or contains(., '변경')]")
        ))
        confirm_btn.click()
        time.sleep(1)

        titles = chat_page.get_sidebar_titles()
        assert any(RENAME_TARGET in t for t in titles), \
            f"❌ [CHAT-02-004] 이름 변경 실패 (현재 목록: {titles})"
        print(f"  ✅ 대화 이름 '{RENAME_TARGET}'으로 변경 확인 완료")

        # ── CHAT-02-005: 이름 변경한 대화 삭제 ───────────────────────
        print("\n[CHAT-02-005] 대화 삭제 테스트")

        items_before = chat_page.get_sidebar_items(min_count=1)
        target_item = None
        for item in items_before:
            title = item.find_element(By.XPATH, CHAT_TITLE_XPATH).text.strip()
            if RENAME_TARGET in title:
                target_item = item
                break

        assert target_item is not None, f"❌ [CHAT-02-005] '{RENAME_TARGET}' 대화를 찾을 수 없습니다."
        chat_page.click_more_menu(target_item)

        delete_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//li[@role='menuitem'][.//*[@data-testid='trashIcon']]")
        ))
        driver.execute_script("arguments[0].click();", delete_btn)
        time.sleep(0.5)

        confirm_delete = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), '삭제')]")
        ))
        confirm_delete.click()
        time.sleep(2)

        try:
            wait.until(lambda d: not any(
                RENAME_TARGET in item.find_element(By.XPATH, CHAT_TITLE_XPATH).text.strip()
                for item in d.find_elements(By.XPATH, SIDEBAR_ITEMS_XPATH)
            ))
        except Exception:
            pass
        time.sleep(1)

        titles_after = chat_page.get_sidebar_titles()
        assert not any(RENAME_TARGET in t for t in titles_after), \
            f"❌ [CHAT-02-005] 삭제된 대화 '{RENAME_TARGET}'이 여전히 사이드바에 있습니다."
        print(f"  ✅ 대화 삭제 확인 완료 ('{RENAME_TARGET}' 사이드바에서 제거됨)")

        # ── CHAT-02-006: 검색 기능 테스트 ────────────────────────────
        print("\n[CHAT-02-006] 검색 기능 테스트")

        search_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@role='button'][.//*[@data-testid='magnifying-glassIcon']]")
        ))
        search_btn.click()
        time.sleep(0.5)

        search_input = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@placeholder='Search']")
        ))
        search_input.send_keys(TEST_KEYWORD)
        time.sleep(1)

        result_items = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, SEARCH_RESULT_XPATH)
        ))
        assert len(result_items) > 0, f"❌ [CHAT-02-006] '{TEST_KEYWORD}' 검색 결과가 없습니다."

        result_titles = [item.find_element(By.XPATH, SEARCH_TITLE_XPATH).text.strip() for item in result_items]
        print(f"  검색 결과 목록: {result_titles}")

        assert all(TEST_KEYWORD in t for t in result_titles), \
            f"❌ [CHAT-02-006] 검색 결과에 '{TEST_KEYWORD}'와 무관한 대화가 포함되어 있습니다: {result_titles}"
        print(f"  ✅ 검색 결과 전체 키워드 확인 완료 ({len(result_items)}개)")

        first_result = result_items[0]
        first_result_title = result_titles[0]
        first_result.click()
        time.sleep(1.5)

        current_url = driver.current_url
        assert "/ai-helpy-chat/chats/" in current_url, \
            f"❌ [CHAT-02-006] 검색 결과 클릭 후 대화방으로 이동하지 않았습니다. (현재 URL: {current_url})"

        answers = driver.find_elements(By.XPATH, ANSWER_XPATH)
        assert len(answers) > 0, "❌ [CHAT-02-006] 접속한 대화방에 내용이 없습니다."
        print(f"  ✅ '{first_result_title}' 대화방 접속 확인 완료")

        print("\n🎉 과거 대화 히스토리 전체 테스트 통과!")