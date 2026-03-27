from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from src.utils.logger import setup_logger

class AgentPage:
    def __init__(self, driver:WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver,10)
        self.logger = setup_logger("AgentPage")
    
    def go_to_builder(self):
        self.logger.info("에이전트 생성 페이지 이동 시도")
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/ai-helpy-chat/agents/builder']"))
        )
        element.click()
        self.logger.info("에이전트 생성 페이지 이동 완료")
    
    def go_to_mine(self):
        self.logger.info("내 에이전트 페이지 이동 시도")
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/ai-helpy-chat/agents/mine']"))
        )
        element.click()
        self.logger.info("내 에이전트 페이지 이동 완료")
        
    def create_agent(
        self, name: str, 
        system_prompt: str, # 규칙(필수)
        description: str = None, # 한줄 소개
        purpose: str = None, # 카테고리
        conversation_starters: list = None, # 시작 대화
        file_path: str = None, # 파일 업로드
        visibility: str = "private"):
        try:
            # 이름 입력 (필수)
            name_input = self.wait.until(
                EC.visibility_of_element_located((By.NAME, "name"))
            )
            if name:
                name_input.send_keys(name)
            
            # 한줄 소개 입력 (선택)
            if description: # By.NAME으로 찾을 시 ElementNotInteractableException 오류 발생
                description_input = self.driver.find_element(By.XPATH, "//input[@name='description']")
                description_input.send_keys(description)

            # 카테고리 선택 (선택, 기본값: 기타)
            if purpose:
                category = self.wait.until(
                    EC.element_to_be_clickable((By.ID, "agent-builder-purpose"))
                )
                category.click()

                option = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f"//li[@role='option' and @data-value='{purpose}']")
                    )
                )
                option.click()
                self.logger.info(f"카테고리 선택 완료: {purpose}")
            
            # 규칙 입력 (필수)
            system_prompt_input = self.driver.find_element(By.NAME, "systemPrompt")
            if system_prompt:
                system_prompt_input.send_keys(system_prompt)

            # 포커스 이동 (만들기 버튼 활성화를 위해) << 이거 나중에 다른 방법 없는지 찾아보기
            system_prompt_input.send_keys(Keys.TAB)
            self.logger.info("규칙 입력 완료 - 포커스 이동")
                    
            # 시작 대화 입력 (선택)
            if conversation_starters:
                for i, starter in enumerate(conversation_starters[:4]):
                    starter_input = self.driver.find_element(
                        By.NAME, f"conversationStarters.{i}.value"
                    )
                    starter_input.send_keys(starter)
                    self.logger.info(f"시작 대화 {i+1} 입력 완료: {starter}")
            
            self.logger.info("에이전트 생성 입력 완료")
            
            # 자료 업로드 (선택)
            if file_path:
                file_input = self.driver.find_element((By.NAME,""))
            
            # 만들기 버튼 클릭
            create_btn = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@type='button' and text()='만들기']")
                )
            )
            """ 이거 상황 봐서 쓰기
            if not create_btn.is_enabled():
                self.logger.info("생성 버튼 비활성화 → 클릭 생략")
                return 
            """
            create_btn.click()
           
            self.logger.info("만들기 버튼 클릭 완료")
            # 공개 설정 팝업
            # visibility: private(나만 보기), organization(기관 내 공유), 기본값: private
            if visibility != "private":
                radio = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f"//input[@type='radio' and @value='{visibility}']")
                    )
                )
                self.driver.execute_script("arguments[0].click();", radio)
                self.logger.info(f"공개 설정 선택 완료: {visibility}")

            # 저장 버튼 클릭
            save_btn = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@type='submit' and @form='publish-setting-form']")
                )
            )
            save_btn.click()
            self.logger.info("공개 설정 저장 완료")

        except Exception as e:
            self.logger.error(f"에이전트 생성 실패: {e}")
            raise 
    
    def is_agent_created(self):
        try:
            alert = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "[role='alert']"))
            )
            return "에이전트가 생성 되었습니다." in alert.text
        except Exception as e:
            self.logger.info(f"생성 완료 알림 없음: {e}")
            return False
    
    def get_error_messages(self):
        try:
            error = self.wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "p.MuiFormHelperText-root.Mui-error[id$='-helper-text']")
                )
            )
            self.logger.info(f"에러 메시지: {error.text}")
            return error.text
        except Exception as e:
            self.logger.info(f"에러 메시지 없음: {e}")
            return None