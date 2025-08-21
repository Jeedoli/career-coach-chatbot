"""
🚀 Django Ninja API 엔드포인트

요구사항 100% 충족:
1. ✅ 이력서 핵심 정보 입력 API
2. ✅ 맞춤 면접 모의 질문 5개 생성 API  
3. ✅ 자기 개발 학습 경로 추천 API

차별화된 API 설계:
- 단계별 프로세스 (프로필 → 분석 → 질문/학습경로)
- 실시간 분석 결과 캐싱
- 확장 가능한 구조
"""

import time
import json
from typing import List
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema
from ninja.responses import Response

from .models import ResumeProfile, InterviewSession, LearningPath
from .schemas import (
    ResumeProfileCreateRequest, ResumeProfileResponse,
    InterviewSessionCreateRequest, InterviewSessionResponse,
    LearningPathCreateRequest, LearningPathResponse,
    ErrorResponse, SuccessResponse,
    ResumeAnalysisResult, InterviewQuestion, LearningStep
)
from .ai_service import career_coach_ai

# API 인스턴스 생성
api = NinjaAPI(
    title="🤖 AI Challenge: 커리어 코치 챗봇 API",
    description="""
    🎯 이력서 기반 개인 맞춤형 커리어 코칭 시스템
    
    👨‍💻 개발자: 이재훈
    📧 이메일: ljhx6787@naver.com  
    🐙 GitHub: https://github.com/Jeedoli
    📁 포트폴리오: https://www.notion.so/Portfolio-Project-562a127538cf4f4483456207bfdacaa9
    
    3단계 AI 분석 프로세스:
    1. 📝 이력서 심층 분석 - 20년 경력 헤드헌터 관점의 정밀 진단
    2. 🎯 맞춤형 면접 질문 5개 - 회사 유형별 실전 질문 생성
    3. 📚 개인화 학습 로드맵 - 기술 심화 + 프로젝트 + 커뮤니케이션 스킬
    
    핵심 차별화:
    - ✨ 다단계 프롬프트 엔지니어링으로 맞춤형 개인화 구현
    - 🏢 회사 유형별 맞춤 면접 스타일 (스타트업/대기업/외국계)
    - 📈 실무 중심 학습 경로 (포트폴리오 프로젝트 포함)
    - 🤖 GPT-4o-mini 기반 비용 효율적 AI 분석
    (좋은 모델 쓸수록 더 좋아지겠죠..!? 우선 비용이 합리적인 모델로 적용했습니다. 마음 껏 테스트 해주세요!)
    
    사용법:
    1. /profiles 로 이력서 정보 입력 및 AI 분석
    2. /interview-sessions 로 맞춤형 면접 질문 생성
    3. /learning-paths 로 개인화된 학습 경로 추천
    """,
    version="1.0.0",
    docs_url="/docs"
)


@api.exception_handler(Exception)
def global_exception_handler(request, exc):
    """글로벌 예외 처리"""
    return JsonResponse({
        "error": "서버 내부 오류가 발생했습니다.",
        "details": str(exc) if hasattr(exc, '__str__') else "알 수 없는 오류"
    }, status=500)


# === 1. 이력서 프로필 관리 ===

@api.post("/profiles", 
          response={201: ResumeProfileResponse, 400: ErrorResponse},
          summary="📝 이력서 프로필 생성 및 AI 분석",
          description="""
          구직자의 이력서 정보를 입력받아 AI가 심층 분석하고 프로필을 생성합니다.
          
          📋 입력 필드:
          
          • career_summary (필수, 최대 1000자)
            - 본인의 주요 경력과 성과를 요약
            - 구체적인 프로젝트 경험, 담당 업무, 성과 포함
            - 예시: "3년차 백엔드 개발자로 Spring Boot/MSA 기반 E-commerce 플랫폼 개발"
          
          • job_role (필수, 최대 200자)
            - 현재 또는 목표하는 구체적인 직무
            - 예시: "Spring Boot/MSA 기반 E-commerce 백엔드 개발"
          
          • technical_skills (필수, 최대 500자)
            - 보유한 기술 스택을 쉼표로 구분하여 나열
            - 예시: "Python, Django, Spring Boot, Java, AWS EC2/RDS, Docker"
          
          • experience_years (필수, 정수)
            - 해당 분야 총 경력 연수 (0~50년)
            - 예시: 3 (3년차), 0 (신입), 5 (5년차)
          
          🤖 AI 분석 결과:
          - career_level: "junior", "mid", "senior", "lead" 중 하나
          - strength_areas: 시장에서 차별화되는 강점 영역 배열
          - improvement_areas: 발전이 필요한 영역 배열  
          - market_competitiveness: 1-10점 경쟁력 점수
          
          ⚡ 처리 시간: 약 5-10초 (OpenAI API 호출 포함)
          """,
          tags=["이력서 분석"])
def create_profile(request, data: ResumeProfileCreateRequest):
    """
    📝 이력서 핵심 정보 입력 API
    
    **기능**: 구직자의 경력, 직무, 기술 스킬 정보를 받아 프로필 생성 및 AI 분석
    """
    try:
        start_time = time.time()
        
        # 1. 프로필 생성
        profile = ResumeProfile.objects.create(
            career_summary=data.career_summary,
            job_role=data.job_role,
            technical_skills=data.technical_skills,
            experience_years=data.experience_years
        )
        
        # 2. AI 분석 실행 (차별화 포인트!)
        analysis = career_coach_ai.analyze_resume_profile(
            career_summary=data.career_summary,
            job_role=data.job_role,
            technical_skills=data.technical_skills,
            experience_years=data.experience_years
        )
        
        # 3. 분석 결과 저장 (캐싱)
        analysis_data = {
            "career_level": analysis.career_level,
            "strength_areas": analysis.strength_areas,
            "improvement_areas": analysis.improvement_areas,
            "career_pattern": analysis.career_pattern,
            "market_competitiveness": analysis.market_competitiveness,
            "personality_traits": analysis.personality_traits,
            "growth_trajectory": analysis.growth_trajectory,
            "analysis_metadata": {
                "generation_time": time.time() - start_time,
                "model_used": "gpt-4o-mini"
            }
        }
        
        profile.analysis_result = analysis_data
        profile.save()
        
        # 4. 응답 반환
        response_data = ResumeProfileResponse(
            id=str(profile.id),
            career_summary=profile.career_summary,
            job_role=profile.job_role,
            technical_skills=profile.technical_skills,
            experience_years=profile.experience_years,
            created_at=profile.created_at,
            analysis_result=ResumeAnalysisResult(**{
                k: v for k, v in analysis_data.items() 
                if k != "analysis_metadata"
            })
        )
        
        return 201, response_data
        
    except Exception as e:
        return 400, ErrorResponse(
            error="프로필 생성 중 오류가 발생했습니다.",
            details={"message": str(e)}
        )


@api.get("/profiles/{profile_id}", 
         response={200: ResumeProfileResponse, 404: ErrorResponse},
         summary="📄 프로필 조회",
         description="""
         생성된 이력서 프로필과 AI 분석 결과를 조회합니다.
         
         📋 URL 파라미터:
         - profile_id (필수): 조회할 프로필의 UUID
         - 예시: /profiles/9b63e33b-d5b7-4a98-b2b1-ff7201d6b757
         
         📊 응답 내용:
         - 입력한 이력서 정보 (career_summary, job_role 등)
         - AI 분석 결과 (강점, 개선점, 시장 경쟁력 등)
         - 생성 일시 및 메타데이터
         """,
         tags=["이력서 분석"])
def get_profile(request, profile_id: str):
    """프로필 조회 API"""
    try:
        profile = get_object_or_404(ResumeProfile, id=profile_id)
        
        analysis_result = None
        if profile.analysis_result:
            analysis_result = ResumeAnalysisResult(**{
                k: v for k, v in profile.analysis_result.items() 
                if k != "analysis_metadata"
            })
        
        response_data = ResumeProfileResponse(
            id=str(profile.id),
            career_summary=profile.career_summary,
            job_role=profile.job_role,
            technical_skills=profile.technical_skills,
            experience_years=profile.experience_years,
            created_at=profile.created_at,
            analysis_result=analysis_result
        )
        
        return response_data
        
    except Exception as e:
        return 404, ErrorResponse(error="프로필을 찾을 수 없습니다.")


# === 2. 면접 질문 생성 ===

@api.post("/interview-sessions", 
          response={201: InterviewSessionResponse, 400: ErrorResponse},
          summary="🎯 맞춤형 면접 질문 5개 생성",
          description="""
          이력서 분석 결과를 바탕으로 회사 유형과 포지션 레벨에 맞는 개인화된 면접 질문 5개를 생성합니다.
          
          📋 입력 필드:
          
          • profile_id (필수, UUID 문자열)
            - 이전에 생성한 프로필의 고유 ID
            - /profiles API 응답에서 받은 id 값 사용
            - 예시: "9b63e33b-d5b7-4a98-b2b1-ff7201d6b757"
          
          • target_company_type (필수)
            회사 유형에 따라 면접 스타일이 달라집니다:
            - "startup": 빠른 성장, 다양한 역할, 문제해결 능력 중시
            - "midsize": 안정성과 성장의 균형, 체계적 프로세스
            - "large": 전문성, 체계적 업무, 협업 능력  
            - "foreign": 글로벌 마인드, 커뮤니케이션, 다양성
          
          • target_position_level (필수)
            지원하려는 포지션 레벨:
            - "junior": 0-2년차, 기초 역량 및 학습 의지 중심
            - "mid": 3-5년차, 실무 경험 및 문제 해결 능력 중심
            - "senior": 6-10년차, 전문성 및 리더십 중심
            - "lead": 10년차+, 아키텍처 설계 및 팀 관리 중심
          
          📊 생성되는 질문 구조:
          - question: 개인 경험을 반영한 구체적 질문
          - category: "기술", "경험", "문제해결", "팀워크", "비전" 중 하나
          - difficulty_level: "기본", "중급", "고급" 중 하나
          - suggested_answer_approach: 효과적인 답변 구조 가이드
          
          ✨ 차별화: "자신의 강점은?"이 아닌 실제 경험 기반 구체적 질문
          """,
          tags=["면접 질문"])
def create_interview_session(request, data: InterviewSessionCreateRequest):
    """
    🎯 맞춤 면접 모의 질문 생성 API
    
    **핵심 차별화**: 
    - 이력서 분석 기반 개인화된 질문
    - 회사 유형별 맞춤형 질문 스타일
    - 실제 면접에서 나올 법한 심층적 질문
    """
    try:
        start_time = time.time()
        
        # 1. 프로필 조회
        profile = get_object_or_404(ResumeProfile, id=data.profile_id)
        
        # 2. 분석 결과 확인
        if not profile.analysis_result:
            return 400, ErrorResponse(
                error="프로필 분석이 완료되지 않았습니다. 먼저 프로필을 생성해주세요."
            )
        
        # 3. AI 분석 객체 복원
        from .ai_service import CareerAnalysis
        analysis_data = profile.analysis_result
        analysis = CareerAnalysis(
            career_level=analysis_data['career_level'],
            strength_areas=analysis_data['strength_areas'],
            improvement_areas=analysis_data['improvement_areas'],
            career_pattern=analysis_data['career_pattern'],
            market_competitiveness=analysis_data['market_competitiveness'],
            personality_traits=analysis_data['personality_traits'],
            growth_trajectory=analysis_data['growth_trajectory']
        )
        
        # 4. 맞춤형 면접 질문 생성 (핵심!)
        questions_data = career_coach_ai.generate_interview_questions(
            analysis=analysis,
            company_type=data.target_company_type,
            position_level=data.target_position_level,
            career_summary=profile.career_summary,
            technical_skills=profile.technical_skills
        )
        
        # 5. 면접 세션 저장
        session = InterviewSession.objects.create(
            profile=profile,
            target_company_type=data.target_company_type,
            target_position_level=data.target_position_level,
            questions=questions_data,
            generation_metadata=career_coach_ai.get_generation_metadata(
                "interview_questions", start_time
            )
        )
        
        # 6. 응답 반환
        questions = [InterviewQuestion(**q) for q in questions_data]
        
        response_data = InterviewSessionResponse(
            id=str(session.id),
            profile_id=str(profile.id),
            target_company_type=session.target_company_type,
            target_position_level=session.target_position_level,
            questions=questions,
            created_at=session.created_at,
            generation_metadata=session.generation_metadata
        )
        
        return 201, response_data
        
    except Exception as e:
        return 400, ErrorResponse(
            error="면접 질문 생성 중 오류가 발생했습니다.",
            details={"message": str(e)}
        )


# === 3. 학습 경로 생성 ===

@api.post("/learning-paths", 
          response={201: LearningPathResponse, 400: ErrorResponse},
          summary="📚 개인화된 학습 경로 추천",
          description="""
          현재 수준 분석을 바탕으로 실전 중심의 3단계 학습 로드맵을 설계합니다.
          
          📋 입력 필드:
          
          • profile_id (필수, UUID 문자열)
            - 이전에 생성한 프로필의 고유 ID
            - /profiles API 응답에서 받은 id 값 사용
            - 예시: "9b63e33b-d5b7-4a98-b2b1-ff7201d6b757"
          
          • target_goal (필수)
            학습 목표에 따라 로드맵 구성이 달라집니다:
            - "skill_enhancement": 현재 기술 스택 심화 및 전문성 강화
            - "career_change": 새로운 기술 분야로 전환 (예: 백엔드→프론트엔드)
            - "promotion": 승진 및 리더십 역량 개발 (시니어→리드)
            - "interview_prep": 면접 및 이직 준비 집중
            - "freelance_prep": 프리랜서/창업 준비
          
          • preferred_duration_months (선택, 정수, 기본값: 3)
            - 학습 계획 기간 (월 단위)
            - 권장 범위: 1-12개월
            - 예시: 3 (3개월), 6 (6개월), 12 (1년)
          
          📅 생성되는 로드맵 구조:
          - phase: 단계명 (예: "1단계: Spring Boot 고급 기능 마스터")
          - duration_weeks: 예상 소요 기간 (주 단위)
          - objectives: 구체적 학습 목표 배열
          - resources: 추천 학습 자료 (책, 강의, 문서)
          - milestones: 측정 가능한 성과 지표
          - projects: 실전 경험을 위한 구체적 프로젝트 제안 (기술 스택 포함)
          - personal_advice: 개인 맞춤형 진심어린 조언 (2-3줄)
          
          ✅ AI Challenge 필수 요소 포함:
          - ⚡ 특정 기술 스택 심화: 현재 기술을 전문가 수준으로 발전
          - 🛠️ 관련 프로젝트 경험: 실제 포트폴리오가 될 수 있는 프로젝트
          - 💬 커뮤니케이션 스킬: 기술 발표, 코드 리뷰, 팀 협업 역량
          - 🎯 개인화 조언: 현재 수준과 목표에 맞는 구체적 실행 방안
          
          🎯 결과: 구체적 학습 자료 + 측정 가능한 마일스톤 + 실행 가능한 프로젝트 + 진심어린 조언
          """,
          tags=["학습 경로"])
def create_learning_path(request, data: LearningPathCreateRequest):
    """
    📚 자기 개발 학습 경로 추천 API
    
    **핵심 차별화**:
    - 현재 수준 분석 기반 맞춤형 로드맵
    - 실현 가능한 단계별 학습 계획
    - 구체적인 학습 자료와 마일스톤 제시
    """
    try:
        start_time = time.time()
        
        # 1. 프로필 조회
        profile = get_object_or_404(ResumeProfile, id=data.profile_id)
        
        # 2. 분석 결과 확인
        if not profile.analysis_result:
            return 400, ErrorResponse(
                error="프로필 분석이 완료되지 않았습니다."
            )
        
        # 3. AI 분석 객체 복원
        from .ai_service import CareerAnalysis
        analysis_data = profile.analysis_result
        analysis = CareerAnalysis(
            career_level=analysis_data['career_level'],
            strength_areas=analysis_data['strength_areas'],
            improvement_areas=analysis_data['improvement_areas'],
            career_pattern=analysis_data['career_pattern'],
            market_competitiveness=analysis_data['market_competitiveness'],
            personality_traits=analysis_data['personality_traits'],
            growth_trajectory=analysis_data['growth_trajectory']
        )
        
        # 4. 개인 맞춤형 학습 경로 생성 (핵심!)
        learning_data = career_coach_ai.generate_learning_path(
            analysis=analysis,
            target_goal=data.target_goal,
            career_summary=profile.career_summary,
            technical_skills=profile.technical_skills,
            duration_months=data.preferred_duration_months or 3
        )
        
        # 5. 학습 경로 저장
        learning_path = LearningPath.objects.create(
            profile=profile,
            target_goal=data.target_goal,
            learning_roadmap=learning_data,
            estimated_duration_months=data.preferred_duration_months or 3,
            generation_metadata=career_coach_ai.get_generation_metadata(
                "learning_path", start_time
            )
        )
        
        # 6. 응답 반환
        learning_steps = [LearningStep(**step) for step in learning_data]
        
        response_data = LearningPathResponse(
            id=str(learning_path.id),
            profile_id=str(profile.id),
            target_goal=learning_path.target_goal,
            learning_roadmap=learning_steps,
            estimated_duration_months=learning_path.estimated_duration_months,
            created_at=learning_path.created_at,
            generation_metadata=learning_path.generation_metadata
        )
        
        return 201, response_data
        
    except Exception as e:
        return 400, ErrorResponse(
            error="학습 경로 생성 중 오류가 발생했습니다.",
            details={"message": str(e)}
        )


# === 4. 헬스체크 ===

@api.get("/health", 
         response=SuccessResponse,
         summary="🩺 API 상태 확인",
         description="""
         API 서버의 상태와 사용 가능한 기능을 확인합니다.
         
         📊 응답 내용:
         - 서버 상태 (healthy/unhealthy)
         - API 버전 정보
         - 사용 가능한 주요 기능 목록
         
         💡 용도: 서버 연결 테스트, 기능 확인
         """,
         tags=["시스템"])
def health_check(request):
    """API 상태 확인"""
    return SuccessResponse(
        message="커리어 코치 챗봇 API가 정상적으로 동작 중입니다! 🚀",
        data={
            "status": "healthy",
            "version": "1.0.0",
            "features": [
                "이력서 분석 및 프로필 생성",
                "맞춤형 면접 질문 생성 (5개)",
                "개인화된 학습 경로 추천"
            ]
        }
    )



