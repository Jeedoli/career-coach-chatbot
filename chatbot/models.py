"""
🎯 커리어 코치 챗봇 - 데이터 모델
요구사항:
1. 이력서 핵심 정보 입력
2. 맞춤 면접 모의 질문 5개 생성  
3. 자기 개발 학습 경로 추천

평가 포인트:
- LLM 프롬프트 엔지니어링 효과성 & 독창성
- 개인 맞춤형 특징
- API 설계 견고함 & 확장성
- 실용성
"""

from django.db import models
from django.core.validators import MinLengthValidator
import uuid


class ResumeProfile(models.Model):
    """이력서 기반 프로필 정보"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # 기본 정보
    career_summary = models.TextField(
        verbose_name="경력 요약",
        help_text="예: 3년차 백엔드 개발자",
        validators=[MinLengthValidator(10)]
    )
    
    job_role = models.CharField(
        max_length=100,
        verbose_name="수행 직무",
        help_text="예: Spring Boot/MSA 기반 커머스 서비스 개발"
    )
    
    technical_skills = models.TextField(
        verbose_name="기술 스킬",
        help_text="예: Python, AWS EC2, Docker, MySQL"
    )
    
    experience_years = models.PositiveIntegerField(
        verbose_name="총 경력 연수",
        default=0
    )
    
    # 분석 결과 저장 (캐싱용)
    analysis_result = models.JSONField(
        null=True, 
        blank=True,
        verbose_name="AI 분석 결과"
    )
    
    class Meta:
        db_table = 'resume_profiles'
        verbose_name = '이력서 프로필'
        verbose_name_plural = '이력서 프로필들'
    
    def __str__(self):
        return f"{self.career_summary[:50]}..."


class InterviewSession(models.Model):
    """면접 질문 생성 세션"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(ResumeProfile, on_delete=models.CASCADE, related_name='interview_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 면접 설정
    target_company_type = models.CharField(
        max_length=50,
        choices=[
            ('startup', '스타트업'),
            ('midsize', '중견기업'),
            ('large', '대기업'),
            ('foreign', '외국계'),
        ],
        default='startup'
    )
    
    target_position_level = models.CharField(
        max_length=50,
        choices=[
            ('junior', '주니어'),
            ('mid', '미드레벨'),
            ('senior', '시니어'),
            ('lead', '리드/매니저'),
        ],
        default='junior'
    )
    
    # AI 생성 결과
    questions = models.JSONField(
        verbose_name="생성된 면접 질문들",
        help_text="5개의 맞춤형 면접 질문"
    )
    
    generation_metadata = models.JSONField(
        default=dict,
        verbose_name="생성 메타데이터",
        help_text="프롬프트 정보, 소요시간 등"
    )
    
    class Meta:
        db_table = 'interview_sessions'
        verbose_name = '면접 세션'
        verbose_name_plural = '면접 세션들'
        ordering = ['-created_at']


class LearningPath(models.Model):
    """개인 맞춤형 학습 경로"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(ResumeProfile, on_delete=models.CASCADE, related_name='learning_paths')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 학습 목표
    target_goal = models.CharField(
        max_length=100,
        choices=[
            ('skill_enhancement', '기술 스킬 강화'),
            ('career_change', '커리어 전환'),
            ('promotion', '승진/성장'),
            ('interview_prep', '면접 준비'),
        ],
        default='skill_enhancement'
    )
    
    # AI 생성 학습 경로
    learning_roadmap = models.JSONField(
        verbose_name="학습 로드맵",
        help_text="단계별 학습 계획"
    )
    
    estimated_duration_months = models.PositiveIntegerField(
        verbose_name="예상 완료 기간(개월)",
        default=3
    )
    
    generation_metadata = models.JSONField(
        default=dict,
        verbose_name="생성 메타데이터"
    )
    
    class Meta:
        db_table = 'learning_paths'
        verbose_name = '학습 경로'
        verbose_name_plural = '학습 경로들'
        ordering = ['-created_at']


class UserFeedback(models.Model):
    """사용자 피드백 (개선용)"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(ResumeProfile, on_delete=models.CASCADE, related_name='feedbacks')
    created_at = models.DateTimeField(auto_now_add=True)
    
    feedback_type = models.CharField(
        max_length=50,
        choices=[
            ('interview_quality', '면접 질문 품질'),
            ('learning_path_relevance', '학습 경로 적합성'),
            ('overall_satisfaction', '전체 만족도'),
        ]
    )
    
    rating = models.PositiveIntegerField(
        choices=[(i, f'{i}점') for i in range(1, 6)],
        verbose_name="평점 (1-5)"
    )
    
    comment = models.TextField(
        blank=True,
        verbose_name="상세 피드백"
    )
    
    class Meta:
        db_table = 'user_feedbacks'
        verbose_name = '사용자 피드백'
        verbose_name_plural = '사용자 피드백들'
