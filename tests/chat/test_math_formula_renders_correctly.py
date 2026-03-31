import pytest
from selenium.webdriver.common.by import By

from src.pages.chat.chat_page import ChatPage


# ────────────────────────────────────────────────────────────────
# CHAT-01-005: 수식 SVG 렌더링 테스트
# ────────────────────────────────────────────────────────────────


def assert_svg_formula(answer_container, label):
    """답변에 SVG 수식 렌더링 여부 확인"""
    try:
        formula_svg = answer_container.find_element(
            By.XPATH, ".//*[local-name()='svg' and @role='img']"
        )
        assert formula_svg.is_displayed(), f"❌ [{label}] 수식 SVG가 화면에 보이지 않습니다."
        print(f"  ✅ [{label}] 수식 SVG 렌더링 확인 완료")

    except AssertionError:
        raise
    except Exception:
        pytest.fail(f"❌ [{label}] 수식 SVG 요소를 찾을 수 없습니다.")


class TestFormulaRendering:

    def test_math_quadratic_formula(self, logged_in_driver):
        """이차방정식 수식 렌더링"""
        driver = logged_in_driver
        chat_page = ChatPage(driver)

        print("\n[케이스 1] 이차방정식 근의 공식 수식 렌더링 테스트")

        chat_page.send_question("이차방정식 근의 공식을 수식으로 써줘")
        print("  ✅ 질문 전송 완료")

        answer = chat_page.wait_for_answer("이차방정식")
        print(f"  ✅ 답변 생성 확인 (길이: {len(answer.text)}자)")

        assert_svg_formula(answer, "이차방정식")

        print("\n🎉 이차방정식 테스트 통과!")


    def test_chem_water_formula(self, logged_in_driver):
        """화학 수식 렌더링"""
        driver = logged_in_driver
        chat_page = ChatPage(driver)

        print("\n[케이스 2] 화학 수식 렌더링 테스트")

        chat_page.send_question("물 분자(H2O)를 수식 형태로 표현해줘")
        print("  ✅ 질문 전송 완료")

        answer = chat_page.wait_for_answer("화학수식")
        print(f"  ✅ 답변 생성 확인 (길이: {len(answer.text)}자)")

        assert_svg_formula(answer, "화학수식")

        print("\n🎉 화학 수식 테스트 통과!")


    def test_math_integral_formula(self, logged_in_driver):
        """적분 수식 렌더링"""
        driver = logged_in_driver
        chat_page = ChatPage(driver)

        print("\n[케이스 3] 적분 수식 렌더링 테스트")

        chat_page.send_question("정적분 공식을 수식으로 써줘")
        print("  ✅ 질문 전송 완료")

        answer = chat_page.wait_for_answer("적분수식")
        print(f"  ✅ 답변 생성 확인 (길이: {len(answer.text)}자)")

        assert_svg_formula(answer, "적분수식")

        print("\n🎉 적분 수식 테스트 통과!")