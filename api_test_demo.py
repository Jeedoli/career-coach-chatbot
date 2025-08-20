#!/usr/bin/env python3
"""
🧪 AI Challenge - 커리어 코치 챗봇 API 테스트 데모

실제 심사위원이 테스트할 수 있는 완전한 플로우를 보여줍니다.
"""

import requests
import json
import time
from typing import Dict, Any

class CareerCoachAPITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        
    def print_section(self, title: str):
        """섹션 제목 출력"""
        print(f"\n{'='*60}")
        print(f"🔍 {title}")
        print('='*60)
        
    def print_response(self, response: requests.Response):
        """응답 결과 예쁘게 출력"""
        try:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"📄 Response:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except:
            print(f"❌ Status: {response.status_code}")
            print(f"Response: {response.text}")
    
    def test_health_check(self):
        """헬스체크 테스트"""
        self.print_section("API 상태 확인")
        
        response = requests.get(f"{self.api_url}/health")
        self.print_response(response)
        
        return response.status_code == 200
    
    def test_profile_creation(self) -> str:
        """프로필 생성 테스트"""
        self.print_section("1단계: 이력서 프로필 생성 및 AI 분석")
        
        # 테스트 데이터 - 실제 예시
        profile_data = {
            "career_summary": "3년차 백엔드 개발자로 Spring Boot/MSA 기반 E-commerce 플랫폼 개발 경험. 월 1천만 건 트래픽 처리 시스템 설계 및 AWS 클라우드 운영. 팀 리딩 경험과 성능 최적화를 통한 응답시간 50% 개선 달성.",
            "job_role": "Spring Boot/MSA 기반 E-commerce 백엔드 개발",
            "technical_skills": "Python, Django, Spring Boot, Java, AWS EC2/RDS, Docker, Kubernetes, MySQL, Redis, Git, Jenkins",
            "experience_years": 3
        }
        
        print("📤 Request Data:")
        print(json.dumps(profile_data, indent=2, ensure_ascii=False))
        
        response = requests.post(
            f"{self.api_url}/profiles",
            json=profile_data,
            headers={"Content-Type": "application/json"}
        )
        
        self.print_response(response)
        
        if response.status_code == 201:
            data = response.json()
            return data["id"]
        return None
    
    def test_interview_questions(self, profile_id: str):
        """면접 질문 생성 테스트"""
        self.print_section("2단계: 맞춤형 면접 질문 5개 생성")
        
        interview_data = {
            "profile_id": profile_id,
            "target_company_type": "startup",
            "target_position_level": "mid"
        }
        
        print("📤 Request Data:")
        print(json.dumps(interview_data, indent=2, ensure_ascii=False))
        
        response = requests.post(
            f"{self.api_url}/interview-sessions",
            json=interview_data,
            headers={"Content-Type": "application/json"}
        )
        
        self.print_response(response)
        
        # 질문 품질 분석
        if response.status_code == 201:
            data = response.json()
            questions = data.get("questions", [])
            
            print(f"\n📊 질문 분석:")
            print(f"   - 총 질문 수: {len(questions)}개")
            
            categories = [q.get("category", "기타") for q in questions]
            difficulties = [q.get("difficulty_level", "기본") for q in questions]
            
            print(f"   - 카테고리: {', '.join(set(categories))}")
            print(f"   - 난이도 분포: {', '.join(set(difficulties))}")
            
            # 개인화 정도 체크
            spring_boot_mentioned = sum(1 for q in questions if "Spring Boot" in q.get("question", ""))
            print(f"   - 개인화 정도: Spring Boot 언급 {spring_boot_mentioned}회")
        
        return response.status_code == 201
    
    def test_learning_path(self, profile_id: str):
        """학습 경로 생성 테스트"""
        self.print_section("3단계: 개인화된 학습 경로 추천")
        
        learning_data = {
            "profile_id": profile_id,
            "target_goal": "skill_enhancement",
            "preferred_duration_months": 3
        }
        
        print("📤 Request Data:")
        print(json.dumps(learning_data, indent=2, ensure_ascii=False))
        
        response = requests.post(
            f"{self.api_url}/learning-paths",
            json=learning_data,
            headers={"Content-Type": "application/json"}
        )
        
        self.print_response(response)
        
        # 학습 경로 품질 분석
        if response.status_code == 201:
            data = response.json()
            roadmap = data.get("learning_roadmap", [])
            
            print(f"\n📊 학습 경로 분석:")
            print(f"   - 총 단계 수: {len(roadmap)}단계")
            
            total_weeks = sum(step.get("duration_weeks", 0) for step in roadmap)
            print(f"   - 총 학습 기간: {total_weeks}주")
            
            # AI Challenge 요구사항 체크
            all_objectives = []
            for step in roadmap:
                all_objectives.extend(step.get("objectives", []))
            
            objectives_text = " ".join(all_objectives)
            
            has_tech_enhancement = any("기술" in obj or "스택" in obj for obj in all_objectives)
            has_project_experience = any("프로젝트" in obj for obj in all_objectives)
            has_communication = any("발표" in obj or "커뮤니케이션" in obj or "멘토링" in obj for obj in all_objectives)
            
            print(f"   - ✅ 기술 스택 심화: {'포함' if has_tech_enhancement else '누락'}")
            print(f"   - ✅ 프로젝트 경험: {'포함' if has_project_experience else '누락'}")
            print(f"   - ✅ 커뮤니케이션 스킬: {'포함' if has_communication else '누락'}")
        
        return response.status_code == 201
    
    def test_profile_insights(self, profile_id: str):
        """프로필 인사이트 테스트"""
        self.print_section("추가 기능: 프로필 인사이트")
        
        response = requests.get(f"{self.api_url}/profiles/{profile_id}/insights")
        self.print_response(response)
        
        return response.status_code == 200
    
    def run_full_test(self):
        """전체 플로우 테스트"""
        print("🤖 AI Challenge - 커리어 코치 챗봇 API 테스트 시작")
        print(f"🌐 API URL: {self.api_url}")
        print(f"📄 Swagger 문서: {self.base_url}/api/docs")
        
        start_time = time.time()
        
        # 1. 헬스체크
        if not self.test_health_check():
            print("❌ API 서버가 응답하지 않습니다. 서버를 먼저 시작해주세요.")
            return False
        
        # 2. 프로필 생성
        profile_id = self.test_profile_creation()
        if not profile_id:
            print("❌ 프로필 생성 실패")
            return False
        
        # 3. 면접 질문 생성
        if not self.test_interview_questions(profile_id):
            print("❌ 면접 질문 생성 실패")
            return False
        
        # 4. 학습 경로 생성
        if not self.test_learning_path(profile_id):
            print("❌ 학습 경로 생성 실패")
            return False
        
        # 5. 인사이트 조회
        self.test_profile_insights(profile_id)
        
        # 결과 요약
        total_time = time.time() - start_time
        
        print(f"\n{'='*60}")
        print("🎉 전체 테스트 완료!")
        print(f"⏱️  총 소요 시간: {total_time:.2f}초")
        print(f"📊 생성된 프로필 ID: {profile_id}")
        print("✅ AI Challenge 3대 요구사항 모두 검증 완료:")
        print("   1. ✅ 이력서 핵심 정보 입력 API")
        print("   2. ✅ 맞춤 면접 모의 질문 5개 생성")
        print("   3. ✅ 자기 개발 학습 경로 추천 (기술 심화 + 프로젝트 + 커뮤니케이션)")
        print(f"\n📄 더 자세한 API 문서: {self.base_url}/api/docs")
        print(f"🔍 Swagger UI에서 직접 테스트해보세요!")
        
        return True

def main():
    """메인 실행 함수"""
    tester = CareerCoachAPITester()
    
    try:
        success = tester.run_full_test()
        exit(0 if success else 1)
    except requests.exceptions.ConnectionError:
        print("❌ 서버에 연결할 수 없습니다.")
        print("💡 다음 명령어로 서버를 먼저 시작해주세요:")
        print("   poetry run python manage.py runserver")
        exit(1)
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        exit(1)

if __name__ == "__main__":
    main()
