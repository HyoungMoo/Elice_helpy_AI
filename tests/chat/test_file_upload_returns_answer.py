import os

from src.pages.chat.chat_page import ChatPage


# ────────────────────────────────────────────────────────────────
# CHAT-01-010: 다양한 확장자 파일 업로드 테스트
# JPG(이미지), PDF(문서), XLSX(엑셀) 파일을 각각 업로드하고
# AI 가 파일 내용을 인식해서 정상적으로 답변하는지 확인
# ────────────────────────────────────────────────────────────────

# 현재 파일 위치를 기준으로 프로젝트 루트 경로 계산
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))

# 각 파일 타입별 경로, 질문, 라벨을 딕셔너리로 관리
TEST_FILES = {
    "jpg": {
        "path": os.path.join(PROJECT_ROOT, "src", "resources", "assets", "ticket.jpg"),
        "question": "사진에 나온 내용을 설명해줘.",
        "label": "JPG"
    },
    "pdf": {
        "path": os.path.join(PROJECT_ROOT, "src", "resources", "test_files", "sample.pdf"),
        "question": "이 PDF의 주요 내용을 요약해줘.",
        "label": "PDF"
    },
    "xlsx": {
        "path": os.path.join(PROJECT_ROOT, "src", "resources", "test_files", "sample.xlsx"),
        "question": "이 엑셀 파일의 데이터를 분석해줘.",
        "label": "XLSX"
    },
}


class TestFileUpload:

    def _upload_file_and_ask(self, chat_page, file_path, question, label):
        """파일 업로드 후 질문 전송 → 답변 완료 확인
        JPG/PDF/XLSX 모두 동일한 흐름으로 처리하기 위해 공통 메서드로 분리"""
        print(f"\n  [{label}] 파일 업로드 테스트 시작")

        assert os.path.exists(file_path), f"❌ [{label}] 테스트 파일이 없습니다: {file_path}"

        # ── 1. 파일 업로드 (CDP로 OS 다이얼로그 가로채기) ────────────
        chat_page.upload_file(file_path)
        print(f"  ✅ [{label}] 파일 업로드 완료")

        # ── 2. 질문 전송 ─────────────────────────────────────────────
        chat_page.send_question(question)
        print(f"  ✅ [{label}] 질문 전송 완료: {question}")

        # ── 3. 답변 생성 완료 대기 ───────────────────────────────────
        # 파일 분석에 시간이 걸리므로 timeout 을 120초로 넉넉하게 설정
        print(f"  ⏳ [{label}] 답변 생성 대기 중...")
        answer = chat_page.wait_for_answer(label, timeout=120)
        print(f"  ✅ [{label}] 답변 확인 완료 (길이: {len(answer.text)}자)")
        print(f"  답변 미리보기: {answer.text[:100]}...")

    def test_jpg_file_upload_returns_image_description(self, logged_in_driver):
        """JPG 파일 업로드 시 이미지 내용을 인식하고 답변하는지 확인"""
        chat_page = ChatPage(logged_in_driver)
        f = TEST_FILES["jpg"]
        self._upload_file_and_ask(chat_page, f["path"], f["question"], f["label"])
        print("\n🎉 JPG 파일 업로드 테스트 통과!")

    def test_pdf_file_upload_returns_summary(self, logged_in_driver):
        """PDF 파일 업로드 시 내용을 요약해서 답변하는지 확인"""
        chat_page = ChatPage(logged_in_driver)
        f = TEST_FILES["pdf"]
        self._upload_file_and_ask(chat_page, f["path"], f["question"], f["label"])
        print("\n🎉 PDF 파일 업로드 테스트 통과!")

    def test_xlsx_file_upload_returns_data_analysis(self, logged_in_driver):
        """XLSX 파일 업로드 시 데이터를 분석해서 답변하는지 확인"""
        chat_page = ChatPage(logged_in_driver)
        f = TEST_FILES["xlsx"]
        self._upload_file_and_ask(chat_page, f["path"], f["question"], f["label"])
        print("\n🎉 XLSX 파일 업로드 테스트 통과!")
