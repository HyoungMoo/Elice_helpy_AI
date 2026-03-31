import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from src.pages.chat.chat_page import ChatPage, ANSWER_XPATH

class TestQuestionEdit:

    def test_edited_question_regenerates_answer(self, logged_in_driver):
        """[CHAT-01-008] 질문 수정 시 기존 답변 제거 및 새 답변 생성 검증"""
        driver = logged_in_driver
        wait = WebDriverWait(driver, 20)
        actions = ActionChains(driver)
        chat_page = ChatPage(driver)

        # ── STEP 1. 초기 질문 전송 및 답변 확보 ───────────────────────
        print("\n[STEP 1] 초기 질문 전송")
        chat_page.send_question("사과 칼로리 알려줘")
        
        # 답변이 나올 때까지 대기 후, 사라질 대상(old_answer)을 미리 특정합니다.
        chat_page.wait_for_answer("사과")
        old_answer_element = wait.until(EC.presence_of_element_located((By.XPATH, ANSWER_XPATH)))
        print(f"  ✅ 초기 답변 확보 완료: {old_answer_element.text[:15]}...")

        # ── STEP 2. 질문 카드 호버 및 편집 모드 진입 ───────────────────
        print("[STEP 2] 질문 수정 버튼 클릭")
        
        # '사과'가 포함된 내 질문 카드를 찾아 마우스를 올립니다.
        my_question_card = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class,'MuiPaper-root')][.//span[contains(text(),'사과')]]")
        ))
        actions.move_to_element(my_question_card).perform()

        # 버튼이 '물리적으로 클릭 가능'할 때까지 기다린 후 JS로 확실하게 클릭
        edit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//*[@data-testid='penIcon']]")))
        driver.execute_script("arguments[0].click();", edit_btn)

        # ── STEP 3. 질문 내용 수정 및 재전송 ─────────────────────────
        print("[STEP 3] 질문 수정 및 보내기")
        
        edit_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//textarea")))
        edit_input.clear()
        edit_input.send_keys("포도 칼로리 알려줘")
        
        save_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class,'MuiButton-containedPrimary') and contains(.,'보내기')]")
        ))
        save_btn.click()

        # ── STEP 4.  소멸 확인 (Staleness Check) ────────────────
        print("[STEP 4] 기존 답변 소멸 검증")
        
        # 🔥 중요: '사과' 답변 요소가 화면에서 사라지거나 파괴될 때까지 대기 
        # 만약 수정 후에도 기존 답변이 남아있으면 여기서 타임아웃 에러가 발생합니다.
        wait.until(EC.staleness_of(old_answer_element))
        print("  ✅ 기존 답변이 정상적으로 제거되었습니다.")

        # ── STEP 5. 새 답변 생성 확인 ───────────────────────────────
        print("[STEP 5] 새 답변 생성 검증")
        
        # 포도 관련 답변이 올 때까지 대기
        chat_page.wait_for_answer("포도")
        
        new_answers = driver.find_elements(By.XPATH, ANSWER_XPATH)
        latest_answer_text = new_answers[-1].text
        
        assert "포도" in latest_answer_text, f"❌ 새 답변에 '포도' 내용이 없습니다: {latest_answer_text[:20]}"
        assert "사과" not in latest_answer_text, "❌ 새 답변에 이전 데이터(사과)가 섞여있습니다."
        
        print(f"  ✅ 새 답변 검증 완료: {latest_answer_text[:20]}...")
        print("\n🎉 질문 수정 테스트 성공!")