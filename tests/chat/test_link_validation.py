import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import send_question, wait_for_answer


# ────────────────────────────────────────────────────────────────
# CHAT-01-006: 올바른 링크 제공 테스트
# 링크 제공을 요청하는 질문을 보냈을 때
# 답변에 올바른 URL 이 포함되고 클릭 시 정상 접속되는지 확인
#
# 검증 포인트:
# 1. 답변에 google.com 링크가 포함됐는지
# 2. 링크 클릭 시 새 탭이 열리는지
# 3. 새 탭 URL 이 google.com 인지
# ────────────────────────────────────────────────────────────────
def test_link_google(logged_in_driver):
    driver = logged_in_driver
    # 최대 30초 동안 요소를 찾을 때까지 대기하는 설정
    wait = WebDriverWait(driver, 30)

    print("\n[테스트] 올바른 링크 제공 테스트")

    # ── 1. 질문 전송 ──────────────────────────────────────────────
    send_question(driver, wait, "구글 홈페이지 링크 알려줘")
    print("  ✅ 질문 전송 완료")

    # ── 2. 답변 완료 대기 ─────────────────────────────────────────
    answer = wait_for_answer(driver, "링크 테스트")
    print(f"  ✅ 답변 생성 확인 (길이: {len(answer.text)}자)")

    # ── 3. 답변 안에 google.com 링크 존재 여부 확인 ──────────────
    # 답변 컨테이너 안에서 href 에 google.com 이 포함된 a 태그 탐색
    # 링크가 없으면 테스트 즉시 실패
    try:
        link = answer.find_element(By.XPATH, ".//a[contains(@href, 'google.com')]")
    except Exception:
        pytest.fail("❌ 답변에 google.com 링크가 없습니다.")

    # 링크가 화면에 실제로 보이는지 확인 (숨겨진 링크는 클릭 불가)
    assert link.is_displayed(), "❌ 링크가 화면에 보이지 않습니다."
    link_href = link.get_attribute("href")
    print(f"  ✅ 링크 확인 완료: {link_href}")

    # ── 4. 링크 클릭 → 새 탭에서 열리는지 확인 ──────────────────
    # 클릭 전 현재 열려있는 탭 목록 저장
    original_window = driver.current_window_handle
    original_windows = set(driver.window_handles)

    link.click()
    time.sleep(2)  # 새 탭이 열릴 때까지 대기

    # 클릭 후 새로 생긴 탭이 있는지 확인
    new_windows = set(driver.window_handles) - original_windows
    assert len(new_windows) > 0, "❌ 링크 클릭 후 새 탭이 열리지 않았습니다."

    # 새로 열린 탭으로 전환
    new_window = new_windows.pop()
    driver.switch_to.window(new_window)
    time.sleep(2)  # 페이지 로딩 대기

    # ── 5. 새 탭 URL 이 google.com 인지 확인 ─────────────────────
    # 단순히 새 탭이 열리는 것뿐만 아니라
    # 실제로 google.com 으로 접속됐는지까지 검증
    current_url = driver.current_url
    print(f"  새 탭 URL: {current_url}")
    assert "google.com" in current_url, \
        f"❌ 새 탭이 google.com으로 접속되지 않았습니다. (현재 URL: {current_url})"
    print("  ✅ 새 탭에서 google.com 정상 접속 확인")

    # ── 6. 원래 탭으로 복귀 ──────────────────────────────────────
    # 새 탭을 닫고 원래 채팅 탭으로 돌아옴
    driver.close()
    driver.switch_to.window(original_window)

    print("\n🎉 올바른 링크 제공 테스트 통과!")