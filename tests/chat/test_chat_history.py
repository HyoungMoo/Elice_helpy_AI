import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from src.pages.chat.chat_page import ChatPage, ANSWER_XPATH, SIDEBAR_ITEMS_XPATH

# ── 공통 설정 및 XPath ──────────────────────────────────────────
# 사이드바 대화 제목 (더 구체적인 클래스 포함 버전 사용)
CHAT_TITLE_XPATH = ".//p[contains(@class,'css-ff35j5')]"

# 검색 결과 관련 XPath
SEARCH_RESULT_XPATH = "//ul[contains(@class,'css-1baokfq')]//a[contains(@href,'/ai-helpy-chat/chats/')]"
SEARCH_TITLE_XPATH  = ".//span[contains(@class,'MuiListItemText-primary')]"

# 테스트 데이터
QUESTIONS = ["사과 칼로리", "바나나 칼로리", "포도 칼로리", "딸기 칼로리", "수박 칼로리"]
TEST_KEYWORD = "사과"
RENAME_TARGET = "새 대화방 이름 변경"

class TestChatHistoryManagement:

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_driver):
        self.driver = logged_in_driver
        self.wait = WebDriverWait(self.driver, 30)
        self.chat_page = ChatPage(self.driver)

    def test_01_sidebar_order_and_creation(self):
        """[CHAT-02-001] 대화 생성 및 사이드바 최신순 정렬 검증"""
        print("\n[단계 1] 대화 생성 및 순서 확인 시작")
        created_titles = []

        for i, q in enumerate(QUESTIONS):
            self.chat_page.click_new_chat()
            self.chat_page.send_question(q)
            self.chat_page.wait_for_answer(f"대화 {i+1}")
            
            # 최신 항목 제목 기록
            items = self.chat_page.get_sidebar_items(min_count=1)
            title = items[0].find_element(By.XPATH, CHAT_TITLE_XPATH).text.strip()
            created_titles.append(title)
            print(f"  ✅ 생성됨: {title}")

        # 순서 검증 (data-index 기반)
        items = self.chat_page.get_sidebar_items(min_count=5)
        indices = [int(item.get_attribute("data-index")) for item in items]
        assert indices == sorted(indices), f"❌ 사이드바 순서 깨짐: {indices}"
        
        # 최신 대화가 맨 위인지 검증
        latest_title = items[0].find_element(By.XPATH, CHAT_TITLE_XPATH).text.strip()
        assert created_titles[-1] in latest_title, "❌ 최신 대화가 상단에 없음"
        print("  ✅ 사이드바 순서 및 최신성 검증 완료")

    def test_02_history_search_edit_delete(self):
        """[CHAT-02-002~006] 대화 조회, 추가 질문, 이름 변경, 삭제, 검색 통합 검증"""
        print("\n[단계 2] 히스토리 관리 기능(CRUD) 검증 시작")
        
        # 1. 과거 대화 내용 조회 (위에서 만든 목록 활용)
        items = self.chat_page.get_sidebar_items(min_count=2)
        items[0].click() # 최신 대화 진입
        time.sleep(1.5)
        
        answers = self.driver.find_elements(By.XPATH, ANSWER_XPATH)
        assert len(answers) > 0, "❌ 과거 대화 내용이 보이지 않습니다."
        print(f"  ✅ 과거 대화 조회 완료 ({len(answers)}개 답변)")

        # 2. 이름 변경
        self.chat_page.click_more_menu(items[0])
        rename_btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//li[@role='menuitem'][.//*[@data-testid='penIcon']]")
        ))
        self.driver.execute_script("arguments[0].click();", rename_btn)
        
        rename_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='name']")))
        rename_input.send_keys(Keys.CONTROL + "a", Keys.DELETE)
        rename_input.send_keys(RENAME_TARGET)
        
        confirm_btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., '확인') or contains(., '저장')]")
        ))
        confirm_btn.click()
        time.sleep(1.5)
        
        assert any(RENAME_TARGET in t for t in self.chat_page.get_sidebar_titles()), "❌ 이름 변경 실패"
        print(f"  ✅ 이름 변경 완료: {RENAME_TARGET}")

        # 3. 검색 기능
        search_btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@role='button'][.//*[@data-testid='magnifying-glassIcon']]")
        ))
        search_btn.click()
        
        search_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
        search_input.send_keys(TEST_KEYWORD)
        time.sleep(1.5)
        
        result_items = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, SEARCH_RESULT_XPATH)))
        result_titles = [item.find_element(By.XPATH, SEARCH_TITLE_XPATH).text.strip() for item in result_items]
        assert all(TEST_KEYWORD in t for t in result_titles), "❌ 검색 결과 키워드 불일치"
        print(f"  ✅ 검색 기능 검증 완료 (결과: {len(result_items)}개)")

        # 4. 삭제 기능 (검색창 닫고 삭제 진행)
        self.driver.refresh() # 검색 모드 해제를 위해 새로고침
        time.sleep(2)
        
        items = self.chat_page.get_sidebar_items()
        target_item = next((i for i in items if RENAME_TARGET in i.text), None)
        assert target_item is not None, f"❌ 삭제할 대상({RENAME_TARGET})을 사이드바에서 찾을 수 없습니다."
        self.chat_page.click_more_menu(target_item)
        
        delete_btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//li[@role='menuitem'][.//*[@data-testid='trashIcon']]")
        ))
        self.driver.execute_script("arguments[0].click();", delete_btn)
        
        confirm_delete = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '삭제')]")))
        confirm_delete.click()
        time.sleep(2)
        
        assert not any(RENAME_TARGET in t for t in self.chat_page.get_sidebar_titles()), "❌ 삭제 후에도 목록에 남음"
        print(f"  ✅ 대화 삭제 검증 완료")

        print("\n🎉 모든 히스토리 관리 테스트 통과!")