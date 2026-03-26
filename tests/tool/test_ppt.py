import pytest
from src.pages.auth.login_page import LoginPage


def test_login_success(logged_in_driver):
    assert "chat" in logged_in_driver.current_url


    

