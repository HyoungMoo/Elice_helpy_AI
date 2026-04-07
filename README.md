# Elice AI HelpyChat QA 자동화 프로젝트

엘리스 AI 헬피챗의 주요 기능을 Selenium + Pytest 기반으로 자동화한 E2E 테스트 프로젝트입니다.

---

## 실행 환경

- Python 3.10 이상
- Chrome 또는 Chromium 브라우저
- (CI 환경) xvfb, chromium-chromedriver, default-jre

---

## 설치

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 의존성 패키지

| 패키지 | 버전 | 용도 |
|---|---|---|
| selenium | 4.41.0 | 브라우저 자동화 |
| pytest | 9.0.2 | 테스트 실행 |
| allure-pytest | 2.13.5 | 테스트 리포트 생성 |
| pyperclip | 1.11.0 | 클립보드 접근 |
| python-pptx | 1.0.2 | PPT 파일 검증 |

> `pytest-html`, `pytest-metadata`, `PyAutoGUI`, `PyGetWindow`, `python-dotenv`, `webdriver-manager` 는 현재 사용하지 않습니다.

---

## 실행 방법

**전체 테스트 실행**
```bash
pytest tests/ --tb=short
```

**특정 테스트만 실행**
```bash
pytest tests/chat/ --tb=short
pytest tests/tool/test_agent.py --tb=short
```

**Allure 리포트 생성**
```bash
pytest tests/ --alluredir=reports/allure-results
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

---

## 프로젝트 구조

```
├── src/
│   ├── pages/          # Page Object Model (POM)
│   │   ├── auth/       # 로그인/로그아웃
│   │   ├── chat/       # AI 대화
│   │   ├── tool/       # 에이전트/퀴즈/PPT
│   │   └── system/     # 시스템 설정
│   ├── utils/          # 로케이터, 유틸리티
│   └── config.py       # 환경 설정
├── tests/              # 테스트 코드
├── reports/            # 테스트 결과물
└── .gitlab-ci.yml      # CI/CD 파이프라인
```

---

## CI/CD

GitLab CI/CD 파이프라인으로 자동 실행됩니다.

- **push** : 변경된 파일 감지 후 관련 테스트만 선별 실행
- **schedule** : 전체 테스트 정기 자동 실행 (회귀 테스트)

---

## 팀

엘리스트랙 QA 4기 1팀 — 구형모, 유호선, 정은하
