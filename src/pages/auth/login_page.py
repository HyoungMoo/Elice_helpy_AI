from src.config import Config
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class LoginPage:
    URL = f"{Config.base_url}/signin"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        with open("./src/resources/credentials.json", "r", encoding="utf-8") as f:
            self.credentials = json.load(f)

    def go_to_login_page(self):
        self.driver.get(self.URL)

    def login(self, user_key="user_1"):
        user = self.credentials[user_key]
        self.driver.find_element(By.NAME, "loginId").send_keys(user["email"])
        self.driver.find_element(By.NAME, "password").send_keys(user["password"])
        self.driver.find_element(By.XPATH, "//button[text()='Login']").click()