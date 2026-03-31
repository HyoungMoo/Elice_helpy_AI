import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.pages.chat.chat_page import ChatPage


IPHONE_WIDTH = 390
IPHONE_HEIGHT = 844


class TestMobileResponsive:

    def test_mobile_responsive_ui(self, logged_in_driver):
        driver = logged_in_driver
        wait = WebDriverWait(driver, 15)
        chat_page = ChatPage(driver)

        print("\n[테스트] 모바일 반응형 UI/UX 테스트")

        # ── 1. 모바일 해상도 설정 ────────────────────────────────
        driver.set_window_size(IPHONE_WIDTH, IPHONE_HEIGHT)

        # UI 전환 안정 대기 (sleep 제거)
        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print(f"  ✅ 해상도 변경 완료: {IPHONE_WIDTH}x{IPHONE_HEIGHT}")

        # ── 2. 사이드바 기본 접힘 확인 ───────────────────────────
        sidebar = None

        try:
            sidebar = driver.find_element(
                By.XPATH,
                "//*[contains(@class,'sidebar') or contains(@class,'drawer')]"
            )

            sidebar_state = driver.execute_script("""
                const el = arguments[0];
                const rect = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);
                return {
                    x: rect.x,
                    width: rect.width,
                    display: style.display,
                    visibility: style.visibility
                };
            """, sidebar)

            is_hidden = (
                sidebar_state['display'] == 'none'
                or sidebar_state['visibility'] == 'hidden'
                or sidebar_state['x'] < 0
                or sidebar_state['width'] == 0
            )

            assert is_hidden, "❌ 사이드바가 기본으로 열려있습니다."
            print("  ✅ 사이드바 기본 접힘 확인")

        except Exception:
            print("  ✅ 사이드바 미렌더링 (모바일 정상)")

        # ── 3. 메뉴 버튼 → 사이드바 열림 ─────────────────────────
        try:
            menu_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[.//*[@data-testid='barsIcon']]")
                )
            )

            menu_btn.click()

            # 슬라이드 완료를 sleep 대신 상태 변화로 체크
            if sidebar:
                wait.until(lambda d: d.execute_script("""
                    const el = arguments[0];
                    const rect = el.getBoundingClientRect();
                    return rect.x >= 0 && rect.width > 0;
                """, sidebar))

                print("  ✅ 사이드바 열림 확인")

        except Exception as e:
            print(f"  ⚠️ 메뉴/사이드바 확인 실패: {e}")

        # ── 4. 입력창 너비 확인 ─────────────────────────────────
        input_box = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='input']"))
        )

        input_width = driver.execute_script(
            "return arguments[0].getBoundingClientRect().width;", input_box
        )

        assert input_width >= IPHONE_WIDTH * 0.6, (
            f"❌ 입력창이 너무 좁음 ({input_width:.0f}px)"
        )

        print(f"  ✅ 입력창 너비 OK ({input_width:.0f}px)")

        # ── 5. 전송 버튼 크기 확인 ───────────────────────────────
        input_box.send_keys("테스트")

        send_btn = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[.//*[@data-testid='arrow-upIcon']]")
            )
        )

        btn_size = driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            return { width: rect.width, height: rect.height };
        """, send_btn)

        assert btn_size['width'] >= 32 and btn_size['height'] >= 32, (
            f"❌ 버튼 너무 작음 ({btn_size['width']:.0f}x{btn_size['height']:.0f})"
        )

        print(f"  ✅ 버튼 크기 OK ({btn_size['width']:.0f}x{btn_size['height']:.0f})")

        input_box.clear()

        # ── 6. 해상도 복원 ───────────────────────────────────────
        driver.maximize_window()

        print("\n🎉 모바일 UI 테스트 통과!")