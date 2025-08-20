"""
🎯 API 스키마 정의 (Pydantic)
Django Ninja에서 사용할 요청/응답 스키마
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
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
        description="현재 또는 희망 직무",
        example="Spring Boot/MSA 기반 E-commerce 백엔드 개발"
    )
    
    technical_skills: str = Field(
        ...,
        min_length=5,
        max_length=300,
        description="보유 기술 스킬 (쉼표로 구분)",
        example="Python, Django, Spring Boot, Java, AWS EC2/RDS, Docker, Kubernetes, MySQL, Redis, Git, Jenkins"
    )
    
    experience_years: int = Field(
        ...,
        ge=0,
        le=50,
        description="총 경력 연수",
        example=3
    )

    class Config:
        schema_extra = {
            "example": {
                "career_summary": "3년차 백엔드 개발자로 Spring Boot/MSA 기반 E-commerce 플랫폼 개발 경험. 월 100만 주문 처리 시스템 설계 및 운영, 팀 리딩 경험 보유. AWS 클라우드 인프라 구축 및 Docker/Kubernetes 기반 CI/CD 파이프라인 구축 경험.",
                "job_role": "Spring Boot/MSA 기반 E-commerce 백엔드 개발",
                "technical_skills": "Python, Django, Spring Boot, Java, AWS EC2/RDS, Docker, Kubernetes, MySQL, Redis, Git, Jenkins, JPA/Hibernate, RESTful API",
                "experience_years": 3
            }
        }

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
    
    profile_id: str = Field(..., description="이력서 프로필 ID (UUID 형식)", example="9b63e33b-d5b7-4a98-b2b1-ff7201d6b757")
    target_company_type: CompanyType = Field(
        CompanyType.STARTUP,
        description="목표 회사 유형 (startup: 스타트업, midsize: 중견기업, large: 대기업, foreign: 외국계)",
        example="startup"
    )
    target_position_level: PositionLevel = Field(
        PositionLevel.JUNIOR,
        description="목표 포지션 레벨 (junior: 주니어, mid: 미드레벨, senior: 시니어, lead: 리드)",
        example="mid"
    )

    class Config:
        schema_extra = {
            "example": {
                "profile_id": "9b63e33b-d5b7-4a98-b2b1-ff7201d6b757",
                "target_company_type": "startup",
                "target_position_level": "mid"
            }
        }


class LearningPathCreateRequest(BaseModel):
    """학습 경로 생성 요청"""
    
    profile_id: str = Field(..., description="이력서 프로필 ID (UUID 형식)", example="9b63e33b-d5b7-4a98-b2b1-ff7201d6b757")
    target_goal: LearningGoal = Field(
        LearningGoal.SKILL_ENHANCEMENT,
        description="학습 목표 (skill_enhancement: 기술 향상, career_change: 커리어 전환, promotion: 승진, interview_prep: 면접 준비)",
        example="skill_enhancement"
    )
    preferred_duration_months: Optional[int] = Field(
        3,
        ge=1,
        le=24,
        description="선호하는 학습 기간(개월) - 1~24개월 범위",
        example=3
    )

    class Config:
        schema_extra = {
            "example": {
                "profile_id": "9b63e33b-d5b7-4a98-b2b1-ff7201d6b757",
                "target_goal": "skill_enhancement",
                "preferred_duration_months": 3
            }
        }


# === 응답 스키마 ===

class ResumeAnalysisResult(BaseModel):
    """이력서 분석 결과"""
    
    career_level: str = Field(..., description="커리어 레벨", example="중급 개발자 (3년차)")
    strength_areas: List[str] = Field(..., description="강점 영역", example=["Spring Boot 기반 MSA 설계 경험", "대용량 트래픽 처리 노하우", "팀 리딩 및 협업 역량"])
    improvement_areas: List[str] = Field(..., description="개선 필요 영역", example=["프론트엔드 기술 스택 확장", "클라우드 네이티브 아키텍처 심화", "데이터베이스 최적화 전문성"])
    career_pattern: str = Field(..., description="커리어 패턴 분석", example="기술적 깊이와 실무 경험이 균형있게 발전하고 있는 성장형 개발자. 팀워크와 문제해결 능력이 뛰어나며, 지속적인 학습 의지가 강함.")
    market_competitiveness: int = Field(..., ge=1, le=10, description="시장 경쟁력 점수 (1-10)", example=7)


class InterviewQuestion(BaseModel):
    """면접 질문"""
    
    question: str = Field(..., description="면접 질문", example="Spring Boot로 개발한 E-commerce 시스템에서 월 1천만 건의 트래픽을 처리하면서 겪었던 가장 큰 기술적 도전은 무엇이었고, 어떤 방식으로 해결하셨나요?")
    category: str = Field(..., description="질문 카테고리", example="기술 전문성 & 실무 경험")
    difficulty_level: str = Field(..., description="난이도", example="고급")
    suggested_answer_approach: str = Field(..., description="답변 접근 방향", example="문제 상황 설명 → 기술적 분석 → 해결 과정 → 결과 및 학습 순서로 구조화하여 답변하세요.")


class LearningStep(BaseModel):
    """학습 단계"""
    
    phase: str = Field(..., description="학습 단계명", example="1단계: 기술 전문성 심화")
    duration_weeks: int = Field(..., description="예상 소요 기간(주)", example=4)
    objectives: List[str] = Field(..., description="학습 목표", example=["현재 주력 기술 스택의 고급 기능 마스터", "성능 최적화 및 아키텍처 설계 능력 향상", "실전 프로젝트 1개 완성 (포트폴리오용)"])
    resources: List[str] = Field(..., description="추천 학습 자료", example=["Spring Boot 공식 문서 심화 학습", "클린 아키텍처 서적", "GitHub 오픈소스 프로젝트 분석"])
    milestones: List[str] = Field(..., description="마일스톤", example=["복잡한 비즈니스 로직을 포함한 개인 프로젝트 완성", "기술 블로그 포스팅 3회 이상", "코드 품질 측정 도구로 80% 이상 달성"])


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
