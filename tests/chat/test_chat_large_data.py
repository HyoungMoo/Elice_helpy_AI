import os
from selenium.webdriver.common.by import By

from src.pages.chat.chat_page import ChatPage


# ────────────────────────────────────────────────────────────────
# CHAT-01-002: 대량 데이터 처리 테스트
# large_text.txt 파일 내용을 JS로 textarea에 직접 주입해 AI가 요약하는지 확인
# OS 네이티브 다이얼로그를 우회 — headless/CI 환경에서도 동작
# ────────────────────────────────────────────────────────────────
class TestChatLargeData:

    def test_summary_contains_required_sections_and_keywords(self, logged_in_driver):
        """대용량 텍스트 파일 내용 전송 후 요약 시 필수 섹션과 키워드가 포함되는지 확인"""
        driver = logged_in_driver
        chat_page = ChatPage(driver)

        # ── 1. 텍스트 파일 경로 확인 ─────────────────────────────────
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        file_path = os.path.join(project_root, "src", "resources", "test_files", "large_text.txt")

        assert os.path.exists(file_path), f"❌ 테스트 파일이 없습니다: {file_path}"
        print(f"\n  ✅ 파일 확인 완료: {file_path}")

        # ── 2. 파일 내용을 JS로 주입 후 전송 ────────────────────────
        chat_page.upload_file(file_path)
        print("  ✅ 질문 전송 완료. 요약 응답 대기 중...")

        # ── 3. 답변 완료 대기 ─────────────────────────────────────────
        chat_box = chat_page.wait_for_answer("대용량 요약", timeout=120)

        # ── 4. 답변에서 불렛포인트(li 태그) 텍스트 추출 ──────────────
        all_li_elements = chat_box.find_elements(By.TAG_NAME, "li")
        summary_items = [li.text.strip() for li in all_li_elements if li.text.strip()]
        full_text = " ".join(summary_items)

        # li 태그가 없으면 전체 텍스트로 검증
        if not full_text:
            full_text = chat_box.text.strip()

        print("\n  --- AI 요약 품질 확인 시작 ---")

        # ── 5. 요약 품질 검증 ─────────────────────────────────────────

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
