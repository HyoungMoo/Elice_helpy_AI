import pytest
import time
import os
import pyperclip
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

def test_chat_large_data_with_summary_check(logged_in_driver):
    driver = logged_in_driver
    
    # 1. 파일 경로 및 데이터 읽기
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    file_path = os.path.join(project_root, "src", "resources", "large_text.txt")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    
    integrated_text = f"아래 내용을 핵심 위주로 요약해주고, 불렛포인트(-)를 사용해줘:\n\n{content}"
    
    # 2. 클립보드 복사
    pyperclip.copy(integrated_text)
    print(f"\n 클립보드 복사 완료 (길이: {len(integrated_text)}자)")

    # 3. 입력창 대기 및 클릭
    input_box = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='input']"))
    )
    input_box.click()
    time.sleep(1)

    # 4. Ctrl + V 실행
    print(" 붙여넣기(Ctrl+V) 실행 중...")
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    
    time.sleep(5)

    # 5. 전송 버튼 클릭
    send_btn_selector = "button[aria-label='보내기']"
    try:
        send_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, send_btn_selector))
        )
        send_btn.click()
    except:
        input_box.send_keys(Keys.ENTER)
        print(" 버튼 클릭 실패로 엔터 키 전송 시도")

    print(" 데이터 전송 완료. 요약 응답 대기 중...")
# 6. AI 답변 종료 체크 
    print(" AI가 요약 답변을 생성 중입니다...")
    
    # 클래스명 대신 data-status 속성을 활용해 답변 완료 시점을 정확히 캐치
    wait = WebDriverWait(driver, 120)
    chat_box_selector = "div[data-status='complete'].elice-aichat__markdown"
    
    try:
        # 답변이 완료되어 status가 complete로 바뀔 때까지 대기
        chat_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, chat_box_selector)))
        print(" AI 답변 생성 완료!")
    except:
        pytest.fail(" 120초 내에 답변이 완료되지 않았거나 구조가 달라졌습니다.")

   # 7. 완성된 답변 검출 (li 태그 기반)
    all_li_elements = chat_box.find_elements(By.TAG_NAME, "li")
    summary_items = [li.text.strip() for li in all_li_elements if li.text.strip()]
    full_text = " ".join(summary_items)

    
    print("\n --- AI 요약 품질 스코어링 시작 ---")
    
    # 1. 섹션 커버리지 (필수 4개 섹션 중 몇 개나 언급했나?)
    required_sections = ["경제", "6G", "바이오", "공간 컴퓨팅"]
    section_count = sum(1 for section in required_sections if section in full_text)
    section_score = (section_count / len(required_sections)) * 100
    
    # 2. 핵심 키워드 밀도 (주요 단어 10개 중 포함된 비율)
    essential_keywords = ["금리", "Fed", "표준화", "위성", "유전자", "윤리", "비전 프로", "생산성", "인플레이션", "6G"]
    found_keywords = [k for k in essential_keywords if k in full_text]
    keyword_score = (len(found_keywords) / len(essential_keywords)) * 100

    # 3. 최소 분량 검증 (요약이 너무 짧으면 정보 누락으로 간주)
    # 원문 대비 10% ~ 50% 사이면 적정 점수
    compression_ratio = len(full_text) / len(content)
    length_score = 100 if 0.1 <= compression_ratio <= 0.6 else 50

    # 최종 합산 점수 (가중치 적용 가능)
    final_score = (section_score * 0.4) + (keyword_score * 0.4) + (length_score * 0.2)
    
    print(f" 섹션 커버리지: {section_score}% ({section_count}/4)")
    print(f" 키워드 매칭: {keyword_score}% ({len(found_keywords)}개 발견)")
    print(f" 압축률: {compression_ratio:.2%}")
    print(f" 최종 요약 품질 점수: {final_score}점")

    # --- 합격/불합격 판정 기준 ---
    # 문장 하나 없다고 Fail이 아니라, 전체 점수가 70점 미만일 때만 Fail 처리
    PASS_THRESHOLD = 70
    if final_score < PASS_THRESHOLD:
        driver.save_screenshot("low_quality_summary.png")
        pytest.fail(f"요약 품질 미달 ({final_score}점). 키워드나 섹션이 부족합니다.")
    else:
        print(f"테스트 통과 (기준: {PASS_THRESHOLD}점)")