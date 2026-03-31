import pytest
import time
import os
import pyperclip
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from src.pages.chat.chat_page import ChatPage


# ────────────────────────────────────────────────────────────────
# CHAT-01-002: 대량 데이터 처리 테스트
# 외부 텍스트 파일을 클립보드로 붙여넣기해서 전송했을 때
# AI 가 내용을 제대로 요약하는지 확인
# ────────────────────────────────────────────────────────────────
class TestChatLargeData:

    def test_summary_contains_required_sections_and_keywords(self, logged_in_driver):
        """대용량 텍스트 요약 시 필수 섹션과 키워드가 포함되는지 확인"""
        driver = logged_in_driver
        wait = WebDriverWait(driver, 15)
        chat_page = ChatPage(driver)

        # ── 1. 텍스트 파일 읽기 ───────────────────────────────────────
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        file_path = os.path.join(project_root, "src", "resources", "test_files", "large_text.txt")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        integrated_text = f"아래 내용을 핵심 위주로 요약해주고, 불렛포인트(-)를 사용해줘:\n\n{content}"

        # ── 2. 클립보드에 텍스트 복사 ────────────────────────────────
        pyperclip.copy(integrated_text)
        print(f"\n  ✅ 클립보드 복사 완료 (길이: {len(integrated_text)}자)")

        # ── 3. 입력창 클릭해서 포커스 맞추기 ─────────────────────────
        input_box = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[name='input']"))
        )
        input_box.click()
        time.sleep(1)

        # ── 4. Ctrl+V 로 붙여넣기 ────────────────────────────────────
        print("  📍 붙여넣기(Ctrl+V) 실행 중...")
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        time.sleep(5)

        # ── 5. 전송 버튼 클릭 ─────────────────────────────────────────
        send_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//*[@data-testid='arrow-upIcon']]"))
        )
        send_btn.click()
        print("  ✅ 데이터 전송 완료. 요약 응답 대기 중...")

        # ── 6. 답변 완료 대기 ─────────────────────────────────────────
        chat_box = chat_page.wait_for_answer("대용량 요약", timeout=120)

        # ── 7. 답변에서 불렛포인트(li 태그) 텍스트 추출 ──────────────
        all_li_elements = chat_box.find_elements(By.TAG_NAME, "li")
        summary_items = [li.text.strip() for li in all_li_elements if li.text.strip()]
        full_text = " ".join(summary_items)

        print("\n  --- AI 요약 품질 확인 시작 ---")

        # ── 8. 요약 품질 검증 ─────────────────────────────────────────

        # [검증 1] 섹션 커버리지
        required_sections = ["경제", "6G", "바이오", "공간 컴퓨팅"]
        section_count = sum(1 for section in required_sections if section in full_text)
        print(f"  섹션 커버리지: {section_count}/4")
        assert section_count >= 2, \
            f"❌ 필수 섹션이 부족합니다. ({section_count}/4개 포함)"

        # [검증 2] 핵심 키워드 포함 여부
        essential_keywords = ["금리", "Fed", "표준화", "위성", "유전자", "윤리", "비전 프로", "생산성", "인플레이션", "6G"]
        found_keywords = [k for k in essential_keywords if k in full_text]
        print(f"  키워드 매칭: {len(found_keywords)}/10")
        assert len(found_keywords) >= 5, \
            f"❌ 핵심 키워드가 부족합니다. ({len(found_keywords)}/10개 발견)"

        print("  ✅ 요약 품질 확인 완료")
        print("🎉 대량 데이터 처리 테스트 통과!")