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
    title="🤖 커리어 코치 챗봇 API",
    description="이력서 기반 개인 맞춤형 면접 질문 생성 & 학습 경로 추천 시스템",
    version="1.0.0"
)


@api.exception_handler(Exception)
def global_exception_handler(request, exc):
    """글로벌 예외 처리"""
    return JsonResponse({
        "error": "서버 내부 오류가 발생했습니다.",
        "details": str(exc) if hasattr(exc, '__str__') else "알 수 없는 오류"
    }, status=500)


# === 1. 이력서 프로필 관리 ===

@api.post("/profiles", response={201: ResumeProfileResponse, 400: ErrorResponse})
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


@api.get("/profiles/{profile_id}", response={200: ResumeProfileResponse, 404: ErrorResponse})
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

@api.post("/interview-sessions", response={201: InterviewSessionResponse, 400: ErrorResponse})
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

@api.post("/learning-paths", response={201: LearningPathResponse, 400: ErrorResponse})
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

@api.get("/health", response=SuccessResponse)
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

@api.get("/profiles/{profile_id}/insights", response=SuccessResponse)
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
