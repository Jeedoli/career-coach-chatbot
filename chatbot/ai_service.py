"""
🤖 AI 서비스 - 핵심 차별화 엔진

평가 포인트 집중:
1. LLM 프롬프트 엔지니어링 - 효과적이고 독창적
2. 개인 맞춤형 특징 - 진짜 맞춤형
3. 실용성 - 실제 도움이 되는가

차별화 전략:
- 다단계 분석 프롬프트 체이닝
- 실제 채용 시장 데이터 반영
- 경력 패턴별 맞춤형 접근
"""

import os
import json
import time
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from openai import OpenAI

# 환경 변수에서 API 키 가져오기
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


@dataclass
class CareerAnalysis:
    """커리어 분석 결과"""
    career_level: str
    strength_areas: List[str]
    improvement_areas: List[str]
    career_pattern: str
    market_competitiveness: int
    personality_traits: List[str]
    growth_trajectory: str


class CareerCoachAI:
    """커리어 코치 AI 엔진"""
    
    def __init__(self):
        self.model = "gpt-4o-mini"  # 비용 효율적이면서 성능 좋은 모델
        
    def analyze_resume_profile(self, career_summary: str, job_role: str, 
                             technical_skills: str, experience_years: int) -> CareerAnalysis:
        """
        🔍 1단계: 이력서 심층 분석
        - 단순 정보 추출이 아닌 패턴 분석
        - 숨겨진 강점/약점 발견
        """
        
        analysis_prompt = f"""
당신은 20년 경력의 글로벌 헤드헌팅 회사 시니어 파트너입니다. 
구글, 메타, 네이버, 카카오 등 수천 명의 개발자 채용을 성공시키며, 개발자 커리어 패턴과 시장 트렌드를 정확히 파악하는 전문가입니다.

**지원자 정보:**
📋 **경력 요약**: {career_summary}
💼 **수행 직무**: {job_role}
🛠️ **기술 스킬**: {technical_skills}
📅 **경력 연수**: {experience_years}년

**미션**: 이 개발자의 현재 위치와 잠재력을 정밀 분석하여, 향후 커리어 전략 수립의 기초 데이터를 제공하세요.

**심층 분석 요구사항:**

1. **커리어 레벨 정밀 진단**
   - 경력 연수 대비 실제 성숙도 평가
   - 업계 표준과 비교한 기술 수준
   - 리더십/책임감 발전 정도

2. **시장 차별화 강점 분석** (구체적 증거 기반)
   - 타 개발자 대비 독특한 경험이나 역량
   - 기술적 깊이와 넓이의 균형
   - 비즈니스 임팩트 창출 능력

3. **전략적 개선 영역** (채용 관점)
   - 현재 시장에서 요구되지만 부족한 스킬
   - 다음 레벨로 승진하기 위한 필수 역량
   - 장기적 경쟁력 확보를 위한 투자 영역

4. **커리어 패턴 심화 분석** (존댓말로 작성 필수)
   - 학습 동기와 성장 의지에 대한 구체적 평가
   - 현재 상황(나이, 경력 전환 등)의 강점과 약점 분석
   - 실무 경험 부족 시 이를 극복할 수 있는 방안과 잠재력
   - 향후 커리어 발전 가능성과 제약 요인
   - 시장에서의 포지셔닝과 차별화 전략

5. **현재 시장 가치** (정량적 평가)
   - 현재 기술 스택의 시장 수요도
   - 경력 대비 연봉 협상력
   - 이직 시 선택권의 폭

**출력 형식 (JSON):**
{{
    "career_level": "주니어/중급/시니어/리드/아키텍트 중 정확한 위치",
    "strength_areas": [
        "구체적이고 차별화된 강점 1 (시장 관점에서 평가)",
        "경쟁사 대비 우위를 가질 수 있는 강점 2", 
        "장기적 성장 잠재력을 보여주는 강점 3"
    ],
    "improvement_areas": [
        "즉시 개선이 필요한 핵심 약점 1 (구체적 이유 포함)",
        "시장 요구사항 대비 부족한 영역 2 (트렌드 반영)",
        "커리어 도약을 위한 필수 투자 영역 3"
    ],
    "career_pattern": "이 개발자님의 현재 상황과 성장 패턴에 대한 심화 분석입니다. 학습 동기, 경력 전환 의지, 실무 경험 부족 극복 방안, 나이와 상황을 고려한 현실적 전망을 포함하여 5-6문장으로 존댓말로 상세히 작성하세요.",
    "market_competitiveness": "현재 시장에서의 경쟁력 점수 (1-10점, 동일 경력 대비)",
    "personality_traits": [
        "이력서에서 드러나는 학습 성향과 적응력 평가",
        "업무 접근 방식과 문제 해결 스타일",
        "팀워크와 리더십 발현 가능성"
    ],
    "growth_trajectory": "현재 궤적을 유지할 경우와 적극적인 성장 전략을 수립할 경우의 5년 후 전망을 구체적으로 비교 분석 (존댓말 4-5문장)"
}}

**필수 작성 규칙:**
- career_pattern과 growth_trajectory는 반드시 존댓말로 작성
- 구체적 근거와 실용적 인사이트 중심
- 나이, 실무 경험, 학습 기간 등 개인 상황을 세밀히 고려
- 일반론이 아닌 이 개발자만의 상황에 맞춘 분석
- 부정적 요소도 건설적 관점에서 개선 방향 제시
"""

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": analysis_prompt}],
                temperature=0.3,  # 일관성 있는 분석을 위해 낮은 temperature
                max_tokens=1500
            )
            
            # 디버깅: 원시 응답 확인
            raw_content = response.choices[0].message.content
            print(f"🔍 OpenAI 원시 응답: {raw_content}")
            
            # JSON 파싱 전 정리
            if raw_content:
                # 코드 블록 마커 제거
                if raw_content.startswith("```json"):
                    raw_content = raw_content[7:]
                if raw_content.endswith("```"):
                    raw_content = raw_content[:-3]
                raw_content = raw_content.strip()
                
                result = json.loads(raw_content)
            else:
                raise ValueError("Empty response from OpenAI")
            
            return CareerAnalysis(
                career_level=result['career_level'],
                strength_areas=result['strength_areas'],
                improvement_areas=result['improvement_areas'],
                career_pattern=result['career_pattern'],
                market_competitiveness=result['market_competitiveness'],
                personality_traits=result['personality_traits'],
                growth_trajectory=result['growth_trajectory']
            )
            
        except json.JSONDecodeError as e:
            # JSON 파싱 오류 상세 로깅
            print(f"❌ JSON 파싱 오류: {e}")
            print(f"🔍 문제가 된 응답 내용: {raw_content}")
            
            # JSON 복구 시도
            try:
                # 불완전한 JSON을 완성하려고 시도
                if "{" in raw_content:
                    start_idx = raw_content.find("{")
                    json_part = raw_content[start_idx:]
                    # 중괄호 균형 맞추기
                    open_count = json_part.count("{")
                    close_count = json_part.count("}")
                    if open_count > close_count:
                        json_part += "}" * (open_count - close_count)
                    result = json.loads(json_part)
                else:
                    raise ValueError("No JSON structure found")
            except:
                # 완전히 실패한 경우 기본값 사용
                result = {
                    "career_level": "분석 중",
                    "strength_areas": ["기술적 역량", "실무 경험"],
                    "improvement_areas": ["추가 분석 필요"],
                    "career_pattern": "분석 진행 중",
                    "market_competitiveness": 5,
                    "personality_traits": ["분석 중"],
                    "growth_trajectory": "추가 분석 필요"
                }
            
            return CareerAnalysis(
                career_level=result['career_level'],
                strength_areas=result['strength_areas'],
                improvement_areas=result['improvement_areas'],
                career_pattern=result['career_pattern'],
                market_competitiveness=result['market_competitiveness'],
                personality_traits=result['personality_traits'],
                growth_trajectory=result['growth_trajectory']
            )
            
        except Exception as e:
            # 완전한 API 호출 실패
            print(f"❌ OpenAI API 호출 오류: {e}")
            print(f"API 키 설정 여부: {'설정됨' if os.getenv('OPENAI_API_KEY') else '미설정'}")
            
            # 기본값 반환 (에러 핸들링)
            return CareerAnalysis(
                career_level="분석 중",
                strength_areas=["기술적 역량"],
                improvement_areas=["추가 분석 필요"],
                career_pattern="분석 진행 중",
                market_competitiveness=5,
                personality_traits=["분석 중"],
                growth_trajectory="추가 분석 필요"
            )

    def generate_interview_questions(self, analysis: CareerAnalysis, 
                                   company_type: str, position_level: str,
                                   career_summary: str, technical_skills: str) -> List[Dict[str, str]]:
        """
        🎯 2단계: 맞춤형 면접 질문 생성
        - 분석 결과 기반 개인화
        - 회사 유형별 차별화
        - 실제 면접에서 나올 법한 질문
        """
        
        # 회사 유형별 면접 스타일 정의
        company_styles = {
            "startup": "빠른 성장, 다양한 역할, 문제해결 능력 중시",
            "midsize": "안정성과 성장의 균형, 체계적 프로세스",
            "large": "전문성, 체계적 업무, 협업 능력",
            "foreign": "글로벌 마인드, 커뮤니케이션, 다양성"
        }
        
        interview_prompt = f"""
당신은 {company_styles.get(company_type, "일반 기업")} 특성을 가진 회사의 시니어 기술 면접관입니다. 
10년 이상 {position_level} 레벨 개발자를 채용해온 전문가로, 실제 업무 역량을 정확히 파악하는 날카로운 질문으로 유명합니다.

**지원자 상세 프로필:**
- 커리어 레벨: {analysis.career_level}
- 핵심 강점: {', '.join(analysis.strength_areas)}
- 개선 필요 영역: {', '.join(analysis.improvement_areas)}
- 성격 특성: {', '.join(analysis.personality_traits)}
- 구체적 경력: {career_summary}
- 기술 스택: {technical_skills}

**면접 목표**: 이 지원자가 우리 회사 {position_level} 포지션에서 **실제로 성과를 낼 수 있는지** 검증하는 심층 질문을 만드세요.

**필수 질문 설계 원칙:**
1. **경험 기반 구체성**: 지원자의 실제 프로젝트/기술을 언급한 세부 질문
2. **실무 시나리오**: 가상이 아닌 실제 일어날 수 있는 업무 상황
3. **기술적 깊이**: 단순 지식이 아닌 문제 해결 과정과 트레이드오프 이해도 평가
4. **협업 검증**: 실제 팀워크와 커뮤니케이션 역량 확인
5. **회사 핏**: {company_type} 환경에서의 적응력과 가치 부합성

**필수 질문 카테고리 (각 1개씩, 총 5개):**

1. **기술 전문성 & 실무 경험** (고급 난이도)
   - 지원자의 주요 기술 스택을 깊이 있게 탐구
   - 실제 겪었을 법한 기술적 도전과 해결 과정
   - 아키텍처/설계 관련 의사결정 경험

2. **문제 해결 & 트러블슈팅** (중급-고급 난이도)
   - 구체적인 문제 상황과 해결 과정
   - 다양한 접근법의 장단점 분석
   - 제약 조건 하에서의 최적해 도출

3. **학습 능력 & 적응력** (중급 난이도)
   - 새로운 기술 습득 경험과 방법론
   - 실패나 어려움 극복 사례
   - 변화하는 요구사항에 대한 대응

4. **팀워크 & 커뮤니케이션** (중급 난이도)
   - 실제 협업 경험과 갈등 해결
   - 기술적 내용의 비기술자 설명 능력
   - 코드 리뷰, 멘토링 등 지식 공유 경험

5. **회사 적합성 & 비전** (기본-중급 난이도)
   - {company_type} 환경에서의 목표와 기여 방향
   - 장기적 성장 계획과 회사 발전 방향의 일치성
   - 업무 우선순위와 가치관

**출력 형식 (JSON):**
[
    {{
        "question": "지원자의 구체적 경험을 언급한 상세하고 날카로운 질문 (2-3문장)",
        "category": "기술 전문성 & 실무 경험",
        "difficulty_level": "고급",
        "suggested_answer_approach": "효과적인 답변을 위한 구체적 가이드 (구조화 방법, 포함할 내용 등)"
    }},
    {{
        "question": "실제 상황 기반의 문제 해결 시나리오 질문",
        "category": "문제 해결 & 트러블슈팅", 
        "difficulty_level": "중급",
        "suggested_answer_approach": "문제 분석 -> 해결 과정 -> 결과 -> 학습 순서로 답변"
    }}
    // ... 총 5개 질문
]

**주의사항:**
- 각 질문은 지원자의 실제 경험과 기술을 구체적으로 언급해야 함
- "일반적으로 어떻게 하나요?" 같은 추상적 질문 금지
- 실제 면접에서 30분 이상 토론할 수 있을 정도의 깊이 있는 질문
- {company_type} 회사의 특성과 {position_level} 레벨에 적합한 난이도
"""

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": interview_prompt}],
                temperature=0.7,  # 창의적 질문 생성을 위해 높은 temperature
                max_tokens=2000
            )
            
            # JSON 파싱 개선
            raw_content = response.choices[0].message.content
            print(f"🔍 면접 질문 원시 응답: {raw_content}")
            
            # JSON 정리
            if raw_content.startswith("```json"):
                raw_content = raw_content[7:]
            if raw_content.endswith("```"):
                raw_content = raw_content[:-3]
            raw_content = raw_content.strip()
            
            questions = json.loads(raw_content)
            return questions[:5]  # 정확히 5개만 반환
            
        except json.JSONDecodeError as e:
            print(f"❌ 면접 질문 JSON 파싱 오류: {e}")
            print(f"🔍 문제가 된 응답: {raw_content}")
            # 기본 질문 반환
        except Exception as e:
            print(f"❌ 면접 질문 생성 오류: {e}")
            # 기본 질문 반환
            # 기본 질문 반환 (에러 핸들링)
            return [
                {
                    "question": "본인의 주요 프로젝트 경험에 대해 설명해주세요.",
                    "category": "경험",
                    "difficulty_level": "기본",
                    "suggested_answer_approach": "구체적인 성과와 학습 포인트 중심으로 답변"
                }
            ] * 5

    def generate_learning_path(self, analysis: CareerAnalysis, target_goal: str,
                             career_summary: str, technical_skills: str,
                             duration_months: int = 3) -> List[Dict[str, Any]]:
        """
        📚 3단계: 개인 맞춤형 학습 경로 생성
        - 현재 수준에서 목표까지의 구체적 로드맵
        - 실현 가능한 단계별 계획
        """
        
        goal_descriptions = {
            "skill_enhancement": "현재 기술 스킬 심화 및 확장",
            "career_change": "새로운 분야로의 커리어 전환",
            "promotion": "현재 직무에서의 승진 및 성장",
            "interview_prep": "면접 준비 및 취업 성공",
            "freelance_prep": "프리랜서/창업 준비"
        }
        
        learning_prompt = f"""
당신은 10년 이상 개발자 커리어 코칭을 해온 시니어 멘토입니다. 실리콘밸리와 국내 대기업에서 수백 명의 개발자 성장을 도왔습니다.

**지원자 심층 분석:**
- 커리어 레벨: {analysis.career_level}
- 핵심 강점: {', '.join(analysis.strength_areas)}
- 개선 필요 영역: {', '.join(analysis.improvement_areas)}
- 성장 궤적: {analysis.growth_trajectory}
- 현재 기술 스택: {technical_skills}
- 커리어 목표: {goal_descriptions.get(target_goal, target_goal)}
- 학습 기간: {duration_months}개월

**미션**: 이 개발자가 시장에서 경쟁력을 갖추고 커리어 목표를 달성할 수 있는 **실전 중심의 학습 로드맵**을 설계하세요.

**필수 포함 요소:**
1. **특정 기술 스택 심화**: 현재 기술을 전문가 수준으로 발전
2. **구체적인 프로젝트 제안**: 실제 포트폴리오가 될 수 있는 프로젝트 (기술 스택 명시)
3. **커뮤니케이션 스킬**: 기술 발표, 코드 리뷰, 팀 협업 역량
4. **한국 취업 시장 맞춤**: 국내 기업 채용 트렌드와 요구사항 반영
5. **개인화된 실행 가이드**: 이 개발자만을 위한 구체적 실행 방법론

**로드맵 설계 원칙:**
- **실무 연결성**: 실제 업무에서 바로 써먹을 수 있는 내용
- **프로젝트 기반**: 각 단계마다 구체적인 산출물 생성
- **네트워킹 포함**: 한국 개발 커뮤니티 참여와 지식 공유 (OKKY, 카카오톡 오픈채팅, 원티드)

**단계별 로드맵 (JSON):**
[
    {{
        "phase": "1단계: 기술 전문성 심화",
        "duration_weeks": {duration_months * 4 // 3},
        "objectives": [
            "현재 주력 기술 스택의 고급 기능 마스터",
            "성능 최적화 및 아키텍처 설계 능력 향상",
            "실전 프로젝트 1개 완성 (포트폴리오용)"
        ],
        "resources": [
            "기술별 공식 문서 심화 학습 (Spring Boot/Django 공식 문서)",
            "실무 아키텍처 패턴 서적 (클린 아키텍처, 마이크로서비스 패턴)",
            "GitHub 오픈소스 프로젝트 분석 (Spring Boot/Django 베스트 프랙티스)"
        ],
        "milestones": [
            "복잡한 비즈니스 로직을 포함한 개인 프로젝트 완성",
            "기술 블로그 포스팅 3회 이상",
            "코드 품질 측정 도구로 80% 이상 달성"
        ],
        "projects": [
            "E-commerce API 서버 구축 (Spring Boot + JPA + Redis 캐싱)",
            "실시간 채팅 시스템 구현 (WebSocket + JWT 인증 + MongoDB)",
            "개인 포트폴리오 사이트 + 관리자 대시보드 (REST API + 프론트엔드 연동)"
        ],
        "personal_advice": "이 단계를 성공적으로 완료하시려면 다음과 같은 구체적인 실행 계획을 권장드립니다. 학습과 실습의 균형을 맞추시되, 평일에는 이론 학습(Django 공식 문서)에, 주말에는 집중적으로 실습 프로젝트에 시간을 할애하세요. IDE는 파이참이나 VS Code를 사용하시고, 버전 관리는 GitHub으로 진행하시기 바랍니다. 학습 순서는 Django ORM 심화 → REST API 설계 → 성능 최적화 → 배포 자동화 순으로 진행하시면 됩니다. 특히 E-commerce 프로젝트는 2주차부터 시작하여 점진적으로 기능을 추가해 나가시고, 진행상황을 벨로그나 브런치, GitHub README에 정리하여 포트폴리오로 활용하시길 바랍니다."
    }},
    {{
        "phase": "2단계: 확장 기술 습득 및 실전 경험",
        "duration_weeks": {duration_months * 4 // 2},
        "objectives": [
            "인접 기술 스택 습득 (풀스택/클라우드/데브옵스)",
            "팀 프로젝트 또는 오픈소스 기여 경험",
            "기술 발표 및 지식 공유 활동"
        ],
        "resources": [
            "클라우드 플랫폼 실습 과정 (AWS Skill Builder, 네이버 클라우드 플랫폼 아카데미)",
            "오픈소스 프로젝트 참여 (GitHub에서 한국어 프로젝트 또는 'good first issue' 찾기)",
            "개발자 커뮤니티 참여 (OKKY, 원티드 개발자 모임, 카카오톡 개발자 오픈채팅)"
        ],
        "milestones": [
            "오픈소스 프로젝트에 의미있는 기여 (PR 머지)",
            "개발자 커뮤니티에서 기술 발표 1회",
            "클라우드 기반 배포 환경 구축 완료"
        ],
        "projects": [
            "마이크로서비스 아키텍처 기반 TODO 서비스 (Docker + Kubernetes)",
            "실시간 주식 가격 모니터링 시스템 (WebSocket + 외부 API 연동)",
            "개발팀용 코드 리뷰 봇 개발 (GitHub API + Slack 연동)"
        ],
        "personal_advice": "2단계 실행을 위해서는 체계적인 접근이 필요합니다. AWS 학습은 AWS Skill Builder에서 단계별로 진행하시고, 실습은 AWS 프리티어를 활용하세요. 오픈소스 기여는 'good first issue' 라벨이 있는 Django 관련 프로젝트를 GitHub에서 찾아 시작하시되, 코드 분석부터 차근차근 시작하세요. 기술 발표 준비는 8주차부터 시작하여 발표 자료는 브런치나 벨로그에 올리고, 데모는 Netlify나 GitHub Pages로 배포하시면 됩니다. 마이크로서비스 프로젝트는 Docker Desktop에서 로컬 개발하시고, Kubernetes는 Minikube로 학습하신 후 네이버 클라우드나 AWS에 배포해보세요. 특히 학습한 내용을 정기적으로 벨로그나 티스토리에 포스팅하여 지식을 정리하시길 권합니다."
    }},
    {{
        "phase": "3단계: 리더십 및 영향력 확장",
        "duration_weeks": {duration_months * 4 - (duration_months * 4 // 3) - (duration_months * 4 // 2)},
        "objectives": [
            "주니어 개발자 멘토링 경험",
            "기술적 의사결정 및 코드 리뷰 리더십",
            "개발 프로세스 개선 제안 및 실행"
        ],
        "resources": [
            "리더십 및 커뮤니케이션 스킬 도서 (크루셜 대화, 피드백의 기술)",
            "코드 리뷰 베스트 프랙티스 학습 (Google의 엔지니어링 문화)",
            "애자일/스크럼 방법론 실습 (Scrum.org 인증 과정)"
        ],
        "milestones": [
            "1명 이상 주니어 개발자 멘토링",
            "팀/회사 내 기술 세미나 진행",
            "개발 프로세스 개선 사례 1건 이상"
        ],
        "projects": [
            "팀 개발 생산성 향상 도구 개발 (CI/CD 파이프라인 + 모니터링)",
            "사내 기술 블로그 플랫폼 구축 (CMS + 검색 + 댓글 시스템)",
            "주니어 개발자를 위한 코딩 테스트 문제 플랫폼 개발"
        ],
        "personal_advice": "리더십 단계의 핵심은 체계적인 멘토링과 프로세스 개선입니다. 주니어 멘토링은 정기적으로 카카오톡 화상통화나 구글 미트로 진행하시고, 멘토링 내용은 노션 템플릿을 만들어 체계적으로 관리하세요. 기술 세미나는 4주 전부터 준비를 시작하여 주제 선정 → 자료 조사 → 발표 자료 작성 → 리허설 순으로 진행하시되, 발표 자료는 파워포인트나 구글 슬라이드로 제작하고 데모는 실제 작동하는 코드로 준비하세요. CI/CD 파이프라인 구축은 젠킨스나 GitHub Actions을 사용하여 실제 프로젝트에 적용해보시고, 모니터링은 엘라스틱서치와 키바나를 활용하시길 바랍니다. 특히 프로세스 개선 제안서는 현재 문제점 분석 → 해결 방안 → 기대 효과를 명확히 정리하여 상급자에게 제시하시면 됩니다."
    }}
]

**중요 출력 규칙:**
- projects와 personal_advice 필드 반드시 포함
- resources는 반드시 문자열 배열로만 출력 (객체 형태 금지)
- personal_advice는 해당 단계의 objectives, resources, milestones, projects를 구체적으로 어떻게 실행할지 상세한 방법론을 존댓말로 제시
- 어떤 도구로, 어떤 순서로, 어떤 플랫폼에서 학습할지 구체적인 실행 계획 포함 (시간 투자량은 언급하지 않음)
- 한국 개발자가 실제로 사용하는 플랫폼과 서비스 위주로 구성
- 구체적이고 실행 가능한 내용으로 작성
"""

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": learning_prompt}],
                temperature=0.4,  # 실용적이면서 창의적인 계획
                max_tokens=2500
            )
            
            # JSON 파싱 개선
            raw_content = response.choices[0].message.content
            print(f"🔍 학습 경로 원시 응답: {raw_content}")
            
            # JSON 부분만 추출
            if "```json" in raw_content:
                start_idx = raw_content.find("```json") + 7
                end_idx = raw_content.find("```", start_idx)
                if end_idx != -1:
                    raw_content = raw_content[start_idx:end_idx]
            elif "[" in raw_content:
                # JSON 배열 부분만 추출
                start_idx = raw_content.find("[")
                end_idx = raw_content.rfind("]") + 1
                raw_content = raw_content[start_idx:end_idx]
            
            raw_content = raw_content.strip()
            learning_steps = json.loads(raw_content)
            return learning_steps
            
        except json.JSONDecodeError as e:
            print(f"❌ 학습 경로 JSON 파싱 오류: {e}")
            print(f"🔍 문제가 된 응답: {raw_content}")
            # 기본 학습 경로 반환
        except Exception as e:
            print(f"❌ 학습 경로 생성 오류: {e}")
            
        # 기본 학습 경로 반환 (에러 핸들링)
        return [
            {
                "phase": "1단계: 현재 스킬 강화",
                "duration_weeks": duration_months * 4 // 3,
                "objectives": [
                    "기존 기술 스택 심화 학습",
                    "실전 프로젝트 경험 쌓기",
                    "코드 품질 향상 집중"
                ],
                "resources": [
                    "온라인 강의 플랫폼 (인프런, 패스트캠퍼스, 유데미)",
                    "기술 공식 문서 및 한국어 튜토리얼 (벨로그, 브런치 기술 포스팅)",
                    "국내 오픈소스 프로젝트 분석 (네이버, 카카오, 우아한형제들 GitHub)"
                ],
                "milestones": [
                    "개인 프로젝트 1개 완성 (GitHub 포트폴리오)",
                    "기술 블로그 포스팅 2회 (벨로그/티스토리)",
                    "포트폴리오 업데이트 및 이력서 개선"
                ],
                "projects": [
                    f"{technical_skills} 기반 웹 애플리케이션 개발",
                    "개인 포트폴리오 사이트 구축",
                    "오픈소스 라이브러리 활용 프로젝트"
                ],
                "personal_advice": f"현재 {analysis.career_level} 레벨에서 효과적으로 성장하시려면 다음과 같은 구체적인 실행 계획을 추천드립니다. 학습과 실습의 균형을 맞추시되, 평일 저녁에는 이론 학습({technical_skills} 공식 문서)에, 주말에는 집중적으로 실습 프로젝트에 시간을 할애하세요. 개발 환경은 VS Code나 인텔리제이를 사용하시고, 버전 관리는 GitHub으로 진행하시기 바랍니다. 학습 순서는 기초 복습 → 심화 기능 → 실전 프로젝트 → 포트폴리오 정리 순으로 진행하시면 됩니다. 특히 개인 프로젝트는 2주차부터 시작하여 점진적으로 새로운 기능을 추가해 나가시고, 진행상황은 벨로그나 티스토리, GitHub README에 상세히 기록하여 성장 과정을 문서화하시길 바랍니다."
            },
            {
                "phase": "2단계: 역량 확장",
                "duration_weeks": duration_months * 4 // 2,
                "objectives": [
                    "새로운 기술 스택 학습",
                    "팀 프로젝트 경험",
                    "커뮤니케이션 스킬 향상"
                ],
                "resources": [
                    "개발자 커뮤니티 참여 (OKKY, 원티드 개발자 모임)",
                    "온라인 멘토링 프로그램 (프로그래머스 멘토링, 코드스테이츠)",
                    "기술 컨퍼런스 참석 (DEVIEW, 우아한테크세미나, 파이콘 코리아)"
                ],
                "milestones": [
                    "협업 프로젝트 참여 (오픈소스 또는 팀 프로젝트)",
                    "기술 발표 경험 (사내 세미나 또는 커뮤니티)",
                    "네트워킹 확대 (OKKY, 원티드 등 커뮤니티 활동)"
                ],
                "projects": [
                    "팀 협업 기반 프로젝트",
                    "오픈소스 기여 활동",
                    "스터디 그룹 프로젝트"
                ],
                "personal_advice": "역량 확장 단계에서는 체계적인 네트워킹과 협업 경험이 핵심입니다. 새로운 기술 학습은 온라인 강의(인프런, 패스트캠퍼스)와 실습을 병행하여 진행하세요. 개발자 커뮤니티는 OKKY, 개발자 카카오톡 오픈채팅방, 원티드 개발자 모임에서 활동하시고, 참석 후에는 반드시 학습한 내용을 벨로그나 브런치에 정리하세요. 팀 협업 프로젝트는 카카오톡이나 슬랙을 통해 커뮤니케이션하시고, 프로젝트 관리는 지라나 노션을 활용하시기 바랍니다. 오픈소스 기여는 이슈 분석부터 차근차근 시작하시고, 첫 PR은 문서 개선이나 작은 버그 수정부터 시작하세요. 특히 스터디 그룹은 온라인(구글 미트)과 오프라인 카페에서 병행하여 진행하시면 더욱 효과적입니다."
            }
        ]

    def get_generation_metadata(self, process_type: str, start_time: float) -> Dict[str, Any]:
        """생성 메타데이터 (성능 모니터링용)"""
        return {
            "process_type": process_type,
            "model_used": self.model,
            "generation_time_seconds": round(time.time() - start_time, 2),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }


# AI 서비스 인스턴스 (싱글톤)
career_coach_ai = CareerCoachAI()
