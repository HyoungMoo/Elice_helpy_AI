import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import send_question, wait_for_answer


# ────────────────────────────────────────────────────────────────
# CHAT-01-005: 복잡한 수식/화학 수식 렌더링 테스트
# 수학/화학 수식을 요청했을 때 일반 텍스트가 아닌
# SVG 수식 폰트(KaTeX/MathJax)로 렌더링되는지 확인
#
# SVG 렌더링이 중요한 이유:
# 일반 텍스트로 출력되면 "x = (-b ± √...)" 처럼 깨져 보일 수 있지만
# SVG 로 렌더링되면 수식 전용 폰트로 깔끔하게 출력됨
# ────────────────────────────────────────────────────────────────


def assert_svg_formula(answer_container, label):
    """
    답변 컨테이너 안에 수식 SVG 가 렌더링됐는지 확인하는 함수
    role='img' 속성을 가진 svg 태그를 찾아서 화면에 보이는지 검증
    local-name() 을 사용하는 이유: SVG 는 네임스페이스가 달라서
    일반 By.TAG_NAME 으로 찾으면 못 찾는 경우가 있음
    """
    try:
        formula_svg = answer_container.find_element(
            By.XPATH, ".//*[local-name()='svg' and @role='img']"
        )
        # SVG 요소가 있어도 화면에 안 보일 수 있으므로 is_displayed() 로 확인
        assert formula_svg.is_displayed(), f"❌ [{label}] 수식 SVG가 화면에 보이지 않습니다."
        print(f"  ✅ [{label}] 수식 SVG 렌더링 확인 완료")
    except AssertionError:
        raise  # assert 실패는 그대로 전달
    except Exception:
        # SVG 요소 자체를 못 찾은 경우 — 수식이 텍스트로만 출력된 것
        pytest.fail(f"❌ [{label}] 수식 SVG 요소를 찾을 수 없습니다. 수식 폰트로 출력되지 않았습니다.")


# ════════════════════════════════════════════════════════════════
# 케이스 1: 이차방정식 근의 공식
# 가장 기본적인 수학 수식으로 SVG 렌더링 여부 확인
# ════════════════════════════════════════════════════════════════
def test_math_quadratic_formula(logged_in_driver):
    driver = logged_in_driver
    # 최대 30초 동안 요소를 찾을 때까지 대기하는 설정
    wait = WebDriverWait(driver, 30)

    print("\n[케이스 1] 이차방정식 근의 공식 수식 렌더링 테스트")
    send_question(driver, wait, "이차방정식 근의 공식을 써줘")
    print("  ✅ 질문 전송 완료")

    # 답변 완료 대기 후 SVG 렌더링 확인
    answer = wait_for_answer(driver, "이차방정식")
    print(f"  ✅ 답변 생성 확인 (길이: {len(answer.text)}자)")

    assert_svg_formula(answer, "이차방정식")
    print("\n🎉 이차방정식 근의 공식 테스트 통과!")


# ════════════════════════════════════════════════════════════════
# 케이스 2: 화학 수식 (물 분자)
# 화학식도 수식 폰트로 렌더링되는지 확인
# ════════════════════════════════════════════════════════════════
def test_chem_water_formula(logged_in_driver):
    driver = logged_in_driver
    wait = WebDriverWait(driver, 30)

    print("\n[케이스 2] 화학 수식 렌더링 테스트")
    send_question(driver, wait, "물 분자(H2O)의 화학식과 구조를 수식으로 써줘")
    print("  ✅ 질문 전송 완료")

    answer = wait_for_answer(driver, "화학수식")
    print(f"  ✅ 답변 생성 확인 (길이: {len(answer.text)}자)")

    assert_svg_formula(answer, "화학수식")
    print("\n🎉 화학 수식 테스트 통과!")


# ════════════════════════════════════════════════════════════════
# 케이스 3: 적분 수식
# 복잡한 수학 기호(∫)가 포함된 수식도 SVG 로 렌더링되는지 확인
# ════════════════════════════════════════════════════════════════
def test_math_integral_formula(logged_in_driver):
    driver = logged_in_driver
    wait = WebDriverWait(driver, 30)

    print("\n[케이스 3] 적분 수식 렌더링 테스트")
    send_question(driver, wait, "정적분 공식을 수식으로 써줘")
    print("  ✅ 질문 전송 완료")

    answer = wait_for_answer(driver, "적분수식")
    print(f"  ✅ 답변 생성 확인 (길이: {len(answer.text)}자)")

    assert_svg_formula(answer, "적분수식")
    print("\n🎉 적분 수식 테스트 통과!")