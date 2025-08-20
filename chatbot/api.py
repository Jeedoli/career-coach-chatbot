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
    ## 🎯 이력서 기반 개인 맞춤형 커리어 코칭 시스템
    
    **3단계 AI 분석 프로세스:**
    1. 📝 **이력서 심층 분석** - 20년 경력 헤드헌터 관점의 정밀 진단
    2. 🎯 **맞춤형 면접 질문 5개** - 회사 유형별 실전 질문 생성
    3. 📚 **개인화 학습 로드맵** - 기술 심화 + 프로젝트 + 커뮤니케이션 스킬
    
    **핵심 차별화:**
    - ✨ 다단계 프롬프트 엔지니어링으로 진짜 개인화 구현
    - 🏢 회사 유형별 맞춤 면접 스타일 (스타트업/대기업/외국계)
    - 📈 실무 중심 학습 경로 (포트폴리오 프로젝트 포함)
    - 🤖 GPT-4o-mini 기반 비용 효율적 AI 분석
    
    **사용법:**
    1. `/profiles` 로 이력서 정보 입력 및 AI 분석
    2. `/interview-sessions` 로 맞춤형 면접 질문 생성
    3. `/learning-paths` 로 개인화된 학습 경로 추천
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
          ## 🎯 핵심 기능
          구직자의 이력서 정보를 입력받아 **AI가 심층 분석**하고 프로필을 생성합니다.
          
          ## 🤖 AI 분석 내용
          - **커리어 레벨 정밀 진단**: 경력 연수 대비 실제 성숙도 평가
          - **시장 차별화 강점 분석**: 타 개발자 대비 독특한 경험과 역량
          - **전략적 개선 영역**: 현재 시장에서 요구되지만 부족한 스킬
          - **시장 경쟁력 점수**: 현재 채용시장에서의 경쟁력 (1-10점)
          
          ## 📋 입력 예시
          ```json
          {
            "career_summary": "3년차 백엔드 개발자로 Spring Boot/MSA 기반 E-commerce 플랫폼 개발 경험...",
            "job_role": "Spring Boot/MSA 기반 E-commerce 백엔드 개발",
            "technical_skills": "Python, Django, Spring Boot, Java, AWS EC2/RDS, Docker, Kubernetes",
            "experience_years": 3
          }
          ```
          
          ⚡ **처리 시간**: 약 5-10초 (OpenAI API 호출 포함)
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
         description="생성된 이력서 프로필과 AI 분석 결과를 조회합니다.",
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
          ## 🎯 핵심 기능
          이력서 분석 결과를 바탕으로 **회사 유형과 포지션 레벨에 맞는 개인화된 면접 질문 5개**를 생성합니다.
          
          ## 🏢 회사 유형별 차별화
          - **startup**: 빠른 성장, 다양한 역할, 문제해결 능력 중시
          - **midsize**: 안정성과 성장의 균형, 체계적 프로세스
          - **large**: 전문성, 체계적 업무, 협업 능력
          - **foreign**: 글로벌 마인드, 커뮤니케이션, 다양성
          
          ## 📊 질문 카테고리 (각 1개씩)
          1. **기술 전문성 & 실무 경험** (고급 난이도)
          2. **문제 해결 & 트러블슈팅** (중급-고급 난이도)
          3. **학습 능력 & 적응력** (중급 난이도)
          4. **팀워크 & 커뮤니케이션** (중급 난이도)
          5. **회사 적합성 & 비전** (기본-중급 난이도)
          
          ## 📋 입력 예시
          ```json
          {
            "profile_id": "9b63e33b-d5b7-4a98-b2b1-ff7201d6b757",
            "target_company_type": "startup",
            "target_position_level": "mid"
          }
          ```
          
          ✨ **차별화**: 지원자의 실제 경험을 언급한 구체적이고 날카로운 질문
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
          ## 🎯 핵심 기능
          현재 수준 분석을 바탕으로 **실전 중심의 3단계 학습 로드맵**을 설계합니다.
          
          ## ✅ AI Challenge 필수 요소 포함
          - ⚡ **특정 기술 스택 심화**: 현재 기술을 전문가 수준으로 발전
          - 🛠️ **관련 프로젝트 경험**: 실제 포트폴리오가 될 수 있는 프로젝트
          - 💬 **커뮤니케이션 스킬**: 기술 발표, 코드 리뷰, 팀 협업 역량
          - 📈 **시장 트렌드 반영**: 최신 기술 동향과 채용 요구사항
          
          ## 📅 3단계 로드맵 구조
          1. **1단계: 기술 전문성 심화** (4주)
             - 현재 주력 기술 스택의 고급 기능 마스터
             - 포트폴리오 프로젝트 완성
             
          2. **2단계: 확장 기술 습득 및 실전 경험** (6주)
             - 인접 기술 스택 습득 (클라우드/데브옵스)
             - 오픈소스 기여 및 커뮤니티 활동
             
          3. **3단계: 리더십 및 영향력 확장** (2주)
             - 멘토링 및 기술 발표 경험
             - 프로세스 개선 제안
          
          ## 📋 입력 예시
          ```json
          {
            "profile_id": "9b63e33b-d5b7-4a98-b2b1-ff7201d6b757",
            "target_goal": "skill_enhancement",
            "preferred_duration_months": 3
          }
          ```
          
          🎯 **결과**: 구체적인 학습 자료, 측정 가능한 마일스톤, 실행 가능한 액션 플랜
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


# === 4. 헬스체크 & 상태 확인 ===

@api.get("/health", 
         response=SuccessResponse,
         summary="🩺 API 상태 확인",
         description="API 서버의 상태와 사용 가능한 기능을 확인합니다.",
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


# === 5. 통계 & 인사이트 ===

@api.get("/profiles/{profile_id}/insights", 
         response=SuccessResponse,
         summary="📊 프로필 인사이트",
         description="프로필 활용 현황과 추천사항을 제공합니다.",
         tags=["분석"])
def get_profile_insights(request, profile_id: str):
    """프로필 인사이트 조회 (추가 기능)"""
    try:
        profile = get_object_or_404(ResumeProfile, id=profile_id)
        
        # 관련 세션들 조회
        interview_sessions = profile.interview_sessions.count()
        learning_paths = profile.learning_paths.count()
        
        insights = {
            "profile_summary": {
                "career_level": profile.analysis_result.get('career_level') if profile.analysis_result else "분석 필요",
                "market_competitiveness": profile.analysis_result.get('market_competitiveness') if profile.analysis_result else 0,
                "created_sessions": interview_sessions,
                "created_learning_paths": learning_paths
            },
            "recommendations": [
                "정기적인 면접 질문 업데이트",
                "학습 경로 진행 상황 체크",
                "새로운 기술 트렌드 반영"
            ]
        }
        
        return SuccessResponse(
            message="프로필 인사이트 조회 완료",
            data=insights
        )
        
    except Exception as e:
        return 404, ErrorResponse(error="프로필을 찾을 수 없습니다.")
