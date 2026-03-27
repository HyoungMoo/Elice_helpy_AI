from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time

class AccountSetting:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def go_to_account_setting(self):
        profile_icon = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.MuiAvatar-root")))
        profile_icon.click()
        time.sleep(1)

        account_setting = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='계정 관리']")))
        account_setting.click()
        time.sleep(1)

   