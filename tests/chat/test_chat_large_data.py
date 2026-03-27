import pytest
import time
import os
import pyperclip
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from helpers import ANSWER_XPATH, wait_for_answer


# ────────────────────────────────────────────────────────────────
# CHAT-01-002: 대량 데이터 처리 테스트
# 외부 텍스트 파일을 클립보드로 붙여넣기해서 전송했을 때
# AI 가 내용을 제대로 요약하는지 확인
# ────────────────────────────────────────────────────────────────
def test_chat_large_data_with_summary_check(logged_in_driver):
    driver = logged_in_driver
    # 최대 15초 동안 요소를 찾을 때까지 대기하는 설정
    wait = WebDriverWait(driver, 15)

    # ── 1. 텍스트 파일 읽기 ───────────────────────────────────────
    # 현재 파일 위치를 기준으로 프로젝트 루트 경로를 계산
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    file_path = os.path.join(project_root, "src", "resources", "test_files", "large_text.txt")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 요약 지시문과 파일 내용을 합쳐서 하나의 질문 텍스트 생성
    integrated_text = f"아래 내용을 핵심 위주로 요약해주고, 불렛포인트(-)를 사용해줘:\n\n{content}"

    # ── 2. 클립보드에 텍스트 복사 ────────────────────────────────
    # 텍스트가 너무 길어서 직접 send_keys() 로 입력하면 느리거나 오류 발생
    # 클립보드에 복사 후 Ctrl+V 로 붙여넣는 방식 사용
    pyperclip.copy(integrated_text)
    print(f"\n  ✅ 클립보드 복사 완료 (길이: {len(integrated_text)}자)")

    # ── 3. 입력창 클릭해서 포커스 맞추기 ─────────────────────────
    input_box = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[name='input']"))
    )
    input_box.click()
    time.sleep(1)  # 포커스 안정화 대기

    # ── 4. Ctrl+V 로 붙여넣기 ────────────────────────────────────
    # ActionChains 로 키보드 단축키 실행
    print("  📍 붙여넣기(Ctrl+V) 실행 중...")
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(5)  # 대용량 텍스트가 입력창에 완전히 붙여넣어질 때까지 대기

    # ── 5. 전송 버튼 클릭 ─────────────────────────────────────────
    send_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//*[@data-testid='arrow-upIcon']]"))
    )
    send_btn.click()
    print("  ✅ 데이터 전송 완료. 요약 응답 대기 중...")

    # ── 6. 답변 완료 대기 ─────────────────────────────────────────
    # 대용량 텍스트라 요약에 시간이 걸리므로 timeout 을 120초로 넉넉하게 설정
    chat_box = wait_for_answer(driver, "대용량 요약", timeout=120)

    # ── 7. 답변에서 불렛포인트(li 태그) 텍스트 추출 ──────────────
    # 요약 결과가 li 태그로 구성되어 있으므로 li 태그만 수집
    # 빈 항목은 제외하고 텍스트만 이어붙여 전체 요약 텍스트 생성
    all_li_elements = chat_box.find_elements(By.TAG_NAME, "li")
    summary_items = [li.text.strip() for li in all_li_elements if li.text.strip()]
    full_text = " ".join(summary_items)

    print("\n  --- AI 요약 품질 확인 시작 ---")

    # ── 8. 요약 품질 검증 ─────────────────────────────────────────

    # [검증 1] 섹션 커버리지
    # 원문에서 반드시 언급되어야 하는 4개 섹션 중 2개 이상 포함되어야 함
    required_sections = ["경제", "6G", "바이오", "공간 컴퓨팅"]
    section_count = sum(1 for section in required_sections if section in full_text)
    print(f"  섹션 커버리지: {section_count}/4")
    assert section_count >= 2, \
        f"❌ 필수 섹션이 부족합니다. ({section_count}/4개 포함)"

    # [검증 2] 핵심 키워드 포함 여부
    # 주요 단어 10개 중 5개 이상 요약에 포함되어야 함
    essential_keywords = ["금리", "Fed", "표준화", "위성", "유전자", "윤리", "비전 프로", "생산성", "인플레이션", "6G"]
    found_keywords = [k for k in essential_keywords if k in full_text]
    print(f"  키워드 매칭: {len(found_keywords)}/10")
    assert len(found_keywords) >= 5, \
        f"❌ 핵심 키워드가 부족합니다. ({len(found_keywords)}/10개 발견)"

    print("  ✅ 요약 품질 확인 완료")
    print("🎉 대량 데이터 처리 테스트 통과!")