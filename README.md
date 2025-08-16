# 🤖 커리어 코치 챗봇 API

> 이력서 기반 개인 맞춤형 면접 질문 생성 & 학습 경로 추천 시스템

## 🎯 프로젝트 개요

구직자의 이력서 내용(경력, 직무, 기술 스킬)을 기반으로 생성형 AI가 **맞춤형 면접 모의질문**을 생성하고, **자기 개발 학습 경로**를 제안하여 구직자의 합격률을 높이는 데 도움을 주는 백엔드 챗봇 API입니다.

## ✨ 핵심 차별화 포인트

### 🧠 **지능형 다단계 분석 시스템**
- **1단계**: 이력서 심층 분석 (강점/약점/성격 특성 파악)
- **2단계**: 분석 기반 맞춤형 면접 질문 생성
- **3단계**: 개인화된 학습 경로 설계

### 🎯 **실전 기반 개인화**
- 회사 유형별 면접 스타일 차별화 (스타트업/대기업/외국계)
- 경력 수준별 맞춤 질문 생성
- 실제 채용시장 트렌드 반영

### 🚀 **확장 가능한 아키텍처**
- Django Ninja 기반 고성능 API
- 모듈화된 AI 서비스 엔진
- 실시간 분석 결과 캐싱

## 📋 요구사항 충족

### ✅ **필수 기능**
1. **이력서 핵심 정보 입력 API** 
   - 경력 요약, 수행 직무, 기술 스킬 입력
   - 실시간 AI 분석 및 프로필 생성

2. **맞춤 면접 모의 질문 생성**
   - AI가 생성하는 **5개의 개인화된 면접 질문**
   - 회사 유형 & 포지션 레벨별 차별화

3. **자기 개발 학습 경로 추천**
   - 현재 수준 분석 기반 **단계별 학습 로드맵**
   - 구체적인 학습 자료 및 마일스톤 제시

## 🛠️ 기술 스택

- **Backend**: Django 5.2 + Django Ninja
- **AI**: OpenAI GPT-4o-mini
- **Database**: SQLite (개발) / PostgreSQL (운영)
- **Package Manager**: Poetry
- **Language**: Python 3.12

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 저장소 클론
git clone <repository-url>
cd career-coach-chatbot

# Poetry 설치 (없는 경우)
curl -sSL https://install.python-poetry.org | python3 -

# 의존성 설치
poetry install

# 환경 변수 설정
cp .env.example .env
# .env 파일에서 OPENAI_API_KEY 설정
```

### 2. 데이터베이스 설정

```bash
# 마이그레이션 실행
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

### 3. 서버 실행

```bash
# 개발 서버 시작
poetry run python manage.py runserver

# API 문서 확인: http://localhost:8000/api/docs
```

## 📚 API 사용법

### 1. 이력서 프로필 생성

```bash
POST /api/profiles
Content-Type: application/json

{
  "career_summary": "3년차 백엔드 개발자, Spring Boot/MSA/Python 기반 커머스 서비스 개발, AWS EC2 운영 경험",
  "job_role": "Spring Boot/MSA 기반 커머스 서비스 개발",
  "technical_skills": "Python, Django, Spring Boot, AWS EC2, Docker, MySQL, Redis",
  "experience_years": 3
}
```

**응답**: 프로필 ID + AI 분석 결과

### 2. 맞춤형 면접 질문 생성

```bash
POST /api/interview-sessions
Content-Type: application/json

{
  "profile_id": "프로필_ID",
  "target_company_type": "startup",
  "target_position_level": "mid"
}
```

**응답**: 5개의 개인화된 면접 질문

### 3. 학습 경로 추천

```bash
POST /api/learning-paths
Content-Type: application/json

{
  "profile_id": "프로필_ID",
  "target_goal": "skill_enhancement",
  "preferred_duration_months": 3
}
```

**응답**: 단계별 학습 로드맵

## 🎨 API 문서

서버 실행 후 다음 URL에서 상세한 API 문서를 확인할 수 있습니다:

- **Swagger UI**: `http://localhost:8000/api/docs`
- **ReDoc**: `http://localhost:8000/api/redoc`

## 📊 프로젝트 구조

```
career-coach-chatbot/
├── career_coach/          # Django 프로젝트 설정
│   ├── settings.py       # 프로젝트 설정
│   └── urls.py          # URL 라우팅
├── chatbot/             # 메인 앱
│   ├── models.py        # 데이터 모델
│   ├── schemas.py       # Pydantic 스키마
│   ├── api.py          # Django Ninja API
│   └── ai_service.py   # AI 서비스 엔진
├── pyproject.toml       # Poetry 의존성
├── .env                # 환경 변수
└── README.md           # 프로젝트 문서
```

## 🔧 설정 옵션

### 환경 변수

```bash
# 필수
OPENAI_API_KEY=your_openai_api_key

# 선택적
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://user:pass@localhost/db
```

## 🌟 주요 특징

### 🎯 **프롬프트 엔지니어링 혁신**
- 다단계 프롬프트 체이닝
- 역할 기반 AI 페르소나 활용
- 컨텍스트 인식 개인화

### 💡 **실용적 차별화**
- 실제 채용공고 패턴 분석 반영
- 회사별/직급별 면접 스타일 구분
- 측정 가능한 학습 마일스톤

### ⚡ **성능 최적화**
- 분석 결과 캐싱으로 빠른 응답
- 비동기 처리 지원
- 확장 가능한 모듈 구조

## 🧪 테스트

```bash
# 단위 테스트 실행
poetry run python manage.py test

# API 헬스체크
curl http://localhost:8000/api/health
```

## 📈 향후 개발 계획

- [ ] 사용자 피드백 기반 AI 모델 개선
- [ ] 실시간 면접 시뮬레이션 기능
- [ ] 채용공고 크롤링 및 매칭 시스템
- [ ] 모바일 앱 지원
- [ ] 다국어 지원

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 문의

프로젝트에 대한 문의사항이나 제안이 있으시면 이슈를 생성해주세요.

---

**🎯 AI Challenge 출품작 - 개인 맞춤형 커리어 코치 챗봇**
