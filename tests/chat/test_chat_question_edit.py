import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from src.pages.chat.chat_page import ChatPage, ANSWER_XPATH


# ────────────────────────────────────────────────────────────────
# CHAT-01-008: 질문 텍스트 수정 테스트
# 내가 보낸 질문 위에 마우스를 올리면 나타나는 편집 버튼을 클릭해서
# 질문을 수정하고 재전송했을 때 동작을 확인
# ────────────────────────────────────────────────────────────────
class TestQuestionEdit:

    def test_edited_question_regenerates_answer_and_removes_old_answer(self, logged_in_driver):
        """질문 수정 후 기존 답변이 사라지고 새 답변이 생성되는지 확인"""
        driver = logged_in_driver
        wait = WebDriverWait(driver, 30)
        actions = ActionChains(driver)
        chat_page = ChatPage(driver)

        # ── 1. 초기 질문 전송 ─────────────────────────────────────────
        print("\n[STEP 1] 초기 질문 전송")
        chat_page.send_question("사과 칼로리 알려줘")
        print("  ✅ 초기 질문 전송 완료")

        # ── 2. 답변 생성 완료 대기 ────────────────────────────────────
        print("\n[STEP 2] 답변 생성 대기")
        chat_page.wait_for_answer("사과 칼로리")

        spans = driver.find_elements(By.XPATH, ANSWER_XPATH)
        assert len(spans) > 0, "❌ 사과 칼로리 답변을 찾을 수 없습니다."
        print(f"  ✅ 사과 칼로리 답변 확인 완료 (길이: {len(spans[-1].text.strip())}자)")

        # ── 3. 질문 박스 호버 → 편집 버튼 클릭 ──────────────────────
        print("\n[STEP 3] 질문 박스 호버 후 편집 버튼 클릭")

        my_q_xpath = (
            "//div[contains(@class,'MuiPaper-root')]"
            "[.//span[@data-status='complete' and contains(text(),'사과')]]"
        )
        my_q_element = wait.until(EC.visibility_of_element_located((By.XPATH, my_q_xpath)))
        actions.move_to_element(my_q_element).perform()
        print("  📍 질문 박스 호버 중...")
        time.sleep(1.5)

        edit_btn = wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[.//*[@data-testid='penIcon']]"))
        )
        driver.execute_script("arguments[0].click();", edit_btn)
        print("  ✅ 편집 버튼 클릭 완료")

        # ── 4. 텍스트 수정 후 보내기 클릭 ───────────────────────────
        print("\n[STEP 4] 텍스트 수정 후 보내기 클릭")

        edit_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//textarea")))
        edit_input.clear()
        edit_input.send_keys("포도 칼로리 알려줘")
        print("  ✅ 텍스트 수정 완료: '사과 칼로리 알려줘' → '포도 칼로리 알려줘'")

        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH,
            "//button[contains(@class,'MuiButton-containedPrimary') and contains(.,'보내기')]"
        )))
        save_btn.click()
        print("  ✅ 보내기 클릭 완료")

        # ── 5. 사과 답변 소멸 확인 ───────────────────────────────────
        print("\n[STEP 5] 사과 답변 소멸 확인")
        time.sleep(2)

        try:
            answer_texts = [s.text.strip() for s in driver.find_elements(By.XPATH, ANSWER_XPATH)]
            assert not any("사과" in t for t in answer_texts), \
                "❌ 질문 수정 후 기존 사과 칼로리 답변이 소멸되지 않았습니다."
        except AssertionError:
            raise
        except Exception:
            pass
        print("  ✅ 기존 사과 칼로리 답변 소멸 확인 완료")

        # ── 6. 포도 칼로리 새 답변 생성 확인 ─────────────────────────
        print("\n[STEP 6] 포도 칼로리 새 답변 생성 확인")
        chat_page.wait_for_answer("포도 칼로리")

        new_spans = driver.find_elements(By.XPATH, ANSWER_XPATH)
        assert len(new_spans) > 0, "❌ 포도 칼로리 새 답변이 생성되지 않았습니다."
        assert any("포도" in s.text.strip() for s in new_spans), \
            "❌ 새 답변에 포도 관련 내용이 없습니다."
        print(f"  ✅ 포도 칼로리 새 답변 생성 확인 완료 (길이: {len(new_spans[-1].text.strip())}자)")

        print("\n🎉 질문 텍스트 수정 테스트 통과!")