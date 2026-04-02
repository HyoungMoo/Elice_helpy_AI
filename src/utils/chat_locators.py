from selenium.webdriver.common.by import By


class ChatLocators:
    # 입력창
    INPUT = (By.CSS_SELECTOR, "textarea[name='input']")

    # 버튼
    SEND_BTN      = (By.XPATH, "//button[.//*[@data-testid='arrow-upIcon']]")
    STOP_BTN      = (By.XPATH, "//button[.//*[@data-testid='stopIcon']]")
    NEW_CHAT_BTN  = (By.XPATH, "//a[contains(@href,'/ai-helpy-chat') and .//span[text()='새 대화']]")
    PLUS_BTN      = (By.XPATH, "//button[.//*[@data-testid='plusIcon']]")
    ELLIPSIS_BTN  = (By.XPATH, ".//button[.//*[@data-testid='ellipsis-verticalIcon']]")
    ELLIPSIS_BTN_GLOBAL = (By.XPATH, "//button[.//*[@data-testid='ellipsis-verticalIcon']]")

    # 답변
    ANSWER        = (By.XPATH, "//div[contains(@class,'elice-aichat__markdown') and @data-status='complete']")

    # 사이드바
    SIDEBAR_ITEMS = (By.XPATH, "//ul[@data-testid='virtuoso-item-list']//a[@data-index]")
    CHAT_TITLE    = (By.XPATH, ".//p[contains(@class,'css-ff35j5')]")

    # 업로드
    UPLOAD_MENU   = (By.XPATH, "//*[contains(@class,'MuiListItemText-primary') and contains(text(),'파일 업로드')]")

    # 알림/에러
    TOAST         = (By.XPATH, "//div[@role='alert'] | //div[contains(@class,'MuiAlert')]")
    UPLOAD_ERROR  = (By.XPATH, "//div[@role='alert'] | //p[contains(@class,'Mui-error')]")
    CHAR_LIMIT    = (By.XPATH, "//p[contains(@class,'Mui-error')] | //div[contains(text(),'글자')]")
