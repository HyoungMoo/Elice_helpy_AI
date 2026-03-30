import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import (
    SIDEBAR_ITEMS_XPATH,
    send_question, wait_for_answer, click_new_chat, get_sidebar_items
)


# ────────────────────────────────────────────────────────────────
# CHAT-02-001: 사이드바 시간순 표시 테스트
# 새 대화를 여러 개 생성했을 때
# 사이드바에 가장 최근 대화가 맨 위에 오는 순서로 표시되는지 확인
#
# 검증 방식:
# 5개 대화를 순서대로 생성 후
# data-index 속성이 0(최신)부터 순서대로 증가하는지 확인
# ────────────────────────────────────────────────────────────────

# 대화 생성에 사용할 질문 목록 (5개 순서대로 생성)
CHAT_TITLE_XPATH = ".//p[contains(@class,'css-ff35j5')]"

QUESTIONS = [
    "사과 칼로리 알려줘",
    "바나나 칼로리 알려줘",
    "포도 칼로리 알려줘",
    "딸기 칼로리 알려줘",
    "수박 칼로리 알려줘",
]


def test_sidebar_chat_order(logged_in_driver):
    driver = logged_in_driver
    # 최대 30초 동안 요소를 찾을 때까지 대기하는 설정
    wait = WebDriverWait(driver, 30)

    print("\n[테스트] 사이드바 대화 순서 확인 테스트")

    # ── 1. 5개 대화 순서대로 생성 ─────────────────────────────────
    # 각 질문마다 새 대화방을 만들고 질문을 전송해서
    # 사이드바에 5개의 대화가 순서대로 쌓이게 함
    created_titles = []

    for i, question in enumerate(QUESTIONS):
        print(f"\n  [{i+1}/5] 새 대화 생성 후 질문: {question}")

        # 새 대화 버튼 클릭 — 이전 대화방에서 나와서 새 대화방 생성
        click_new_chat(driver, wait)

        # 질문 전송
        send_question(driver, wait, question)

        # 답변 완료 대기 — 답변이 완료돼야 사이드바에 제목이 생성됨
        wait_for_answer(driver, f"대화 {i+1}")

        # 사이드바 첫 번째 항목(index=0) 제목 저장
        # 새 대화를 만들면 항상 맨 위(index=0)에 올라와야 함
        time.sleep(1)
        items = driver.find_elements(By.XPATH, SIDEBAR_ITEMS_XPATH)
        if items:
            title = items[0].find_element(By.XPATH, CHAT_TITLE_XPATH).text.strip()
            created_titles.append(title)
            print(f"  ✅ 사이드바 최신 항목: '{title}'")

    print(f"\n  생성된 대화 제목 순서: {created_titles}")

    # ── 2. 사이드바 순서 검증 ─────────────────────────────────────
    print("\n  사이드바 전체 순서 확인 중...")

    # 사이드바에 5개 이상 있는지 확인
    items = get_sidebar_items(driver, wait, min_count=5)
    assert len(items) >= 5, f"❌ 사이드바에 대화가 5개 미만입니다. (현재: {len(items)}개)"

    # data-index 속성값 추출
    # data-index=0 이 가장 최신, 숫자가 클수록 오래된 대화
    indices = [int(item.get_attribute("data-index")) for item in items]
    print(f"  사이드바 data-index 순서: {indices}")

    # indices 가 [0, 1, 2, 3, 4, ...] 처럼 정렬된 순서여야 함
    # sorted(indices) 와 같으면 순서가 올바른 것
    assert indices == sorted(indices), \
        f"❌ 사이드바 순서가 올바르지 않습니다. (현재 순서: {indices})"
    print("  ✅ 사이드바 인덱스 순서 확인 완료")

    # 사이드바 최상단(index=0)이 마지막으로 생성한 대화인지 확인
    # in 연산자로 양방향 포함 여부 확인 — AI 가 제목을 자동 생성하므로
    # 질문 텍스트가 일부만 포함될 수 있음
    latest_title = items[0].find_element(By.XPATH, CHAT_TITLE_XPATH).text.strip()
    print(f"  사이드바 최상단 대화: '{latest_title}'")
    print(f"  마지막으로 생성한 대화: '{created_titles[-1]}'")

    assert created_titles[-1] in latest_title or latest_title in created_titles[-1], \
        f"❌ 최신 대화가 사이드바 상단에 없습니다. (상단: '{latest_title}', 기대: '{created_titles[-1]}')"
    print("  ✅ 최신 대화가 사이드바 상단에 위치 확인 완료")

    print("\n🎉 사이드바 대화 순서 테스트 통과!")