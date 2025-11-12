# FastAPI Board API

FastAPI로 구현한 자유게시판 백엔드 API입니다. 게시글, 댓글, 사용자 인증 기능을 제공합니다.

## 기술 스택

- **FastAPI**: 고성능 웹 프레임워크
- **PostgreSQL**: 데이터베이스
- **SQLAlchemy**: ORM
- **JWT**: 인증
- **Docker & Docker Compose**: 컨테이너화

## 주요 기능

- 사용자 인증 (회원가입, 로그인, JWT 토큰)
- 게시글 CRUD (생성, 조회, 수정, 삭제)
- 댓글 기능
- 조회수 추적
- 페이지네이션

## 프로젝트 구조

```
fast-api-web/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 애플리케이션 진입점
│   ├── config.py            # 설정 파일
│   ├── database.py          # 데이터베이스 연결
│   ├── models/              # SQLAlchemy 모델
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── schemas/             # Pydantic 스키마
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── api/                 # API 라우터
│   │   ├── auth.py
│   │   ├── posts.py
│   │   └── comments.py
│   └── core/                # 핵심 기능
│       ├── security.py      # JWT, 비밀번호 해싱
│       └── dependencies.py  # 의존성 주입
├── Dockerfile
├── compose.yml
├── requirements.txt
└── .env.example
```

## 로컬 개발 환경 설정

### 1. 저장소 클론

```bash
git clone <repository-url>
cd fast-api-web
```

### 2. 환경 변수 설정

```bash
cp .env.example .env
```

`.env` 파일을 열어 필요한 값을 수정하세요:
- `SECRET_KEY`: 강력한 랜덤 키로 변경
- `DATABASE_URL`: 필요시 데이터베이스 설정 변경

### 3. Docker Compose로 실행

```bash
docker compose up -d
```

API 서버가 `http://localhost:8000`에서 실행됩니다.

### 4. API 문서 확인

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## AWS 배포 가이드

### 사전 요구사항

- AWS EC2 인스턴스 (Ubuntu 20.04 이상 권장)
- Docker 및 Docker Compose 설치
- 보안 그룹에서 포트 8000 열기

### 배포 단계

#### 1. EC2 인스턴스에 접속

```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

#### 2. Docker 설치

```bash
# Docker 설치
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker

# Docker Compose 설치
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 현재 사용자를 docker 그룹에 추가
sudo usermod -aG docker $USER
newgrp docker
```

#### 3. 프로젝트 배포

```bash
# 프로젝트 클론
git clone <repository-url>
cd fast-api-web

# 환경 변수 설정
cp .env.example .env
nano .env  # SECRET_KEY를 강력한 값으로 변경

# Docker Compose로 실행
docker compose up -d

# 로그 확인
docker compose logs -f
```

#### 4. 방화벽 설정

AWS 보안 그룹에서 다음 포트를 허용하세요:
- 8000: API 서버
- 22: SSH (관리용)

#### 5. 서비스 확인

```bash
curl http://your-ec2-ip:8000/health
```

### 프로덕션 권장 사항

1. **환경 변수 보안**
   - `SECRET_KEY`를 강력한 랜덤 값으로 설정
   - `.env` 파일 권한 제한: `chmod 600 .env`

2. **HTTPS 설정**
   - Nginx 리버스 프록시 사용
   - Let's Encrypt SSL 인증서 적용

3. **데이터베이스 백업**
   - 정기적인 PostgreSQL 백업 설정
   - AWS RDS 사용 권장

4. **모니터링**
   - 로그 모니터링 설정
   - 헬스체크 엔드포인트 활용

## API 엔드포인트

### 인증

- `POST /auth/register`: 회원가입
- `POST /auth/login`: 로그인
- `GET /auth/me`: 현재 사용자 정보

### 게시글

- `GET /posts`: 게시글 목록 조회 (페이지네이션)
- `POST /posts`: 게시글 작성 (인증 필요)
- `GET /posts/{post_id}`: 게시글 상세 조회
- `PUT /posts/{post_id}`: 게시글 수정 (작성자만)
- `DELETE /posts/{post_id}`: 게시글 삭제 (작성자만)

### 댓글

- `GET /posts/{post_id}/comments`: 댓글 목록 조회
- `POST /posts/{post_id}/comments`: 댓글 작성 (인증 필요)
- `PUT /posts/{post_id}/comments/{comment_id}`: 댓글 수정 (작성자만)
- `DELETE /posts/{post_id}/comments/{comment_id}`: 댓글 삭제 (작성자만)

## 사용 예시

### 회원가입

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 로그인

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### 게시글 작성 (토큰 필요)

```bash
curl -X POST http://localhost:8000/posts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "첫 번째 게시글",
    "content": "안녕하세요!"
  }'
```

## 개발

### 로컬에서 Python 가상환경 사용

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 개발 서버 실행
uvicorn app.main:app --reload
```

## 라이선스

MIT License