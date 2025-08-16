#!/usr/bin/env python3
"""
🧪 커리어 코치 챗봇 API 테스트 스크립트

이 스크립트는 API의 모든 엔드포인트를 테스트하여
정상 동작을 확인합니다.
"""

import requests
import json
import sys
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api"

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.profile_id = None
        
    def test_health_check(self) -> bool:
        """헬스체크 테스트"""
        print("🔍 1. 헬스체크 테스트...")
        
        try:
            response = self.session.get(f"{BASE_URL}/health")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 헬스체크 성공: {data['message']}")
                return True
            else:
                print(f"❌ 헬스체크 실패: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 연결 오류: {e}")
            return False

    def test_create_profile(self) -> bool:
        """프로필 생성 테스트"""
        print("\\n🔍 2. 이력서 프로필 생성 테스트...")
        
        # 테스트 데이터
        test_data = {
            "career_summary": "3년차 백엔드 개발자, Spring Boot/MSA/Python 기반 커머스 서비스 개발, AWS EC2 운영 경험",
            "job_role": "Spring Boot/MSA 기반 커머스 서비스 개발", 
            "technical_skills": "Python, Django, Spring Boot, AWS EC2, Docker, MySQL, Redis",
            "experience_years": 3
        }
        
        try:
            response = self.session.post(
                f"{BASE_URL}/profiles",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                data = response.json()
                self.profile_id = data['id']
                print(f"✅ 프로필 생성 성공: {self.profile_id}")
                print(f"📊 분석 결과: {data['analysis_result']['career_level']}")
                print(f"💪 강점: {', '.join(data['analysis_result']['strength_areas'][:2])}")
                return True
            else:
                print(f"❌ 프로필 생성 실패: {response.status_code}")
                print(f"오류: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 프로필 생성 오류: {e}")
            return False

    def test_get_profile(self) -> bool:
        """프로필 조회 테스트"""
        print("\\n🔍 3. 프로필 조회 테스트...")
        
        if not self.profile_id:
            print("❌ 프로필 ID가 없습니다.")
            return False
            
        try:
            response = self.session.get(f"{BASE_URL}/profiles/{self.profile_id}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 프로필 조회 성공: {data['career_summary'][:50]}...")
                return True
            else:
                print(f"❌ 프로필 조회 실패: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 프로필 조회 오류: {e}")
            return False

    def test_create_interview_session(self) -> bool:
        """면접 질문 생성 테스트"""
        print("\\n🔍 4. 면접 질문 생성 테스트...")
        
        if not self.profile_id:
            print("❌ 프로필 ID가 없습니다.")
            return False
            
        test_data = {
            "profile_id": self.profile_id,
            "target_company_type": "startup",
            "target_position_level": "mid"
        }
        
        try:
            print("⏳ AI가 맞춤형 면접 질문을 생성 중...")
            response = self.session.post(
                f"{BASE_URL}/interview-sessions",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                data = response.json()
                print(f"✅ 면접 질문 생성 성공! (생성 시간: {data['generation_metadata']['generation_time_seconds']}초)")
                
                # 생성된 질문들 출력
                for i, question in enumerate(data['questions'][:3], 1):
                    print(f"\\n📋 질문 {i} ({question['category']}):")
                    print(f"   {question['question']}")
                    
                print(f"\\n... 총 {len(data['questions'])}개 질문 생성됨")
                return True
            else:
                print(f"❌ 면접 질문 생성 실패: {response.status_code}")
                print(f"오류: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 면접 질문 생성 오류: {e}")
            return False

    def test_create_learning_path(self) -> bool:
        """학습 경로 생성 테스트"""
        print("\\n🔍 5. 학습 경로 생성 테스트...")
        
        if not self.profile_id:
            print("❌ 프로필 ID가 없습니다.")
            return False
            
        test_data = {
            "profile_id": self.profile_id,
            "target_goal": "skill_enhancement",
            "preferred_duration_months": 3
        }
        
        try:
            print("⏳ AI가 개인 맞춤형 학습 경로를 생성 중...")
            response = self.session.post(
                f"{BASE_URL}/learning-paths",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                data = response.json()
                print(f"✅ 학습 경로 생성 성공! (예상 기간: {data['estimated_duration_months']}개월)")
                
                # 학습 단계들 출력
                for i, step in enumerate(data['learning_roadmap'][:2], 1):
                    print(f"\\n📚 {step['phase']} ({step['duration_weeks']}주)")
                    print(f"   목표: {', '.join(step['objectives'][:2])}")
                    
                print(f"\\n... 총 {len(data['learning_roadmap'])}단계 로드맵 생성됨")
                return True
            else:
                print(f"❌ 학습 경로 생성 실패: {response.status_code}")
                print(f"오류: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 학습 경로 생성 오류: {e}")
            return False

    def test_get_insights(self) -> bool:
        """인사이트 조회 테스트"""
        print("\\n🔍 6. 프로필 인사이트 조회 테스트...")
        
        if not self.profile_id:
            print("❌ 프로필 ID가 없습니다.")
            return False
            
        try:
            response = self.session.get(f"{BASE_URL}/profiles/{self.profile_id}/insights")
            
            if response.status_code == 200:
                data = response.json()
                insights = data['data']
                summary = insights['profile_summary']
                
                print(f"✅ 인사이트 조회 성공!")
                print(f"📊 커리어 레벨: {summary['career_level']}")
                print(f"🎯 시장 경쟁력: {summary['market_competitiveness']}/10")
                print(f"📈 생성된 세션: 면접 {summary['created_sessions']}개, 학습경로 {summary['created_learning_paths']}개")
                return True
            else:
                print(f"❌ 인사이트 조회 실패: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 인사이트 조회 오류: {e}")
            return False

    def run_all_tests(self):
        """모든 테스트 실행"""
        print("🚀 커리어 코치 챗봇 API 테스트 시작!\\n")
        
        tests = [
            self.test_health_check,
            self.test_create_profile,
            self.test_get_profile,
            self.test_create_interview_session,
            self.test_create_learning_path,
            self.test_get_insights
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
            time.sleep(1)  # API 호출 간격
            
        print(f"\\n{'='*50}")
        print(f"🎯 테스트 결과: {passed}/{total} 통과")
        
        if passed == total:
            print("🎉 모든 테스트 통과! API가 정상적으로 동작합니다!")
            return True
        else:
            print("❌ 일부 테스트 실패. 로그를 확인해주세요.")
            return False


def main():
    """메인 함수"""
    print("🤖 커리어 코치 챗봇 API 테스트")
    print("=" * 50)
    
    # 서버 연결 확인
    tester = APITester()
    
    if not tester.test_health_check():
        print("\\n❌ 서버에 연결할 수 없습니다.")
        print("다음을 확인해주세요:")
        print("1. 서버가 실행 중인지 확인: poetry run python manage.py runserver")
        print("2. URL이 올바른지 확인: http://localhost:8000")
        print("3. .env 파일에 OPENAI_API_KEY가 설정되어 있는지 확인")
        sys.exit(1)
    
    # 전체 테스트 실행
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
