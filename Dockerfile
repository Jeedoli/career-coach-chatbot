# 🐳 AI Challenge - 커리어 코치 챗봇 Docker 배포용
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Poetry 설치
RUN pip install poetry

# Poetry 설정 (가상환경 생성 안함)
RUN poetry config virtualenvs.create false

# 의존성 파일 복사
COPY pyproject.toml poetry.lock* ./

# 의존성 설치 (프로덕션용 패키지만)
RUN poetry install --only=main

# 애플리케이션 코드 복사
COPY . .

# 데이터베이스 디렉토리 생성 및 권한 설정
RUN mkdir -p /app/db && chmod 755 /app/db

# 정적 파일 수집
RUN python manage.py collectstatic --noinput

# 데이터베이스 마이그레이션
RUN python manage.py migrate

# 포트 노출
EXPOSE 8000

# Gunicorn으로 실행 (프로덕션 환경)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "60", "career_coach.wsgi:application"]
