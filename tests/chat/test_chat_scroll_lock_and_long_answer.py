import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from src.pages.chat.chat_page import ChatPage
from src.utils.chat_locators import ChatLocators

STOP_BTN_XPATH = ChatLocators.STOP_BTN[1]


# ────────────────────────────────────────────────────────────────
# CHAT-01-003 + CHAT-01-007: 자동 스크롤 및 뷰 유지 + 대용량 텍스트 답변 테스트
#
# 두 테스트를 합친 이유:
# - CHAT-01-007 은 3000자 이상 긴 답변을 요청하는 테스트
# - CHAT-01-003 은 답변 생성 중 스크롤 위치 유지 테스트
# - 긴 답변 생성 중에 스크롤 테스트를 하면 한 번에 두 가지 검증 가능
# ────────────────────────────────────────────────────────────────

MIN_LENGTH = 3000


class TestScrollLockAndLongAnswer:

    def test_scroll_position_stays_fixed_and_long_answer_generated(self, logged_in_driver):
        """
        CHAT-01-003: 답변 생성 중 위/아래 스크롤 시 화면 위치가 고정되는지 확인
        CHAT-01-007: 3000자 이상의 대용량 답변이 생성되는지 확인
        """
        driver = logged_in_driver
        wait = WebDriverWait(driver, 300)
        chat_page = ChatPage(driver)

        # ── 1. 질문 전송 ──────────────────────────────────────────────
        # 3000자 이상 긴 답변을 요청해서
        # 답변 생성 시간을 충분히 확보하고 스크롤바가 생기도록 유도
        chat_page.send_question("아무 주제로 3000자 이상의 보고서를 작성해줘")
        print("\n  ✅ 질문 전송 완료")

        # ── 2. 답변 생성 시작 확인 ───────────────────────────────────
        # stopIcon(중단 버튼)이 나타나면 AI 가 답변을 생성 중인 것
        wait.until(EC.presence_of_element_located((By.XPATH, STOP_BTN_XPATH)))
        print("  ⏳ 답변 생성 시작 확인")

        # ── 3. 채팅창 스크롤 정보 가져오는 함수 ─────────────────────
        # 이 서비스는 채팅창이 .ew8d2wp0 클래스 div 내부에서 스크롤됨
        # window.scrollBy 는 이 서비스에서 작동하지 않음
        # sh: 채팅창 전체 높이 / st: 현재 스크롤 위치 / ch: 화면에 보이는 높이
        def get_scroll_info():
            try:
                result = driver.execute_script("""
                    const el = document.querySelector('.ew8d2wp0');
                    if (!el) return null;
                    return { sh: el.scrollHeight, st: el.scrollTop, ch: el.clientHeight };
                """)
                return result
            except Exception:
                return None

        def check_position_fixed(label, fixed_st, seconds=3):
            """스크롤 위치가 고정되어 있는지 일정 시간 동안 확인"""
            for i in range(seconds):
                time.sleep(1)
                info = get_scroll_info()
                if info is None:
                    continue
                current_st = info['st']
                assert abs(fixed_st - current_st) < 20, \
                    f"❌ [CHAT-01-003] {label} — {i+1}초 후 화면 위치가 흔들립니다. (변화량: {abs(fixed_st - current_st)}px)"
            print(f"  ✅ [CHAT-01-003] {label} 위치 고정 확인 완료")

        # ── 4. 답변이 충분히 쌓일 때까지 대기 ───────────────────────
        # scrollHeight 가 화면 높이의 3배 이상이면 답변이 충분히 쌓인 것
        print("  ⏳ 답변이 충분히 쌓일 때까지 대기 중...")
        info = None
        for _ in range(60):  # 최대 60초 대기
            info = get_scroll_info()
            if info and info['sh'] > info['ch'] * 3:
                break
            time.sleep(1)
        assert info is not None, "❌ 채팅 컨테이너(.ew8d2wp0)를 찾을 수 없습니다."
        print(f"  ✅ 답변 충분히 쌓임 (전체높이: {info['sh']}px, 화면높이: {info['ch']}px)")

        chat_container = driver.find_element(By.CSS_SELECTOR, ".ew8d2wp0")
        actions = ActionChains(driver)

        # ── 5. 아래로 스크롤 후 위치 고정 확인 ──────────────────────
        # 실제 사용자가 마우스 휠로 아래로 내리는 동작 재현
        # 아래로 내렸을 때 그 위치에서 고정되어야 함
        print("  📍 아래로 스크롤 시도")
        actions.scroll_to_element(chat_container).scroll_by_amount(0, 400).perform()
        time.sleep(1)

        info = get_scroll_info() or {}
        print(f"  현재 스크롤 위치: {info.get('st', '?')}px")

        check_position_fixed("아래로 스크롤", info.get('st', 0))

        # ── 6. 위로 스크롤 후 위치 고정 확인 ────────────────────────
        # 실제 사용자가 마우스 휠로 위로 올리는 동작 재현
        # 이전 내용 확인하려고 위로 올렸을 때 위치가 고정되어야 함
        print("  📍 위로 스크롤 시도")
        actions.scroll_to_element(chat_container).scroll_by_amount(0, -800).perform()
        time.sleep(1)

        info = get_scroll_info() or {}
        dist_from_bottom = info.get('sh', 0) - (info.get('st', 0) + info.get('ch', 0))
        print(f"  현재 바닥과의 거리: {dist_from_bottom}px")
        assert dist_from_bottom > 200, \
            "❌ [CHAT-01-003] 위로 올렸으나 화면이 강제로 하단을 추적 중입니다!"

        check_position_fixed("위로 스크롤", info['st'])

        # ── 7. 답변 생성 완료까지 대기 ───────────────────────────────
        print("  ⏳ 답변 생성 완료 대기 중...")
        answer = chat_page.wait_for_answer("대용량 답변", timeout=300)
        answer_text = answer.text.strip()
        print(f"  ✅ 답변 생성 완료 (길이: {len(answer_text)}자)")

        # ── 8. 답변 길이 검증 ─────────────────────────────────────────
        # 3000자 이상이면 통과
        assert len(answer_text) >= MIN_LENGTH, (
            f"❌ [CHAT-01-007] 답변이 너무 짧습니다. "
            f"(현재: {len(answer_text)}자 / 기준: {MIN_LENGTH}자 이상)"
        )
        print(f"  ✅ [CHAT-01-007] 대용량 답변 확인 완료 ({len(answer_text)}자 ≥ {MIN_LENGTH}자)")

        print("\n🎉 자동 스크롤 및 대용량 답변 테스트 통과!")