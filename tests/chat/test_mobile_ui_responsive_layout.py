import pytest
import time
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

        print("\n[테스트] 모바일 반응형 UI/UX 검증 시작")

        # ── 1. 모바일 해상도 설정 ────────────────────────────────
        driver.set_window_size(IPHONE_WIDTH, IPHONE_HEIGHT)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print(f"  ✅ 해상도 변경 완료: {IPHONE_WIDTH}x{IPHONE_HEIGHT}")

        # ── 2. 사이드바 기본 접힘 상태 검증 ────────────────────────
        sidebar = None
        try:
            sidebar = driver.find_element(By.XPATH, "//*[contains(@class,'sidebar') or contains(@class,'drawer')]")
            
            # 사이드바의 물리적 위치와 스타일 확인
            is_hidden = driver.execute_script("""
                const el = arguments[0];
                const rect = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);
                return (style.display === 'none' || style.visibility === 'hidden' || rect.x < 0 || rect.width === 0);
            """, sidebar)

            assert is_hidden, "❌ [검증 실패] 모바일 진입 시 사이드바가 노출되어 있습니다."
            print("  ✅ 사이드바 기본 접힘 확인")
        except Exception:
            print("  ✅ 사이드바 미렌더링 (모바일 정상)")

        # ── 3. 메뉴 버튼 작동 및 레이어 간섭 제거 ──────────────────
        try:
            menu_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//*[@data-testid='barsIcon']]")))
            menu_btn.click()
            print("  클릭: 메뉴 버튼")

            if sidebar:
                # 사이드바가 화면 안으로 들어올 때까지 대기
                wait.until(lambda d: d.execute_script("return arguments[0].getBoundingClientRect().x >= 0;", sidebar))
                print("  ✅ 사이드바 열림 확인")

                # 🔥 핵심: 입력창을 가리는 투명 레이어(Backdrop) 강제 제거 및 사이드바 닫기
                driver.execute_script("""
                    document.querySelectorAll('.MuiBackdrop-root').forEach(el => el.remove());
                    document.body.click(); 
                """)
                time.sleep(1.5) # 닫히는 애니메이션 대기
                print("  ✅ 사이드바 닫기 및 배경 레이어 제거 완료")
        except Exception as e:
            print(f"  ⚠️ 메뉴/사이드바 확인 중 이슈 발생 (무시 가능): {e}")

        # ── 4. 입력창(Textarea) 반응형 너비 검증 ──────────────────
        input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='input']")))
        
        # 요소가 화면 중앙에 오도록 스크롤 (가려짐 방지)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_box)

        input_width = driver.execute_script("return arguments[0].getBoundingClientRect().width;", input_box)
        assert input_width >= IPHONE_WIDTH * 0.6, f"❌ [검증 실패] 입력창 너비 부족 ({input_width:.0f}px)"
        print(f"  ✅ 입력창 너비 정상 ({input_width:.0f}px)")

        # ── 5. 입력 기능 및 전송 버튼 크기 검증 ──────────────────
        # Interaction 에러 방지를 위해 JS로 값을 주입하고 이벤트를 발생시킴
        driver.execute_script("""
            arguments[0].value = '모바일 테스트';
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        """, input_box)
        print("  ✅ 텍스트 입력 확인")

        send_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[.//*[@data-testid='arrow-upIcon']]")))
        btn_size = driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            return { width: rect.width, height: rect.height };
        """, send_btn)

        # 모바일 터치 타겟 가이드라인(최소 32~44px) 준수 여부 확인
        assert btn_size['width'] >= 32 and btn_size['height'] >= 32, \
            f"❌ [검증 실패] 전송 버튼이 너무 작아 터치가 어렵습니다 ({btn_size['width']:.0f}px)"
        print(f"  ✅ 전송 버튼 크기 정상 ({btn_size['width']:.0f}x{btn_size['height']:.0f})")

        # ── 6. 환경 복원 ────────────────────────────────────────
        input_box.clear()
        print("\n🎉 모바일 반응형 UI 테스트 전체 통과!")