import time

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
        tool_ids: list = None,  # 추가
        visibility: str = "private",
        is_edit: bool = False):
        try:
            # 이름 입력 (필수)
            name_input = self.wait.until(
                EC.visibility_of_element_located((By.NAME, "name"))
            )
            if name:
                name_input.send_keys(Keys.CONTROL, "a")
                name_input.send_keys(Keys.DELETE)
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
                system_prompt_input.send_keys(Keys.CONTROL, "a")
                system_prompt_input.send_keys(Keys.DELETE)
                system_prompt_input.send_keys(system_prompt)

            # 포커스 이동 (만들기 버튼 활성화를 위해) << 이거 나중에 다른 방법 없는지 찾아보기
            system_prompt_input.send_keys(Keys.TAB)
            self.logger.info("규칙 입력 완료 - 포커스 이동")
            time.sleep(3)
                    
            # 시작 대화 입력 (선택)
            if conversation_starters:
                for i, starter in enumerate(conversation_starters[:4]):
                    starter_input = self.driver.find_element(
                        By.NAME, f"conversationStarters.{i}.value"
                    )
                    starter_input.send_keys(starter)
                    self.logger.info(f"시작 대화 {i+1} 입력 완료: {starter}")
            
                # 기능 선택 (선택)
            if tool_ids:
                for tool_id in tool_ids:
                    checkbox = self.driver.find_element(
                        By.CSS_SELECTOR, f"input[type='checkbox'][value='{tool_id}']"
                    )
                    self.driver.execute_script("arguments[0].click();", checkbox)
                    self.logger.info(f"기능 선택 완료: {tool_id}")
                        
                self.logger.info("에이전트 생성 입력 완료")
            
            # 만들기 / 업데이트 버튼 클릭
            btn_text = "업데이트" if is_edit else "만들기"
            create_btn = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//button[@type='button' and text()='{btn_text}']")
                )
            )
            if not create_btn.is_enabled():
                self.logger.info("생성 버튼 비활성화 → 클릭 생략")
                return 
            
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
        
    def is_agent_updated(self):
        try:
            alert = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "[role='alert']"))
            )
            return "에이전트가 업데이트 되었습니다." in alert.text
        except Exception as e:
            self.logger.info(f"업데이트 완료 알림 없음: {e}")
            return False
        
    def get_name_error_message(self):
        try:
            error = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//p[contains(text(),'이름을 입력해주세요')]")
                )
            )
            self.logger.info(f"에러 메시지: {error.text}")
            return error.text
        except Exception as e:
            self.logger.info(f"에러 메시지 없음: {e}")
            return None

    def get_rule_error_message(self):
        try:
            error = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//p[contains(text(),'규칙을 입력해주세요')]")
                )
            )
            self.logger.info(f"에러 메시지: {error.text}")
            return error.text
        except Exception as e:
            self.logger.info(f"에러 메시지 없음: {e}")
            return None
        
    def upload_file(self, file_path: str):
        file_input = self.driver.find_element(By.CSS_SELECTOR, "input.css-1bgri6b")
        self.driver.execute_script("arguments[0].style.display = 'block';", file_input)
        file_input.send_keys(file_path)
        self.logger.info(f"파일 업로드 시도: {file_path}")
        self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "svg.MuiSvgIcon-colorSuccess[data-testid='circle-checkIcon']")
            )
        )
        self.logger.info(f"파일 업로드 성공: {file_path}")
        
    def go_to_edit(self, name: str):
        edit_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//p[contains(text(),'{name}')]/ancestor::a//button[.//*[@data-testid='penIcon']]")
            )
        )
        edit_btn.click()
        self.logger.info(f"에이전트 수정 페이지 이동: {name}")
    
    def delete_agent(self, name: str):
        delete_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//p[contains(text(),'{name}')]/ancestor::a//button[.//*[@data-testid='trashIcon']]")
            )
        )
        delete_btn.click()
        self.logger.info(f"에이전트 삭제 버튼 클릭: {name}")

        # 삭제 확인 팝업
        confirm_btn = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@role='dialog']//button[text()='삭제']")
            )
        )
        confirm_btn.click()
        self.logger.info("삭제 확인 클릭 완료")
        
    def is_agent_deleted(self):
        try:
            alert = self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "[role='alert']"))
            )
            return "에이전트가 삭제되었습니다." in alert.text
        except Exception as e:
            self.logger.info(f"삭제 완료 알림 없음: {e}")
            return False
        
    def is_agent_in_list(self, name: str, should_exist: bool = True):
        try:
            if should_exist:
                self.wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, f"//p[contains(text(),'{name}')]")
                    )
                )
            else:
                self.wait.until(
                    EC.invisibility_of_element_located(
                        (By.XPATH, f"//p[contains(text(),'{name}')]")
                    )
                )
            self.logger.info(f"에이전트 목록 확인: {name}, 존재여부: {should_exist}")
            return True
        except Exception as e:
            self.logger.info(f"에이전트 목록 확인 실패: {e}")
            return False
        
    def search_agent(self, name: str):
        search_input = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder='AI 에이전트 검색']")
            )
        )
        search_input.send_keys(name)
        self.logger.info(f"에이전트 검색: {name}")