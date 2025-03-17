# 1. Python 이미지를 기본 이미지로 사용
FROM python:3.13.2-slim

# 2. 작업 디렉토리 설정
WORKDIR /home/salguy

# 3. 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 프로젝트 파일 복사
COPY . .

# 5. 컨테이너 시작 시 실행될 명령어 설정
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]