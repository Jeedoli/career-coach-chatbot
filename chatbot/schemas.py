"""
🎯 API 스키마 정의 (Pydantic)
Django Ninja에서 사용할 요청/응답 스키마
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class CompanyType(str, Enum):
    """회사 유형"""
    STARTUP = "startup"
    MIDSIZE = "midsize" 
    LARGE = "large"
    FOREIGN = "foreign"


class PositionLevel(str, Enum):
    """포지션 레벨"""
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"


class LearningGoal(str, Enum):
    """학습 목표"""
    SKILL_ENHANCEMENT = "skill_enhancement"
    CAREER_CHANGE = "career_change"
    PROMOTION = "promotion"
    INTERVIEW_PREP = "interview_prep"


# === 요청 스키마 ===

class ResumeProfileCreateRequest(BaseModel):
    """이력서 프로필 생성 요청"""
    
    career_summary: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="경력 요약 (예: 3년차 백엔드 개발자, Spring Boot/MSA/Python 기반 커머스 서비스 개발)",
        example="3년차 백엔드 개발자, Spring Boot/MSA/Python 기반 커머스 서비스 개발, AWS EC2 운영 경험"
    )
    
    job_role: str = Field(
        ...,
        min_length=5,
        max_length=100,
        description="수행 직무",
        example="Spring Boot/MSA 기반 커머스 서비스 개발"
    )
    
    technical_skills: str = Field(
        ...,
        min_length=5,
        max_length=300,
        description="보유 기술 스킬 리스트",
        example="Python, Django, Spring Boot, AWS EC2, Docker, MySQL, Redis"
    )
    
    experience_years: int = Field(
        ...,
        ge=0,
        le=50,
        description="총 경력 연수",
        example=3
    )

    @validator('career_summary')
    def validate_career_summary(cls, v):
        if not v.strip():
            raise ValueError('경력 요약은 비워둘 수 없습니다')
        return v.strip()

    @validator('technical_skills')
    def validate_technical_skills(cls, v):
        skills = [skill.strip() for skill in v.split(',')]
        if len(skills) < 2:
            raise ValueError('최소 2개 이상의 기술 스킬을 입력해주세요')
        return v.strip()


class InterviewSessionCreateRequest(BaseModel):
    """면접 세션 생성 요청"""
    
    profile_id: str = Field(..., description="이력서 프로필 ID")
    target_company_type: CompanyType = Field(
        CompanyType.STARTUP,
        description="목표 회사 유형"
    )
    target_position_level: PositionLevel = Field(
        PositionLevel.JUNIOR,
        description="목표 포지션 레벨"
    )


class LearningPathCreateRequest(BaseModel):
    """학습 경로 생성 요청"""
    
    profile_id: str = Field(..., description="이력서 프로필 ID")
    target_goal: LearningGoal = Field(
        LearningGoal.SKILL_ENHANCEMENT,
        description="학습 목표"
    )
    preferred_duration_months: Optional[int] = Field(
        3,
        ge=1,
        le=24,
        description="선호하는 학습 기간(개월)"
    )


# === 응답 스키마 ===

class ResumeAnalysisResult(BaseModel):
    """이력서 분석 결과"""
    
    career_level: str = Field(..., description="커리어 레벨 (신입/주니어/시니어 등)")
    strength_areas: List[str] = Field(..., description="강점 영역")
    improvement_areas: List[str] = Field(..., description="개선 필요 영역")
    career_pattern: str = Field(..., description="커리어 패턴 분석")
    market_competitiveness: int = Field(..., ge=1, le=10, description="시장 경쟁력 점수 (1-10)")


class InterviewQuestion(BaseModel):
    """면접 질문"""
    
    question: str = Field(..., description="면접 질문")
    category: str = Field(..., description="질문 카테고리 (기술/경험/인성 등)")
    difficulty_level: str = Field(..., description="난이도 (기본/중급/고급)")
    suggested_answer_approach: str = Field(..., description="답변 접근 방향")


class LearningStep(BaseModel):
    """학습 단계"""
    
    phase: str = Field(..., description="학습 단계명")
    duration_weeks: int = Field(..., description="예상 소요 기간(주)")
    objectives: List[str] = Field(..., description="학습 목표")
    resources: List[str] = Field(..., description="추천 학습 자료")
    milestones: List[str] = Field(..., description="마일스톤")


class ResumeProfileResponse(BaseModel):
    """이력서 프로필 응답"""
    
    id: str
    career_summary: str
    job_role: str
    technical_skills: str
    experience_years: int
    created_at: datetime
    analysis_result: Optional[ResumeAnalysisResult] = None


class InterviewSessionResponse(BaseModel):
    """면접 세션 응답"""
    
    id: str
    profile_id: str
    target_company_type: str
    target_position_level: str
    questions: List[InterviewQuestion]
    created_at: datetime
    generation_metadata: Dict[str, Any]


class LearningPathResponse(BaseModel):
    """학습 경로 응답"""
    
    id: str
    profile_id: str
    target_goal: str
    learning_roadmap: List[LearningStep]
    estimated_duration_months: int
    created_at: datetime
    generation_metadata: Dict[str, Any]


# === 에러 응답 ===

class ErrorResponse(BaseModel):
    """에러 응답"""
    
    error: str = Field(..., description="에러 메시지")
    details: Optional[Dict[str, Any]] = None


# === 성공 응답 ===

class SuccessResponse(BaseModel):
    """성공 응답"""
    
    message: str = Field(..., description="성공 메시지")
    data: Optional[Dict[str, Any]] = None
