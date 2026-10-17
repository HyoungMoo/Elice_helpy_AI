# Elice AI HelpyChat QA 자동화 프로젝트

**Python · Selenium · Pytest · GitLab CI/CD · Allure**

엘리스 AI HelpyChat 웹서비스의 주요 기능을 대상으로 **E2E(End-to-End) 자동화 테스트**를 구현한 프로젝트입니다. 인증 및 계정 관리, AI 채팅, 생성 도구, 시스템 설정을 검증하며, Page Object Model(POM) 구조와 GitLab CI/CD를 활용해 반복 테스트 실행을 관리합니다.

> 이 문서는 저장소에 포함된 실제 소스코드와 CI 설정을 기준으로 작성했습니다. 테스트 성공률·커버리지 등 실행 결과 수치는 별도 결과 자료가 확인되지 않아 기재하지 않았습니다.

## 1. 프로젝트 개요

| 항목 | 내용 |
| --- | --- |
| 대상 서비스 | Elice AI HelpyChat |
| 테스트 유형 | 웹 UI / E2E 기능 자동화 테스트 |
| 자동화 기술 | Python, Selenium WebDriver, Pytest |
| 설계 방식 | Page Object Model(POM), Pytest Fixture |
| CI/CD | GitLab CI/CD (Push / Schedule) |
| 리포트 | Allure HTML, JUnit XML (Schedule 파이프라인) |
| 팀 | 엘리스 SW QA 트랙 4기 1팀 — 구형모, 유호선, 정은하 |

## 2. 테스트 범위

실제 `tests/` 디렉터리에는 다음과 같은 테스트가 구현되어 있습니다.

| 영역 | 주요 검증 항목 | 경로 |
| --- | --- | --- |
| 인증·계정 | 회원가입 진입, 로그인·로그아웃, 계정 설정, 계정 탈퇴 | `tests/auth/` |
| AI 채팅 | 입력값 유효성, 대화 기록, 질문 수정, 응답 중지, 새 대화, 새로고침 후 동작 | `tests/chat/` |
| 채팅 UI·콘텐츠 | 긴 응답과 스크롤, 모바일 반응형, 파일 업로드 후 응답, 링크, 수식 렌더링, 클립보드 | `tests/chat/` |
| 생성 도구 | 에이전트, PPT, 퀴즈 생성 및 입력 조건·중지 동작 | `tests/tool/` |
| 시스템 설정 | 언어 변경, 새로고침 후 언어 유지, 채팅 상태 유지, 브라우저 언어 감지 | `tests/system/` |

저장소에서 확인되는 `test_` 함수 정의는 **총 79개**입니다. 이는 정적 코드 기준이며, 실제 실행 시 수집되는 테스트 건수 또는 별도로 관리한 테스트 케이스 총수와 반드시 일치하지는 않습니다.

### 대표 테스트 시나리오

**AI 채팅**
- 입력값이 비어 있거나 공백만 있는 경우 전송 버튼의 활성화 상태 검증
- 기존 질문을 수정한 뒤 새로운 답변이 생성되는지 확인
- 답변 생성 중 중지 기능 및 입력창 상태 확인
- 대화 기록의 검색·수정·삭제, 신규 대화 생성 동작 확인
- 긴 응답의 출력 및 스크롤 위치 동작 검증
- JPG·PDF·XLSX 파일 업로드 후 AI 응답 확인
- 모바일 화면 레이아웃과 SVG 수식 표시 검증

**생성 도구**
- 에이전트 생성 시 필수 입력값 및 선택 입력값 검증
- PPT 생성 시 주제 미입력 오류 메시지와 생성 버튼 상태 확인
- PPT 생성 중 중지 및 생성 결과 다운로드 관련 동작 검증
- 퀴즈 생성 옵션과 필수 입력값에 따른 동작 검증

**시스템 설정**
- 언어 설정 변경 후 UI 반영 확인
- 언어 변경·새로고침 시 설정 및 대화 상태 유지 여부 확인

## 3. 테스트 자동화 구조

### Page Object Model (POM)

화면별 동작을 `src/pages/`에 분리하고, 테스트 시나리오는 `tests/`에서 관리합니다. 화면 요소 탐색에 사용되는 로케이터는 `src/utils/`의 영역별 모듈로 구분되어 있습니다.

- `src/pages/auth/`: 로그인, 로그아웃, 회원가입, 계정 설정
- `src/pages/chat/`: AI 채팅 관련 화면 동작
- `src/pages/tool/`: 에이전트, PPT, 퀴즈 생성 도구
- `src/pages/system/`: 시스템 설정
- `src/utils/`: 로케이터 및 로깅 유틸리티

### Pytest Fixture

`tests/conftest.py`에서 공통 실행 환경을 관리합니다.

| Fixture | 역할 |
| --- | --- |
| `driver` | Headless Chrome 실행, 창 크기 및 다운로드 경로 설정, 테스트 후 브라우저 종료 |
| `logged_in_driver` | `driver`를 사용해 로그인 페이지에 접근하고 지정된 테스트 계정으로 로그인 |
| `fresh_driver` | 별도 로그인 없이 기본 브라우저 객체 제공 |

`driver`는 기본적으로 `1920×1080` 해상도와 Headless Chrome 옵션을 사용합니다. 다운로드 경로는 `reports/downloads/`입니다.

## 4. 프로젝트 구조

```text
.
├── .gitlab-ci.yml
├── .gitignore
├── README.md
├── pytest.ini
├── requirements.txt
├── src/
│   ├── config.py
│   ├── pages/
│   │   ├── auth/
│   │   │   ├── accountsetting_page.py
│   │   │   ├── login_page.py
│   │   │   ├── logout_page.py
│   │   │   └── signup_page.py
│   │   ├── chat/
│   │   │   └── chat_page.py
│   │   ├── system/
│   │   │   └── settings_page.py
│   │   └── tool/
│   │       ├── agent_page.py
│   │       ├── ppt_page.py
│   │       ├── quiz_page.py
│   │       └── tool_page.py
│   ├── resources/
│   │   ├── assets/
│   │   └── test_files/
│   └── utils/
│       ├── auth_locators.py
│       ├── chat_locators.py
│       ├── logger.py
│       └── tool_locators.py
├── tests/
│   ├── conftest.py
│   ├── auth/
│   ├── chat/
│   ├── system/
│   └── tool/
└── reports/
    ├── downloads/
    └── logs/
```

`reports/screenshots/`, `reports/allure-results/`, `reports/allure-report/` 등은 실행 과정에서 생성될 수 있는 경로입니다.

## 5. 실행 환경 및 설치

### 사전 준비

- Python 및 pip
- Google Chrome 또는 호환되는 Chromium 브라우저
- Selenium에서 사용할 수 있는 ChromeDriver 환경
- **테스트 전용 계정 인증 정보**
- Allure HTML 리포트를 로컬에서 생성하려면 별도 Allure CLI 설치

저장소의 `requirements.txt`에는 다음 패키지가 명시되어 있습니다.

| 패키지 | 버전 | 용도 |
| --- | --- | --- |
| `selenium` | 4.41.0 | 브라우저 UI 자동화 |
| `pytest` | 9.0.2 | 테스트 실행 |
| `allure-pytest` | 2.13.5 | Allure 결과 데이터 생성 |
| `pyperclip` | 1.11.0 | 클립보드 접근 |
| `python-pptx` | 1.0.2 | PPT 파일 처리 및 검증 |

### 1) 가상환경 생성

```bash
python -m venv venv
```

Windows:

```powershell
venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

### 2) 패키지 설치

```bash
pip install -r requirements.txt
```

### 3) 테스트 계정 설정

`src/pages/auth/login_page.py`는 실행 시 `src/resources/credentials.json`을 읽습니다. 로컬 실행 전 해당 파일에 프로젝트에서 사용하는 **테스트 전용 계정 정보**를 준비해야 합니다.

`tests/conftest.py`의 `logged_in_driver`는 `user_2` 계정을 사용합니다. 필요한 계정 키와 JSON 형식은 `LoginPage` 구현 및 팀의 테스트 계정 관리 기준에 맞춰 설정하세요.

> 실제 아이디, 비밀번호, 토큰 등 인증 정보는 Git 저장소에 커밋하지 마세요. CI에서는 GitLab 변수 `CREDENTIALS_JSON`으로 인증 정보 파일을 주입하도록 설정되어 있습니다.

## 6. 테스트 실행

프로젝트 루트 디렉터리에서 실행합니다.

**전체 테스트**

```bash
pytest tests/
```

**영역별 테스트**

```bash
pytest tests/auth/
pytest tests/chat/
pytest tests/tool/
pytest tests/system/
```

**특정 파일 테스트**

```bash
pytest tests/chat/test_chat_question_edit.py
pytest tests/tool/test_agent.py
pytest tests/tool/test_ppt.py
```

**Allure 결과 생성**

```bash
pytest tests/ --alluredir=reports/allure-results
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

`pytest.ini`에는 `addopts = -v -s` 및 `pythonpath = .`이 설정되어 있습니다.

> 일부 테스트는 로컬 OS, 클립보드, 외부 서비스 응답 및 테스트 계정 상태에 영향을 받을 수 있습니다. 특히 CI에서는 클립보드 서식 검증과 수식 렌더링 테스트를 제외하도록 설정되어 있습니다.

## 7. GitLab CI/CD

`.gitlab-ci.yml`에는 `test` 스테이지의 두 작업이 정의되어 있습니다.

### `run_qa_push` — 변경 범위 기반 테스트

**실행 조건:** `main` 브랜치에 Push된 파이프라인

Git diff로 직전 커밋 대비 변경 파일을 확인하고 실행 대상을 결정합니다.

| 변경된 경로 | 실행 대상 |
| --- | --- |
| `src/pages/chat/*.py` | `tests/chat/` |
| `src/pages/tool/*.py` | `tests/tool/` |
| `src/pages/auth/*.py` | `tests/auth/` |
| `src/pages/system/*.py`, `src/utils/*.py`, `src/config.py` | 전체 `tests/` |
| `tests/` 아래 테스트 파일 | 해당 변경 테스트 파일 |

변경된 테스트 대상이 없으면 테스트 실행을 건너뛰도록 되어 있습니다. 이 방식은 변경 영역과 관련된 테스트를 우선 실행하기 위한 **파일 경로 기반 선별 실행**입니다.

### `run_qa_schedule` — 정기 회귀 테스트

**실행 조건:** GitLab Schedule 파이프라인

- 기본적으로 `tests/` 전체 실행 (`TEST_PATH` 변수로 경로 변경 가능)
- JUnit XML 생성: `reports/result.xml`
- Allure 결과 생성: `reports/allure-results/`
- Allure HTML 리포트 생성: `reports/allure-report/`
- 실행 결과 및 스크린샷을 GitLab Artifact로 보관 (설정상 1주)

두 작업 모두 Linux에서 `xvfb-run`을 통해 브라우저 테스트를 실행합니다. 다음 테스트 파일은 CI에서 제외됩니다.

- `tests/chat/test_clipboard_format_preserved.py`
- `tests/chat/test_math_formula_renders_correctly.py`

**현재 CI 설정의 주의점:** 테스트 실행 명령에 `|| true`가 사용되어 테스트 실패가 잡(Job)의 실패 상태로 전파되지 않을 수 있습니다. 따라서 테스트 실패 여부는 Allure·JUnit 결과 및 로그에서 별도로 확인해야 합니다. 또한 `run_qa_push`는 실패 시 스크린샷 Artifact 저장을 설정하지만, 위 동작 때문에 실패가 잡 상태로 표시되지 않을 수 있습니다.

## 8. 테스트 결과 확인 및 개선 방향

프로젝트는 테스트 결과를 Allure 리포트와 로그로 확인할 수 있도록 구성되어 있습니다. 다만 이 압축파일에는 실제 실행 결과 보고서가 포함되어 있지 않으므로, 현재 테스트 통과율이나 결함 건수는 기재하지 않았습니다.

향후 개선 가능한 항목은 다음과 같습니다.

- CI에서 테스트 실패가 파이프라인 상태에 반영되도록 `|| true` 처리 방식 검토
- 테스트 케이스 관리 문서와 Pytest 수집 결과를 대조해 자동화 커버리지 산정 근거 명확화
- 로컬·CI 환경별 실행 제약과 제외 테스트의 원인 문서화
- 변경 파일 감지 로직에서 공통 의존성 및 여러 커밋 Push 상황에 대한 처리 검토

## 9. 팀

**엘리스 SW QA 트랙 4기 1팀**

- 구형모
- 유호선
- 정은하

---

본 README는 업로드된 소스코드의 구조 및 설정을 설명한 문서입니다. 실제 테스트 결과와 개인별 기여도는 별도 산출물로 확인 후 추가하는 것을 권장합니다.
