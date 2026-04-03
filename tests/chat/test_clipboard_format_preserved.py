import pytest
import time
import subprocess
import pyautogui
import pygetwindow as gw
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from src.pages.chat.chat_page import ChatPage
from src.utils.chat_locators import ChatLocators

ANSWER_XPATH = ChatLocators.ANSWER[1]


# ────────────────────────────────────────────────────────────────
# CHAT-01-009: 외부 앱 서식 유지 / 클립보드 복사 테스트
# 질문과 답변의 복사 버튼을 클릭했을 때 클립보드에 복사되고
# 메모장에 붙여넣기했을 때 서식이 유지되는지 눈으로 확인
#
# ⚠️ Windows 전용 테스트 (메모장 사용)
# 검증 방식: 자동 검증 없이 눈으로 직접 확인
# ────────────────────────────────────────────────────────────────

# pyautogui 안전 설정
# FAILSAFE: 마우스를 화면 모서리로 이동하면 자동으로 중단
# PAUSE: 각 동작 사이에 0.3초 대기 (너무 빠르면 오류 발생)
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3


def focus_notepad():
    """
    메모장 창을 찾아서 포커스를 맞추는 함수
    pygetwindow 의 activate() 메서드에 버그가 있어서
    창 중앙을 직접 클릭하는 방식으로 우회
    """
    time.sleep(2)  # 메모장이 완전히 열릴 때까지 대기
    # 한글/영문 환경 모두 대응하기 위해 여러 제목으로 시도
    windows = (
        gw.getWindowsWithTitle("제목 없음 - 메모장")
        or gw.getWindowsWithTitle("Untitled - Notepad")
        or gw.getWindowsWithTitle("메모장")
    )
    assert windows, "❌ 메모장 창을 찾을 수 없습니다."
    win = windows[0]
    win.maximize()
    time.sleep(0.5)
    # 창 중앙을 클릭해서 포커스 확보
    pyautogui.click(win.left + win.width // 2, win.top + win.height // 2)
    time.sleep(0.3)


def focus_browser(driver):
    """
    메모장이 열리면서 브라우저가 뒤로 밀리는 현상 해결
    모든 창 중에서 Chrome/Helpy/Elice 관련 창을 찾아서 앞으로 가져옴
    """
    all_windows = gw.getAllWindows()
    for w in all_windows:
        title = w.title.lower()
        # 브라우저 창 제목에 chrome, helpy, elice 중 하나가 포함되면 해당 창으로 전환
        if "chrome" in title or "helpy" in title or "elice" in title:
            w.maximize()
            time.sleep(0.5)
            # 브라우저 상단 탭 영역 클릭해서 포커스 확보
            pyautogui.click(w.left + w.width // 2, w.top + 30)
            time.sleep(0.5)
            break
    # Selenium 레벨에서도 브라우저 창 포커스 복귀
    driver.switch_to.window(driver.current_window_handle)
    driver.execute_script("window.focus();")
    time.sleep(1)


class TestClipboardFormat:

    def test_clipboard_copy_preserves_format_in_notepad(self, logged_in_driver):
        """질문/답변 복사 버튼 클릭 후 메모장 붙여넣기 시 서식이 유지되는지 확인"""
        driver = logged_in_driver
        wait = WebDriverWait(driver, 30)
        chat_page = ChatPage(driver)

        # ── 1. 줄바꿈 포함 질문 전송 ──────────────────────────────────
        # Shift+Enter 로 줄바꿈을 포함한 질문을 전송
        # 줄바꿈 서식이 복사 후에도 유지되는지 확인하기 위함
        print("\n[STEP 1] 줄바꿈 포함 질문 전송")
        input_box = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[name='input']"))
        )
        input_box.send_keys("안녕")
        input_box.send_keys(Keys.SHIFT + Keys.ENTER)  # 줄바꿈 (전송 아님)
        input_box.send_keys("반가워")

        send_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//*[@data-testid='arrow-upIcon']]"))
        )
        send_btn.click()
        print("  ✅ 질문 전송 완료")

        # ── 2. 답변 생성 완료 대기 ────────────────────────────────────
        print("\n[STEP 2] 답변 생성 대기")
        chat_page.wait_for_answer("클립보드 테스트")
        print("  ✅ 답변 생성 확인 완료")

        # ══════════════════════════════════════════════════════════════
        # 케이스 1: 질문 복사 버튼 → 메모장 붙여넣기
        # ══════════════════════════════════════════════════════════════
        print("\n[케이스 1] 질문 복사 버튼 → 메모장 붙여넣기")

        my_q_xpath = (
            "//div[contains(@class,'MuiPaper-root')]"
            "[.//span[@data-status='complete' and contains(text(),'안녕')]]"
        )
        my_q_element = wait.until(EC.visibility_of_element_located((By.XPATH, my_q_xpath)))

        # 질문 박스 위로 마우스 이동 — 복사 버튼이 나타나도록 호버
        chat_page.hover_element(my_q_element)
        print("  📍 질문 박스 호버 중...")
        time.sleep(1.5)

        # 복사 버튼은 data-floating='true' div 안에 있음
        copy_btn = wait.until(EC.presence_of_element_located((By.XPATH,
            "//div[contains(@class,'MuiPaper-root')]"
            "[.//span[@data-status='complete' and contains(text(),'안녕')]]"
            "/..//div[@data-floating='true']//button[@aria-label='복사']"
        )))
        # 호버 상태에서만 보이는 버튼이라 JS 클릭으로 안정적으로 실행
        driver.execute_script("arguments[0].click();", copy_btn)
        time.sleep(0.5)
        print("  ✅ 질문 복사 버튼 클릭 완료")

        # 메모장 열고 붙여넣기 (닫지 않음 — 눈으로 직접 확인)
        subprocess.Popen("notepad.exe")
        focus_notepad()
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        print("  ✅ [케이스 1] 메모장 붙여넣기 완료 — 눈으로 확인하세요")

        # ══════════════════════════════════════════════════════════════
        # 케이스 2: 답변 복사 버튼 → 메모장 붙여넣기
        # ══════════════════════════════════════════════════════════════
        print("\n[케이스 2] 답변 복사 버튼 → 메모장 붙여넣기")

        # 메모장이 열리면서 브라우저 포커스가 사라졌으므로 복귀
        focus_browser(driver)

        answer_containers = driver.find_elements(By.XPATH, ANSWER_XPATH)
        assert len(answer_containers) > 0, "❌ [케이스 2] 답변 요소를 찾을 수 없습니다."

        last_answer = answer_containers[-1]
        chat_page.hover_element(last_answer)
        print("  📍 답변 영역 호버 중...")
        time.sleep(1.5)

        # 답변 복사 버튼은 elice-aichat__markdown 의 조상(css-i1h66d) 안에 있음
        answer_copy_btn = wait.until(EC.presence_of_element_located((By.XPATH,
            "//div[contains(@class,'elice-aichat__markdown')]"
            "/ancestor::div[contains(@class,'css-i1h66d')]"
            "//button[@aria-label='복사']"
        )))
        driver.execute_script("arguments[0].click();", answer_copy_btn)
        time.sleep(0.5)
        print("  ✅ 답변 복사 버튼 클릭 완료")

        # 복사 완료 표시 확인 — 복사 버튼이 checkIcon 으로 바뀌면 복사 성공
        try:
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//button[.//*[@data-testid='checkIcon']]")
            ))
            print("  ✅ 복사 완료 표시(checkIcon) 확인")
        except Exception:
            print("  ⚠️  복사 완료 표시를 찾지 못했습니다.")

        # 새 메모장 열고 붙여넣기 (닫지 않음 — 눈으로 직접 확인)
        subprocess.Popen("notepad.exe")
        focus_notepad()
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        print("  ✅ [케이스 2] 메모장 붙여넣기 완료 — 눈으로 확인하세요")

        print("\n🎉 클립보드 복사 테스트 완료!")