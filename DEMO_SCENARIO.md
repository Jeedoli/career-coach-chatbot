# 🎬 커리어 코치 챗봇 API 데모 시나리오

## 🎯 **실제 사용 시나리오: "김개발"의 이력서 분석부터 면접 준비까지**

### 👤 **테스트 페르소나: 김개발 (3년차 백엔드 개발자)**
- **경력**: 3년차 백엔드 개발자
- **경험**: Spring Boot, 커머스 서비스 개발
- **목표**: 스타트업 시니어 개발자 전향
- **고민**: 면접 준비 + 스킬 업그레이드

## 🔄 **Step-by-Step 데모**

### 1️⃣ **프로필 생성 및 AI 분석**

**요청:**
```bash
curl -X POST "http://localhost:8000/api/profiles" \
  -H "Content-Type: application/json" \
  -d '{
    "career_summary": "3년차 백엔드 개발자, Spring Boot/JPA 기반 이커머스 플랫폼 개발, 월 1000만 PV 서비스 운영 경험, MSA 전환 프로젝트 리드",
    "job_role": "Spring Boot 기반 이커머스 API 서버 개발 및 MSA 아키텍처 설계",
    "technical_skills": "Java, Spring Boot, JPA, MySQL, Redis, Docker, AWS EC2, Jenkins, Git",
    "experience_years": 3
  }'
```

**AI 분석 결과 (예상):**
```json
{
  "id": "abcd-1234-efgh-5678",
  "analysis_result": {
    "career_level": "주니어-미드 전환기",
    "strength_areas": [
      "실무 중심의 백엔드 개발 경험",
      "대용량 트래픽 처리 경험",
      "MSA 아키텍처 이해도",
      "DevOps 도구 활용 능력"
    ],
    "improvement_areas": [
      "프론트엔드 기술 이해 부족",
      "팀 리딩 경험 부족",
      "최신 클라우드 서비스 활용도",
      "테스트 코드 작성 습관"
    ],
    "career_pattern": "실무 중심의 꾸준한 성장형. 기술적 깊이는 있으나 폭넓은 경험 필요",
    "market_competitiveness": 7
  }
}
```

### 2️⃣ **스타트업 면접 질문 생성**

**요청:**
```bash
curl -X POST "http://localhost:8000/api/interview-sessions" \
  -H "Content-Type: application/json" \
  -d '{
    "profile_id": "abcd-1234-efgh-5678",
    "target_company_type": "startup",
    "target_position_level": "mid"
  }'
```

**생성된 맞춤 면접 질문 (예상):**
```json
{
  "questions": [
    {
      "question": "월 1000만 PV를 처리하면서 가장 큰 성능 이슈는 무엇이었고, 어떻게 해결했나요? 특히 데이터베이스 최적화 관점에서 설명해주세요.",
      "category": "기술적 깊이",
      "difficulty_level": "중급",
      "suggested_answer_approach": "구체적인 성능 지표와 해결 과정, 데이터베이스 쿼리 최적화 경험 중심으로 답변"
    },
    {
      "question": "MSA 전환 프로젝트를 리드하셨다고 하는데, 모놀리식에서 MSA로 전환할 때 가장 어려웠던 점과 팀원들을 어떻게 설득했는지 말씀해주세요.",
      "category": "리더십/문제해결",
      "difficulty_level": "고급",
      "suggested_answer_approach": "기술적 도전과 팀 관리, 의사결정 과정을 균형있게 설명"
    },
    {
      "question": "스타트업에서는 빠른 개발과 안정성을 동시에 추구해야 합니다. 개발 속도와 코드 품질 사이에서 어떤 기준으로 균형을 맞추시나요?",
      "category": "스타트업 적합성",
      "difficulty_level": "중급",
      "suggested_answer_approach": "실무 경험 기반으로 스타트업 환경에 대한 이해도 어필"
    },
    {
      "question": "현재 사용하고 있는 Jenkins 기반 CI/CD에서 개선하고 싶은 부분이 있다면 무엇인가요? GitHub Actions나 다른 도구로의 전환을 고려해본 적이 있나요?",
      "category": "DevOps/기술 트렌드",
      "difficulty_level": "중급",
      "suggested_answer_approach": "현재 도구의 한계점과 최신 트렌드에 대한 관심도 표현"
    },
    {
      "question": "만약 우리 회사에 입사한다면, 첫 3개월 동안 어떤 목표를 세우고 어떻게 팀에 기여할 계획인가요?",
      "category": "동기/성장 계획",
      "difficulty_level": "기본",
      "suggested_answer_approach": "구체적이고 현실적인 계획과 팀워크 강조"
    }
  ]
}
```

### 3️⃣ **개인 맞춤형 학습 경로 생성**

**요청:**
```bash
curl -X POST "http://localhost:8000/api/learning-paths" \
  -H "Content-Type: application/json" \
  -d '{
    "profile_id": "abcd-1234-efgh-5678",
    "target_goal": "promotion",
    "preferred_duration_months": 4
  }'
```

**생성된 학습 로드맵 (예상):**
```json
{
  "learning_roadmap": [
    {
      "phase": "1단계: 시니어 개발자 역량 강화",
      "duration_weeks": 6,
      "objectives": [
        "클린 아키텍처 설계 패턴 습득",
        "테스트 주도 개발(TDD) 실습",
        "코드 리뷰 및 멘토링 스킬 개발"
      ],
      "resources": [
        "클린 아키텍처 (로버트 마틴 저서)",
        "실전 테스트 주도 개발 온라인 강의",
        "GitHub 오픈소스 프로젝트 코드 리뷰 참여"
      ],
      "milestones": [
        "개인 프로젝트에 클린 아키텍처 적용",
        "테스트 커버리지 80% 이상 달성"
      ]
    },
    {
      "phase": "2단계: 최신 기술 스택 확장",
      "duration_weeks": 6,
      "objectives": [
        "Kubernetes 기반 컨테이너 오케스트레이션",
        "React 기본기 습득 (풀스택 역량)",
        "모니터링 및 로깅 시스템 구축"
      ],
      "resources": [
        "쿠버네티스 완벽 가이드",
        "React 공식 문서 및 실습 프로젝트",
        "Prometheus + Grafana 실습"
      ],
      "milestones": [
        "Kubernetes 클러스터 직접 구축",
        "간단한 React 관리자 페이지 개발"
      ]
    },
    {
      "phase": "3단계: 리더십 및 실전 적용",
      "duration_weeks": 4,
      "objectives": [
        "팀 프로젝트 리딩 경험 확보",
        "기술 블로그 운영으로 지식 공유",
        "컨퍼런스 발표 또는 세미나 참여"
      ],
      "resources": [
        "사내 스터디 그룹 리딩",
        "기술 블로그 플랫폼 (Medium, velog)",
        "개발자 컨퍼런스 및 밋업 참여"
      ],
      "milestones": [
        "기술 블로그 월 2회 포스팅",
        "사내 기술 세미나 발표 1회"
      ]
    }
  ],
  "estimated_duration_months": 4
}
```

### 4️⃣ **진행 상황 인사이트 확인**

**요청:**
```bash
curl -X GET "http://localhost:8000/api/profiles/abcd-1234-efgh-5678/insights"
```

**인사이트 결과:**
```json
{
  "data": {
    "profile_summary": {
      "career_level": "주니어-미드 전환기",
      "market_competitiveness": 7,
      "created_sessions": 1,
      "created_learning_paths": 1
    },
    "recommendations": [
      "생성된 면접 질문으로 모의 면접 연습",
      "학습 경로의 1단계부터 체계적 진행",
      "정기적인 학습 진도 체크 및 업데이트"
    ]
  }
}
```

## 🎯 **데모 시나리오의 차별화 포인트**

### 🧠 **AI 분석의 정교함**
- **개인별 특성 파악**: 단순 키워드가 아닌 패턴 분석
- **시장 관점 평가**: 실제 채용 시장에서의 경쟁력 평가
- **성장 궤적 예측**: 향후 발전 가능성과 방향성 제시

### 🎯 **맞춤형 면접 질문**
- **실무 경험 기반**: 이력서의 구체적 경험을 활용한 질문
- **회사 특성 반영**: 스타트업 환경에 맞는 질문 스타일
- **난이도 조절**: 경력 수준에 맞는 적절한 난이도

### 📚 **실현 가능한 학습 계획**
- **단계적 접근**: 현재 수준에서 목표까지의 점진적 계획
- **구체적 자료**: 실제 학습할 수 있는 리소스 제공
- **측정 가능한 목표**: 명확한 성과 지표와 마일스톤

## 🚀 **직접 체험해보기**

1. **OpenAI API 키 설정** 후
2. **서버 실행**: `poetry run python manage.py runserver`
3. **위 시나리오 실행** 또는
4. **테스트 스크립트**: `python test_api.py`

---

**🎉 실제 사용해보면 일반적인 질문 생성기와는 차원이 다른 개인 맞춤형 경험을 느낄 수 있습니다!**
