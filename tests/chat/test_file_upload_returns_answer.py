import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

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

    def _upload_file_and_ask(self, driver, chat_page, file_path, question, label):
        """
        파일 업로드 후 질문 전송 → 답변 완료 확인
        JPG/PDF/XLSX 모두 동일한 흐름으로 처리하기 위해 공통 메서드로 분리
        """
        wait = WebDriverWait(driver, 30)
        print(f"\n  [{label}] 파일 업로드 테스트 시작")

        # 테스트 파일이 실제로 존재하는지 먼저 확인
        assert os.path.exists(file_path), f"❌ [{label}] 테스트 파일이 없습니다: {file_path}"

        # ── 1. 파일 첨부 버튼(+) 클릭 ───────────────────────────────
        plus_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[.//*[@data-testid='plusIcon']]")
        ))
        plus_btn.click()
        time.sleep(1)

        # ── 2. "파일 업로드" 메뉴 클릭 ──────────────────────────────
        upload_menu = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(@class,'MuiListItemText-primary') and contains(text(),'파일 업로드')]")
        ))
        upload_menu.click()
        time.sleep(1)

        # ── 3. 파일 경로 직접 전달 ───────────────────────────────────
        # JS 로 input 요소를 화면에 보이게 만든 후 send_keys() 로 경로를 직접 전달
        # 파일 탐색기 없이 업로드 가능
        file_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@type='file']")
        ))
        driver.execute_script(
            "arguments[0].style.display = 'block'; arguments[0].style.visibility = 'visible';",
            file_input
        )
        file_input.send_keys(file_path)
        time.sleep(2)
        print(f"  ✅ [{label}] 파일 선택 완료")

        # ── 4. ESC 로 파일 업로드 창 닫기 ───────────────────────────
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(1)
        print(f"  ✅ [{label}] 파일 업로드 창 닫기 완료")

        # ── 5. 질문 입력 ─────────────────────────────────────────────
        input_box = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "textarea[name='input']")
        ))
        input_box.click()
        time.sleep(0.5)
        input_box.send_keys(question)
        time.sleep(1)

        # ── 6. 전송 버튼 클릭 ────────────────────────────────────────
        send_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[.//*[@data-testid='arrow-upIcon']]")
        ))
        send_btn.click()
        print(f"  ✅ [{label}] 질문 전송 완료: {question}")

        # ── 7. 답변 생성 완료 대기 ───────────────────────────────────
        # 파일 분석에 시간이 걸리므로 timeout 을 120초로 넉넉하게 설정
        print(f"  ⏳ [{label}] 답변 생성 대기 중...")
        answer = chat_page.wait_for_answer(label, timeout=120)
        print(f"  ✅ [{label}] 답변 확인 완료 (길이: {len(answer.text)}자)")
        print(f"  답변 미리보기: {answer.text[:100]}...")

        # 다음 테스트 파일 업로드 전 안정화 대기
        time.sleep(3)

    def test_jpg_file_upload_returns_image_description(self, logged_in_driver):
        """JPG 파일 업로드 시 이미지 내용을 인식하고 답변하는지 확인"""
        chat_page = ChatPage(logged_in_driver)
        f = TEST_FILES["jpg"]
        self._upload_file_and_ask(logged_in_driver, chat_page, f["path"], f["question"], f["label"])
        print("\n🎉 JPG 파일 업로드 테스트 통과!")

    def test_pdf_file_upload_returns_summary(self, logged_in_driver):
        """PDF 파일 업로드 시 내용을 요약해서 답변하는지 확인"""
        chat_page = ChatPage(logged_in_driver)
        f = TEST_FILES["pdf"]
        self._upload_file_and_ask(logged_in_driver, chat_page, f["path"], f["question"], f["label"])
        print("\n🎉 PDF 파일 업로드 테스트 통과!")

    def test_xlsx_file_upload_returns_data_analysis(self, logged_in_driver):
        """XLSX 파일 업로드 시 데이터를 분석해서 답변하는지 확인"""
        chat_page = ChatPage(logged_in_driver)
        f = TEST_FILES["xlsx"]
        self._upload_file_and_ask(logged_in_driver, chat_page, f["path"], f["question"], f["label"])
        print("\n🎉 XLSX 파일 업로드 테스트 통과!")