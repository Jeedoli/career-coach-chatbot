"""
🧪 Django 테스트 케이스

Unit tests for the Career Coach Chatbot API
"""

from django.test import TestCase, Client
from django.urls import reverse
from .models import ResumeProfile, InterviewSession, LearningPath

class ResumeProfileTestCase(TestCase):
    """이력서 프로필 모델 테스트"""
    
    def setUp(self):
        self.profile_data = {
            'career_summary': '3년차 백엔드 개발자',
            'job_role': 'Spring Boot 개발',
            'technical_skills': 'Java, Spring Boot, MySQL',
            'experience_years': 3
        }
    
    def test_profile_creation(self):
        """프로필 생성 테스트"""
        profile = ResumeProfile.objects.create(**self.profile_data)
        self.assertTrue(isinstance(profile, ResumeProfile))
        self.assertEqual(profile.career_summary, '3년차 백엔드 개발자')

class APIEndpointTestCase(TestCase):
    """API 엔드포인트 테스트"""
    
    def setUp(self):
        self.client = Client()
    
    def test_health_check(self):
        """헬스체크 엔드포인트 테스트"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
    # TODO: OpenAI API 키가 필요한 테스트들은 추후 추가
