import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from helpers import (
    ANSWER_XPATH, SIDEBAR_ITEMS_XPATH,
    send_question, wait_for_answer,
    click_more_menu, get_sidebar_items, get_sidebar_titles
)


# ────────────────────────────────────────────────────────────────
# CHAT-02-002~006: 과거 대화 히스토리 통합 테스트
# 과거 대화 내용 조회 → 추가 질문 → 이름 변경 → 삭제 → 검색
# 순서대로 하나의 흐름으로 테스트
# ────────────────────────────────────────────────────────────────

# 사이드바 대화 제목을 가져오는 XPath
CHAT_TITLE_XPATH    = ".//p[contains(@class,'css-ff35j5')]"

# 검색 결과는 일반 사이드바와 다른 ul 구조로 렌더링되므로 별도 XPath 사용
SEARCH_RESULT_XPATH = "//ul[contains(@class,'css-1baokfq')]//a[contains(@href,'/ai-helpy-chat/chats/')]"
SEARCH_TITLE_XPATH  = ".//span[contains(@class,'MuiListItemText-primary')]"

# 검색 테스트에 사용할 키워드 (이 키워드가 포함된 대화가 사전에 존재해야 함)
TEST_KEYWORD  = "사과"

# 이름 변경 테스트에 사용할 새 이름
RENAME_TARGET = "새 대화방 이름 변경"


def test_chat_history_full(logged_in_driver):
    driver = logged_in_driver
    # 최대 30초 동안 요소를 찾을 때까지 대기하는 설정
    wait = WebDriverWait(driver, 30)

    # ── CHAT-02-002: 과거 대화 내용 누락 없이 기록 확인 ──────────
    # 사이드바에서 최신 대화방에 들어가서
    # 이전에 나눴던 대화 내용(답변)이 그대로 남아있는지 확인
    print("\n[CHAT-02-002] 과거 대화 내용 누락 확인")

    # 사이드바에 대화가 2개 이상 로딩될 때까지 대기
    items = get_sidebar_items(driver, wait, min_count=2)
    # 대화가 2개 미만이면 테스트 불가 — 사전에 대화를 만들어놔야 함
    assert len(items) >= 2, "❌ [CHAT-02-002] 과거 대화가 없습니다. 사전에 대화를 생성해주세요."

    # 가장 최신 대화방(index=0) 클릭해서 진입
    latest_chat = items[0]
    latest_chat_title = latest_chat.find_element(By.XPATH, CHAT_TITLE_XPATH).text.strip()
    latest_chat.click()
    time.sleep(1.5)  # 대화방 로딩 대기
    print(f"  최신 대화 '{latest_chat_title}' 진입")

    # 대화방 안에 완료된 답변(data-status='complete')이 하나라도 있으면 기록이 있는 것
    answers = driver.find_elements(By.XPATH, ANSWER_XPATH)
    assert len(answers) > 0, \
        f"❌ [CHAT-02-002] 과거 대화 '{latest_chat_title}'에 대화 내용이 없습니다."
    print(f"  ✅ 과거 대화 내용 확인 완료 ({len(answers)}개 답변 존재)")

    # ── CHAT-02-003: 과거 대화에 추가 질문 ───────────────────────
    # 기존 대화방에서 새 질문을 보냈을 때
    # AI 가 이전 대화 맥락을 기억하고 정상적으로 답변하는지 확인
    print("\n[CHAT-02-003] 과거 대화에 추가 질문")

    send_question(driver, wait, "저번에 무슨 대화를 나누었더라")
    wait_for_answer(driver, "추가 질문")

    # 마지막 답변이 비어있지 않으면 정상적으로 답변한 것
    containers = driver.find_elements(By.XPATH, ANSWER_XPATH)
    assert len(containers[-1].text.strip()) > 0, \
        "❌ [CHAT-02-003] 추가 질문에 대한 답변이 없습니다."
    print("  ✅ 추가 질문 답변 확인 완료")

    # ── CHAT-02-004: 현재 대화방 이름 변경 ───────────────────────
    # 사이드바에서 더보기(···) 버튼 → 이름 변경 메뉴 클릭 후
    # 새 이름으로 변경되었는지 사이드바에서 확인
    print("\n[CHAT-02-004] 대화 이름 변경 테스트")

    # 현재 들어와 있는 대화방(index=0)의 더보기 버튼 클릭
    items = get_sidebar_items(driver, wait, min_count=1)
    click_more_menu(driver, wait, items[0])

    # 드롭다운 메뉴에서 penIcon(연필 아이콘)이 있는 이름 변경 버튼 클릭
    rename_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//li[@role='menuitem'][.//*[@data-testid='penIcon']]")
    ))
    driver.execute_script("arguments[0].click();", rename_btn)
    time.sleep(0.5)

    # 이름 입력창에서 기존 텍스트 전체 선택 후 삭제하고 새 이름 입력
    rename_input = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@name='name']")
    ))
    rename_input.send_keys(Keys.CONTROL + "a")  # 전체 선택
    rename_input.send_keys(Keys.DELETE)          # 삭제
    time.sleep(0.2)
    rename_input.send_keys(RENAME_TARGET)        # 새 이름 입력
    time.sleep(0.3)

    # 확인/저장/변경 버튼 중 하나를 클릭해서 이름 변경 완료
    confirm_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., '확인') or contains(., '저장') or contains(., '변경')]")
    ))
    confirm_btn.click()
    time.sleep(1)

    # 사이드바 제목 목록에 변경한 이름이 있으면 성공
    titles = get_sidebar_titles(driver)
    assert any(RENAME_TARGET in t for t in titles), \
        f"❌ [CHAT-02-004] 이름 변경 실패 (현재 목록: {titles})"
    print(f"  ✅ 대화 이름 '{RENAME_TARGET}'으로 변경 확인 완료")

    # ── CHAT-02-005: 이름 변경한 대화 삭제 ───────────────────────
    # 위에서 이름 변경한 대화방을 삭제하고
    # 사이드바에서 해당 대화가 사라졌는지 확인
    print("\n[CHAT-02-005] 대화 삭제 테스트")

    # 사이드바에서 RENAME_TARGET 이름을 가진 대화 찾기
    items_before = get_sidebar_items(driver, wait, min_count=1)
    target_item = None
    for item in items_before:
        title = item.find_element(By.XPATH, CHAT_TITLE_XPATH).text.strip()
        if RENAME_TARGET in title:
            target_item = item
            break

    # 삭제할 대화를 찾지 못하면 테스트 실패
    assert target_item is not None, f"❌ [CHAT-02-005] '{RENAME_TARGET}' 대화를 찾을 수 없습니다."
    click_more_menu(driver, wait, target_item)

    # 드롭다운 메뉴에서 trashIcon(휴지통 아이콘)이 있는 삭제 버튼 클릭
    delete_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//li[@role='menuitem'][.//*[@data-testid='trashIcon']]")
    ))
    driver.execute_script("arguments[0].click();", delete_btn)
    time.sleep(0.5)

    # 삭제 확인 팝업에서 최종 삭제 버튼 클릭
    confirm_delete = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(), '삭제')]")
    ))
    confirm_delete.click()
    time.sleep(2)

    # 삭제된 항목이 사이드바에서 사라질 때까지 대기
    # virtuoso 가상 스크롤 특성상 개수 비교가 불안정하므로
    # 삭제한 이름이 목록에서 없어지는 걸로 확인
    try:
        wait.until(lambda d: not any(
            RENAME_TARGET in item.find_element(By.XPATH, CHAT_TITLE_XPATH).text.strip()
            for item in d.find_elements(By.XPATH, SIDEBAR_ITEMS_XPATH)
        ))
    except Exception:
        pass
    time.sleep(1)

    # 사이드바 제목 목록에 삭제한 이름이 없으면 성공
    titles_after = get_sidebar_titles(driver)
    assert not any(RENAME_TARGET in t for t in titles_after), \
        f"❌ [CHAT-02-005] 삭제된 대화 '{RENAME_TARGET}'이 여전히 사이드바에 있습니다."
    print(f"  ✅ 대화 삭제 확인 완료 ('{RENAME_TARGET}' 사이드바에서 제거됨)")

    # ── CHAT-02-006: 검색 기능 테스트 ────────────────────────────
    # 검색창에 키워드를 입력했을 때
    # 해당 키워드가 포함된 대화만 결과에 표시되는지 확인
    # 그리고 결과를 클릭하면 해당 대화방으로 이동하는지 확인
    print("\n[CHAT-02-006] 검색 기능 테스트")

    # 사이드바 상단의 검색(돋보기) 버튼 클릭
    search_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@role='button'][.//*[@data-testid='magnifying-glassIcon']]")
    ))
    search_btn.click()
    time.sleep(0.5)

    # 검색 입력창에 키워드 입력
    search_input = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@placeholder='Search']")
    ))
    search_input.send_keys(TEST_KEYWORD)
    time.sleep(1)

    # 검색 결과 목록이 나타날 때까지 대기
    # 검색 결과는 일반 사이드바와 다른 ul(css-1baokfq) 구조로 렌더링됨
    result_items = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, SEARCH_RESULT_XPATH)
    ))
    assert len(result_items) > 0, f"❌ [CHAT-02-006] '{TEST_KEYWORD}' 검색 결과가 없습니다."

    result_titles = [item.find_element(By.XPATH, SEARCH_TITLE_XPATH).text.strip() for item in result_items]
    print(f"  검색 결과 목록: {result_titles}")

    # 검색 결과 전체가 키워드를 포함하고 있어야 함
    # any() 가 아닌 all() 을 사용해서 무관한 대화가 섞이지 않았는지 확인
    assert all(TEST_KEYWORD in t for t in result_titles), \
        f"❌ [CHAT-02-006] 검색 결과에 '{TEST_KEYWORD}'와 무관한 대화가 포함되어 있습니다: {result_titles}"
    print(f"  ✅ 검색 결과 전체 키워드 확인 완료 ({len(result_items)}개)")

    # 첫 번째 검색 결과 클릭 → 해당 대화방으로 이동하는지 확인
    first_result = result_items[0]
    first_result_title = result_titles[0]
    first_result.click()
    time.sleep(1.5)

    # URL 에 /ai-helpy-chat/chats/ 가 포함되면 대화방으로 이동한 것
    current_url = driver.current_url
    assert "/ai-helpy-chat/chats/" in current_url, \
        f"❌ [CHAT-02-006] 검색 결과 클릭 후 대화방으로 이동하지 않았습니다. (현재 URL: {current_url})"

    # 이동한 대화방에 답변 내용이 있으면 정상 접속된 것
    answers = driver.find_elements(By.XPATH, ANSWER_XPATH)
    assert len(answers) > 0, "❌ [CHAT-02-006] 접속한 대화방에 내용이 없습니다."
    print(f"  ✅ '{first_result_title}' 대화방 접속 확인 완료")

    print("\n🎉 과거 대화 히스토리 전체 테스트 통과!")