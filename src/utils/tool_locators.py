from selenium.webdriver.common.by import By

# 공통
class CommonLocators:

    STOP_BTN = (By.XPATH, "//button[.//*[@data-testid='stopIcon']]")
    RETRY_BTN = (By.CSS_SELECTOR, "[role='dialog'] button[type='submit']")
    
    DIALOG = (By.CSS_SELECTOR, "[role='dialog']")
    TOOLTIP = (By.CSS_SELECTOR, "[role='tooltip']")

    STOP_ALERT = (By.XPATH, "//div[@role='alert' and .//div[contains(text(),'요청에 의해 답변 생성을 중지했습니다.')]]")
    ALERT = (By.CSS_SELECTOR, "[role='alert']")
    ERROR_MSG = (By.CSS_SELECTOR, "p.MuiFormHelperText-root.Mui-error[id$='-helper-text']")

class ToolPageLocators:
    GO_TO_TOOL = (By.XPATH, "//a[@href='/ai-helpy-chat/tools']")
    GO_TO_AGENT = (By.XPATH, "//a[@href='/ai-helpy-chat/agents']")

class PptLocators:
    GO_TO_PPT = (By.XPATH, "//a[.//p[text()='PPT 생성']]")
    
    TOPIC_INPUT = (By.NAME, "topic")
    INSTRUCTIONS_INPUT = (By.NAME, "instructions")
    SLIDES_COUNT_INPUT = (By.NAME, "slides_count")
    SECTION_COUNT_INPUT = (By.NAME, "section_count")
    SIMPLE_MODE_TOGGLE = (By.NAME, "simple_mode")
    
    SLIDES_COUNT_ERROR_MSG = (By.XPATH, "//input[@name='slides_count']/following::p[contains(@class,'Mui-error')][1]")
    SECTION_COUNT_ERROR_MSG = (By.XPATH, "//input[@name='section_count']/following::p[contains(@class,'Mui-error')][1]")
    SUBMIT_BTN = (By.XPATH, "//button[@type='submit' and @form='tool-factory-create_pptx']")
    DOWNLOAD_BTN = (By.XPATH, "//a[contains(text(),'생성 결과 다운받기')]")
    
    SUCCESS_MSG = (By.XPATH, "//p[contains(text(),'입력하신 내용 기반으로 PPT를 생성했습니다.')]")

class QuizLocators:
    GO_TO_QUIZ = (By.XPATH, "//a[.//p[text()='퀴즈 생성']]")
    
    OPTION_TYPE_SELECT = (By.ID, "mui-component-select-quiz_configs.0.option_type")
    DIFFICULTY_SELECT = (By.ID, "mui-component-select-quiz_configs.0.difficulty")
    CONTENT_INPUT = (By.NAME, "content")
    
    ANSWER_ITEM = (By.CSS_SELECTOR, "div[role='button'][data-answer]") # 주관식 1개
    CORRECT_ANSWER_ITEM = (By.CSS_SELECTOR, "div[role='button'][data-answer='true']") # 객관식 단일/복수
    
    SUBMIT_BTN = (By.XPATH, "//button[@type='submit' and @form='tool-factory-create_quiz_from_context']")
    
    SUCCESS_MSG = (By.XPATH, "//p[contains(text(),'입력하신 내용 기반으로 퀴즈를 생성했습니다.')]")

class AgentLocators:
    GO_TO_BUILDER = (By.XPATH, "//a[@href='/ai-helpy-chat/agents/builder']")
    GO_TO_MINE = (By.XPATH, "//a[@href='/ai-helpy-chat/agents/mine']")
    
    NAME_INPUT = (By.NAME, "name")
    DESCRIPTION_INPUT = (By.XPATH, "//input[@name='description']")
    SYSTEM_PROMPT_INPUT = (By.NAME, "systemPrompt")
    CATEGORY_SELECT = (By.ID, "agent-builder-purpose")
    FILE_INPUT = (By.CSS_SELECTOR, "input.css-1bgri6b")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='AI 에이전트 검색']")
    
    PUBLISH_SAVE_BTN = (By.XPATH, "//button[@type='submit' and @form='publish-setting-form']")
    DELETE_CONFIRM_BTN = (By.XPATH, "//div[@role='dialog']//button[text()='삭제']")
    
    NAME_ERROR_MSG = (By.XPATH, "//p[contains(text(),'이름을 입력해주세요')]")
    RULE_ERROR_MSG = (By.XPATH, "//p[contains(text(),'규칙을 입력해주세요')]")
    FILE_UPLOAD_SUCCESS = (By.CSS_SELECTOR, "svg.MuiSvgIcon-colorSuccess[data-testid='circle-checkIcon']")

    @staticmethod
    def category_option(purpose: str):
        return (By.XPATH, f"//li[@role='option' and @data-value='{purpose}']")
    
    @staticmethod
    def create_btn(is_edit: bool = False):
        btn_text = "업데이트" if is_edit else "만들기"
        return (By.XPATH, f"//button[@type='button' and text()='{btn_text}']")
    
    @staticmethod
    def visibility_radio(visibility: str):
        return (By.XPATH, f"//input[@type='radio' and @value='{visibility}']/ancestor::label")
    
    @staticmethod
    def agent_edit_btn(name: str):
        return (By.XPATH, f"//p[contains(text(),'{name}')]/ancestor::a//button[.//*[@data-testid='penIcon']]")
    
    @staticmethod
    def agent_delete_btn(name: str):
        return (By.XPATH, f"//p[contains(text(),'{name}')]/ancestor::a//button[.//*[@data-testid='trashIcon']]")
    
    @staticmethod
    def agent_in_list(name: str):
        return (By.XPATH, f"//p[contains(text(),'{name}')]")
    
    @staticmethod
    def conversation_starter(index: int):
        return (By.NAME, f"conversationStarters.{index}.value")
    
    @staticmethod
    def tool_checkbox(tool_id: str):
        return (By.CSS_SELECTOR, f"input[type='checkbox'][value='{tool_id}']")