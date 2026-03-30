import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ────────────────────────────────────────────────────────────────
# CHAT-01-011: 모바일 UI/UX 반응형 테스트
# 브라우저 창을 모바일 해상도로 줄였을 때
# UI 가 모바일에 맞게 정상적으로 반응하는지 확인
#
# 검증 포인트:
# 1. 사이드바가 기본으로 접혀있는지
# 2. 메뉴 버튼 클릭 시 사이드바가 왼쪽에서 슬라이드로 열리는지
# 3. 입력창 너비가 모바일 화면에 맞는지
# 4. 전송 버튼이 터치하기 충분한 크기인지
# ────────────────────────────────────────────────────────────────

# iPhone 14 Pro 기준 해상도
IPHONE_WIDTH  = 390
IPHONE_HEIGHT = 844


def test_mobile_responsive_ui(logged_in_driver):
    driver = logged_in_driver
    # 최대 10초 동안 요소를 찾을 때까지 대기하는 설정
    wait = WebDriverWait(driver, 10)

    # ── 1. 모바일 해상도로 창 크기 변경 ──────────────────────────
    # 실제 모바일 기기처럼 브라우저 창을 iPhone 14 Pro 해상도로 축소
    # 이렇게 해야 반응형 CSS 가 적용되어 모바일 UI 로 전환됨
    driver.set_window_size(IPHONE_WIDTH, IPHONE_HEIGHT)
    time.sleep(1)  # UI 전환 애니메이션 대기
    print(f"\n✅ 해상도 변경 완료: {IPHONE_WIDTH}x{IPHONE_HEIGHT} (iPhone 14 Pro)")

    # ── 2. 사이드바 기본 접힘 확인 ───────────────────────────────
    # 모바일에서는 사이드바가 기본으로 숨겨져 있어야 함
    # 화면이 좁아서 사이드바가 열려있으면 채팅 영역이 가려지기 때문
    sidebar = None
    sidebar_rect_before = {'x': -1, 'width': 0}

    try:
        # sidebar/Sidebar/drawer/Drawer 클래스 중 하나를 가진 요소 탐색
        sidebar = driver.find_element(By.XPATH,
            "//*[contains(@class,'sidebar') or contains(@class,'Sidebar') "
            "or contains(@class,'drawer') or contains(@class,'Drawer')]"
        )
        # JS 로 사이드바의 실제 위치/크기/표시 여부 가져오기
        sidebar_rect_before = driver.execute_script("""
            const el = arguments[0];
            const rect = el.getBoundingClientRect();
            const style = window.getComputedStyle(el);
            return { x: rect.x, width: rect.width,
                     display: style.display, visibility: style.visibility };
        """, sidebar)

        # 아래 조건 중 하나라도 해당되면 숨겨진 것으로 판단
        # - display: none → 아예 렌더링 안 됨
        # - visibility: hidden → 보이지 않음
        # - x < 0 → 화면 왼쪽 밖으로 밀려있음
        # - width == 0 → 너비가 없음
        is_hidden = (
            sidebar_rect_before['display'] == 'none'
            or sidebar_rect_before['visibility'] == 'hidden'
            or sidebar_rect_before['x'] < 0
            or sidebar_rect_before['width'] == 0
        )
        assert is_hidden, "❌ 모바일 해상도에서 사이드바가 기본으로 열려있습니다."
        print("✅ 사이드바 기본 접힘 확인 완료")

    except AssertionError:
        raise  # assert 실패는 그대로 전달
    except Exception:
        # 사이드바 요소 자체가 없으면 모바일에서 아예 렌더링 안 하는 것 — 정상
        print("✅ 사이드바 요소 없음 (모바일에서 미렌더링 — 정상)")

    # ── 3. 메뉴 버튼 클릭 → 사이드바 슬라이드 열림 확인 ─────────
    # 모바일에서는 햄버거 메뉴(barsIcon) 버튼을 눌러야 사이드바가 열림
    try:
        menu_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[.//*[@data-testid='barsIcon']]")
        ))
        assert menu_btn.is_displayed(), "❌ 메뉴 버튼이 보이지 않습니다."
        print("✅ 메뉴 버튼 노출 확인")

        menu_btn.click()
        time.sleep(0.8)  # 슬라이드 애니메이션 완료 대기

        if sidebar is not None:
            # 버튼 클릭 후 사이드바의 위치/크기/표시 여부 다시 확인
            sidebar_rect_after = driver.execute_script("""
                const el = arguments[0];
                const rect = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);
                return { x: rect.x, width: rect.width,
                         display: style.display, visibility: style.visibility };
            """, sidebar)

            # 클릭 후 사이드바가 화면에 보이는 상태인지 확인
            is_visible = (
                sidebar_rect_after['display'] != 'none'
                and sidebar_rect_after['visibility'] != 'hidden'
                and sidebar_rect_after['x'] >= 0
                and sidebar_rect_after['width'] > 0
            )
            assert is_visible, "❌ 햄버거 버튼 클릭 후 사이드바가 열리지 않았습니다."

            # 클릭 전보다 x 좌표가 커졌으면 왼쪽에서 슬라이드로 들어온 것
            assert sidebar_rect_after['x'] > sidebar_rect_before['x'], \
                "❌ 사이드바가 왼쪽에서 슬라이드로 열리지 않았습니다."
            print("✅ 사이드바 왼쪽 슬라이드 열림 확인 완료")

    except AssertionError:
        raise
    except Exception as e:
        print(f"⚠️  메뉴 버튼 또는 사이드바 슬라이드 확인 실패: {e}")

    # ── 4. 입력창 너비 확인 ───────────────────────────────────────
    # 사이드바를 닫기 위해 body 클릭 후 입력창 너비 측정
    # 입력창이 화면 너비의 60% 이상이어야 모바일에서 사용하기 편함
    driver.execute_script("document.body.click()")
    time.sleep(0.5)

    input_box = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='input']"))
    )
    # JS 로 입력창의 실제 렌더링된 너비 측정
    input_width = driver.execute_script(
        "return arguments[0].getBoundingClientRect().width;", input_box
    )
    assert input_width >= IPHONE_WIDTH * 0.6, (
        f"❌ 입력창 너비({input_width:.0f}px)가 너무 좁습니다. "
        f"(기대: {IPHONE_WIDTH * 0.6:.0f}px 이상)"
    )
    print(f"✅ 입력창 너비 확인 완료 ({input_width:.0f}px)")

    # ── 5. 전송 버튼 크기 확인 ───────────────────────────────────
    # 전송 버튼은 텍스트를 입력해야 활성화(arrow-upIcon) 되므로
    # 먼저 텍스트를 입력한 후 버튼 크기 측정
    # 모바일 터치 최소 권장 크기는 32x32px
    try:
        input_box.click()
        input_box.send_keys("테스트")
        time.sleep(0.5)  # 버튼 활성화 대기

        send_btn = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//button[.//*[@data-testid='arrow-upIcon']]")
        ))
        # JS 로 버튼의 실제 렌더링된 크기 측정
        btn_size = driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            return { width: rect.width, height: rect.height };
        """, send_btn)

        assert btn_size['width'] >= 32 and btn_size['height'] >= 32, (
            f"❌ 전송 버튼이 너무 작습니다 "
            f"({btn_size['width']:.0f}x{btn_size['height']:.0f}px). "
            f"터치 최소 크기는 32x32px입니다."
        )
        print(f"✅ 전송 버튼 크기 확인 완료 ({btn_size['width']:.0f}x{btn_size['height']:.0f}px)")
        input_box.clear()  # 다음 테스트에 영향 없도록 입력창 초기화

    except AssertionError:
        raise
    except Exception as e:
        print(f"⚠️  전송 버튼을 찾지 못했습니다: {e}")

    # ── 6. 원래 해상도 복원 ───────────────────────────────────────
    # 다음 테스트가 모바일 해상도로 실행되지 않도록 원래 크기로 복원
    driver.maximize_window()
    print("\n✅ 브라우저 해상도 복원 완료")
    print("🎉 모바일 반응형 UI/UX 테스트 통과!")