import pytest
from selenium.webdriver.common.by import By

from src.pages.chat.chat_page import ChatPage


CHAT_TITLE_XPATH = ".//p"

QUESTIONS = [
    "사과 칼로리 알려줘",
    "바나나 칼로리 알려줘",
    "포도 칼로리 알려줘",
    "딸기 칼로리 알려줘",
    "수박 칼로리 알려줘",
]


class TestSidebarOrder:

    def test_sidebar_chat_order(self, logged_in_driver):
        driver = logged_in_driver
        chat_page = ChatPage(driver)

        print("\n[테스트] 사이드바 대화 순서 확인 테스트")

        created_titles = []

        # ── 1. 대화 생성 ────────────────────────────────────────
        for i, question in enumerate(QUESTIONS):
            print(f"\n  [{i+1}/5] 질문: {question}")

            chat_page.click_new_chat()
            chat_page.send_question(question)
            chat_page.wait_for_answer(f"대화 {i+1}")

            # 사이드바 최신 항목 안정적으로 가져오기
            items = chat_page.get_sidebar_items(min_count=1)
            latest_item = items[0]

            title = latest_item.find_element(By.XPATH, CHAT_TITLE_XPATH).text.strip()
            created_titles.append(title)

            print(f"  ✅ 최신 대화 제목: '{title}'")

        print(f"\n  생성된 제목 목록: {created_titles}")

        # ── 2. 사이드바 순서 검증 ───────────────────────────────
        print("\n  사이드바 순서 검증 중...")

        items = chat_page.get_sidebar_items(min_count=5)
        assert len(items) >= 5, f"❌ 대화 개수 부족 (현재: {len(items)})"

        # data-index 기반 검증
        indices = [int(item.get_attribute("data-index")) for item in items]
        print(f"  data-index: {indices}")

        assert indices == sorted(indices), \
            f"❌ 사이드바 순서 깨짐: {indices}"

        print("  ✅ 인덱스 순서 정상")

        # ── 3. 최신 대화 상단 검증 ──────────────────────────────
        latest_title = items[0].find_element(By.XPATH, CHAT_TITLE_XPATH).text.strip()

        print(f"  상단 제목: '{latest_title}'")
        print(f"  마지막 생성: '{created_titles[-1]}'")

        assert (
            created_titles[-1] in latest_title
            or latest_title in created_titles[-1]
        ), "❌ 최신 대화가 상단에 없음"

        print("  ✅ 최신 대화 위치 정상")

        print("\n🎉 사이드바 순서 테스트 통과!")