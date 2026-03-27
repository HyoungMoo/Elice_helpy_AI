import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from helpers import ANSWER_XPATH, send_question, wait_for_answer


# ────────────────────────────────────────────────────────────────
# CHAT-01-008: 질문 텍스트 수정 테스트
# 내가 보낸 질문 위에 마우스를 올리면 나타나는 편집 버튼을 클릭해서
# 질문을 수정하고 재전송했을 때 동작을 확인
#
# 검증 포인트:
# 1. 기존 질문(사과)에 대한 답변이 사라지는지
# 2. 수정된 질문(포도)에 대한 새 답변이 생성되는지
# ────────────────────────────────────────────────────────────────
def test_question_edit(logged_in_driver):
    driver = logged_in_driver
    # 최대 30초 동안 요소를 찾을 때까지 대기하는 설정
    wait = WebDriverWait(driver, 30)
    # 마우스 호버 같은 동작을 실행하기 위한 ActionChains
    actions = ActionChains(driver)

    # ── 1. 초기 질문 전송 ─────────────────────────────────────────
    # 나중에 수정할 원본 질문을 먼저 전송
    print("\n[STEP 1] 초기 질문 전송")
    send_question(driver, wait, "사과 칼로리 알려줘")
    print("  ✅ 초기 질문 전송 완료")

    # ── 2. 답변 생성 완료 대기 ────────────────────────────────────
    # 사과 칼로리에 대한 답변이 완료될 때까지 대기
    print("\n[STEP 2] 답변 생성 대기")
    wait_for_answer(driver, "사과 칼로리")

    # 답변 요소가 존재하는지 확인
    spans = driver.find_elements(By.XPATH, ANSWER_XPATH)
    assert len(spans) > 0, "❌ 사과 칼로리 답변을 찾을 수 없습니다."
    print(f"  ✅ 사과 칼로리 답변 확인 완료 (길이: {len(spans[-1].text.strip())}자)")

    # ── 3. 질문 박스 호버 → 편집 버튼 클릭 ──────────────────────
    # 질문 박스에 마우스를 올려야 편집(펜) 버튼이 나타남
    print("\n[STEP 3] 질문 박스 호버 후 편집 버튼 클릭")

    # '사과' 텍스트가 포함된 질문 박스를 XPath 로 찾기
    my_q_xpath = (
        "//div[contains(@class,'MuiPaper-root')]"
        "[.//span[@data-status='complete' and contains(text(),'사과')]]"
    )
    my_q_element = wait.until(EC.visibility_of_element_located((By.XPATH, my_q_xpath)))

    # 질문 박스 위로 마우스 이동 (호버) — 이래야 편집 버튼이 나타남
    actions.move_to_element(my_q_element).perform()
    print("  📍 질문 박스 호버 중...")
    time.sleep(1.5)  # 호버 후 편집 버튼이 나타날 때까지 대기

    # 편집 버튼(penIcon)을 일반 클릭이 아닌 JS 클릭으로 실행
    # 호버 상태에서만 보이는 버튼이라 JS 클릭이 더 안정적
    edit_btn = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[.//*[@data-testid='penIcon']]"))
    )
    driver.execute_script("arguments[0].click();", edit_btn)
    print("  ✅ 편집 버튼 클릭 완료")

    # ── 4. 텍스트 수정 후 보내기 클릭 ───────────────────────────
    # 편집 버튼 클릭 시 질문 내용이 수정 가능한 textarea 로 바뀜
    print("\n[STEP 4] 텍스트 수정 후 보내기 클릭")

    # 수정 가능한 textarea 찾아서 기존 텍스트 지우고 새 질문 입력
    edit_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//textarea")))
    edit_input.clear()
    edit_input.send_keys("포도 칼로리 알려줘")
    print("  ✅ 텍스트 수정 완료: '사과 칼로리 알려줘' → '포도 칼로리 알려줘'")

    # MuiButton-containedPrimary 클래스 + '보내기' 텍스트로 버튼 정확히 찾기
    # aria-label 이 아닌 클래스와 텍스트 조합으로 찾는 이유:
    # 전송 버튼(arrow-upIcon)과 구분하기 위함
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH,
        "//button[contains(@class,'MuiButton-containedPrimary') and contains(.,'보내기')]"
    )))
    save_btn.click()
    print("  ✅ 보내기 클릭 완료")

    # ── 5. 사과 답변 소멸 확인 ───────────────────────────────────
    # 질문을 수정하면 기존 사과 답변이 화면에서 사라져야 함
    # body 전체가 아닌 답변 영역(ANSWER_XPATH)만 확인
    # 사이드바 히스토리에 '사과' 텍스트가 남아있을 수 있으므로 답변 영역만 체크
    print("\n[STEP 5] 사과 답변 소멸 확인")
    time.sleep(2)  # 화면 갱신 대기

    try:
        answer_texts = [s.text.strip() for s in driver.find_elements(By.XPATH, ANSWER_XPATH)]
        assert not any("사과" in t for t in answer_texts), \
            "❌ 질문 수정 후 기존 사과 칼로리 답변이 소멸되지 않았습니다."
    except AssertionError:
        raise  # assert 실패는 그대로 전달
    except Exception:
        pass   # 답변 요소 자체가 없으면 이미 소멸된 것으로 간주
    print("  ✅ 기존 사과 칼로리 답변 소멸 확인 완료")

    # ── 6. 포도 칼로리 새 답변 생성 확인 ─────────────────────────
    # 수정된 질문(포도)에 대한 새 답변이 정상적으로 생성됐는지 확인
    print("\n[STEP 6] 포도 칼로리 새 답변 생성 확인")
    wait_for_answer(driver, "포도 칼로리")

    new_spans = driver.find_elements(By.XPATH, ANSWER_XPATH)
    # 답변 요소가 존재하는지 확인
    assert len(new_spans) > 0, "❌ 포도 칼로리 새 답변이 생성되지 않았습니다."
    # 답변 내용에 '포도' 가 포함됐는지 확인
    assert any("포도" in s.text.strip() for s in new_spans), \
        "❌ 새 답변에 포도 관련 내용이 없습니다."
    print(f"  ✅ 포도 칼로리 새 답변 생성 확인 완료 (길이: {len(new_spans[-1].text.strip())}자)")

    print("\n🎉 질문 텍스트 수정 테스트 통과!")