# Community Backend Portfolio | 아무 말 대잔치 Backend

## 프로젝트 개요 | Project Overview
`2-sungjin-community-be`는 **FastAPI + SQLAlchemy** 기반의 community backend API repository입니다.
이 저장소는 CRUD API 구현에만 머물지 않고, **database abstraction, authentication, containerization, Lambda image delivery, ECS rollout, EC2 deployment readiness, Kubernetes compatibility**까지 포함하도록 구성되었습니다.

This repository was developed as a portfolio-grade backend project. The focus was to demonstrate not only API implementation, but also how a backend can be packaged, verified, deployed, and operated across multiple runtime targets.

- Backend Repo: `https://github.com/sungjin9288/2-sungjin-community-be`
- Frontend Repo: `https://github.com/sungjin9288/2-sungjin-community-fe`
- Runtime note: cloud runtime resources used for validation were intentionally **torn down on 2026-03-11** to avoid unnecessary cost. The source code, deployment scripts, workflow definitions, and runbooks remain as portfolio evidence.

## 역할 정의 | Repository Role
This backend repository owns the following responsibilities:

| Area | Scope |
| --- | --- |
| API Layer | auth, users, posts, comments, direct messages, image-related endpoints |
| Data Layer | SQLAlchemy models, session management, DB health check |
| Security | password hashing, token-based auth flow, request validation |
| Runtime | FastAPI app startup, static/uploads mounting, health endpoints |
| Delivery | Docker image build, ECS task deployment support, Lambda container image support |
| Verification | pytest regression coverage, health checks, deployment smoke readiness |

## 핵심 성과 | Key Outcomes
- Built a **FastAPI REST API** supporting the full community lifecycle.
- Added a **database-driven health check** so deployment targets can fail fast when DB connectivity is broken.
- Made the backend **database-configurable** through `DATABASE_URL`, enabling SQLite for local validation and MySQL/PostgreSQL-compatible drivers for deployment targets.
- Added **runtime directory bootstrap** so containerized startup does not fail when `uploads/` or `static/` paths are missing.
- Packaged the backend for multiple targets:
  - EC2 + Docker Compose
  - ECS Fargate
  - Lambda container image
  - Kubernetes-compatible container runtime
- Verified integration with the frontend repository and GitHub Actions delivery flows.

## 기술 스택 | Tech Stack

### Application Layer
- `Python 3.11+`
- `FastAPI`
- `Uvicorn`
- `Pydantic`

### Data / Persistence
- `SQLAlchemy`
- `SQLite` for local/staging validation
- `PyMySQL` and `psycopg2-binary` for MySQL/PostgreSQL-compatible targets
- `Alembic` included in dependencies for migration-ready evolution

### Security / Auth
- `bcrypt`
- `passlib`
- `PyJWT`

### Delivery / Platform
- `Docker`
- `AWS ECS Fargate`
- `AWS Lambda (container image)`
- `AWS EC2`
- `Kubernetes-compatible deployment templates`

## 아키텍처 | Architecture

### Request path
1. Client sends request to FastAPI application.
2. Route layer validates request payload via Pydantic.
3. Controller/model layer executes business logic.
4. SQLAlchemy session accesses the configured database.
5. Response helpers return a consistent API envelope.

### Runtime-specific behavior
- `lifespan()` ensures startup/shutdown logging.
- `ensure_runtime_directories()` creates `uploads/`, `uploads/profile/`, `uploads/post/`, and `static/` before mounts.
- `/health` performs a real DB connectivity check using `SELECT 1`.
- `/uploads` and `/static` are mounted as static paths for image/content serving.

## 주요 기능 | Functional Scope

### Authentication / 인증
- signup
- login
- token refresh
- logout
- email duplication check
- nickname duplication check

### User Management / 사용자 관리
- my profile read/update
- 1:1 direct message thread list/read/send
- password change
- account deletion

### Post Domain / 게시글
- create, read, update, delete
- pagination
- detail read with count-related handling
- likes integration

### Comment Domain / 댓글
- create, update, delete
- list by post
- author ownership checks

### Static & Uploads / 정적 리소스
- terms/privacy static serving
- uploads mount for image delivery
- Lambda container entrypoint for image-oriented runtime packaging

## 현재 코드 기준 기술 포인트 | Implementation Notes

### Database configuration
`app/database.py` resolves the database from environment configuration:

```python
DEFAULT_SQLITE_URL = "sqlite:///./community.db"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)
```

This means the same application can run:
- locally with SQLite
- in containerized validation with SQLite-backed volume
- in production-like environments with MySQL/PostgreSQL-compatible URLs

### Startup hardening
A deployment issue was fixed by ensuring runtime directories are created before `StaticFiles` mounts are initialized.

Relevant file:
- `app/main.py`

## 프로젝트 구조 | Repository Structure

```text
2-sungjin-community-be/
├── app/
│   ├── common/                    # shared helpers, response/exception utilities
│   ├── controllers/               # business logic orchestration
│   ├── core/                      # logging and shared runtime utilities
│   ├── models/                    # domain access layer
│   ├── routes/                    # FastAPI routers
│   ├── database.py                # engine / session configuration
│   ├── db_models.py               # SQLAlchemy ORM models
│   ├── lambda_handler.py          # Lambda container entrypoint
│   └── main.py                    # FastAPI application bootstrap
├── deploy/ecs/                    # ECS task definition template assets
├── scripts/                       # deployment helpers
├── tests/                         # pytest regression coverage
├── Dockerfile
├── Dockerfile.lambda
├── requirements.txt
└── README.md
```

## 로컬 실행 | Local Development

### Prerequisites
- `Python 3.11+`
- optional virtual environment tooling

### Install
```bash
git clone https://github.com/sungjin9288/2-sungjin-community-be.git
cd 2-sungjin-community-be
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Environment
Example local environment:

```env
DATABASE_URL=sqlite:///./community.db
CORS_ALLOW_ORIGINS=http://localhost:3001,http://127.0.0.1:3001
```

### Run
```bash
uvicorn app.main:app --reload
```

Production-style local run:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open:
- `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 테스트 / 검증 | Test & Verification

### Pytest
```bash
pytest -q
```

### Health check
```bash
curl -s http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy","db":"ok"}
```

### Frontend-integrated verification
The paired frontend repository provides higher-level smoke validation via:
- `npm run test:integration`
- `npm run test:upload`

## API Surface Summary | API 요약

| Domain | Endpoints |
| --- | --- |
| Auth | `/auth/signup`, `/auth/login`, `/auth/refresh`, `/auth/logout`, `/auth/check-email`, `/auth/check-nickname` |
| Users | `/users/me`, `/users/me/password`, account management routes |
| Posts | post list/detail/create/update/delete |
| Comments | comment create/list/update/delete |
| Messages | `/messages/users`, `/messages/conversations`, `/messages/with/{user_id}`, `/messages` |
| Images | image-related upload helpers and mounted static paths |

## 배포 자산 | Delivery Assets

### Containerization
- `Dockerfile`
- `.dockerignore`
- `Dockerfile.lambda`

### Deployment Helpers
- `scripts/deploy-lambda-image.sh`
- `scripts/ec2-bluegreen-be-deploy.sh`
- `deploy/ecs/task-definition.template.json`

### Workflow / CI/CD Assets
- `.github/workflows/ci-backend.yml`
- `.github/workflows/deploy-lambda-image.yml`
- `.github/workflows/deploy-ecs-fargate.yml`
- blue/green support assets in the paired frontend repository

## Infra / Delivery Coverage | 수행 범위

This backend participated in validating the following runtime targets together with the frontend repository:

| Target | Status | Notes |
| --- | --- | --- |
| Docker image build | Done | backend image build validated |
| Docker Compose on EC2 | Done | FE/BE combined compose deployment validated |
| ECS Fargate | Done | backend task definition and service rollout validated |
| Lambda container image | Done | image packaging and deployment workflow prepared/validated |
| Kubernetes (staging validation) | Done | backend image deployed to EKS staging during validation |
| Blue/Green deployment support | Done | backend deployment helper assets prepared |

## Portfolio Value | 포트폴리오 관점의 강점
This repository demonstrates:

- API-first backend design
- runtime configurability instead of hardcoded infra coupling
- production-style startup hardening
- health-check-aware deployment readiness
- multi-target packaging strategy (EC2 / ECS / Lambda / K8s)
- cost-aware operations after validation

## Cost Control / 비용 정리 원칙
Because this project is a personal portfolio artifact, not a commercial service, the validated cloud runtime resources were removed after verification.

What remains in Git:
- backend source code
- Docker and Lambda packaging assets
- ECS deployment template
- CI/CD workflow definitions
- integration-compatible app structure

## Related Repository & Documents
- Frontend repo: `https://github.com/sungjin9288/2-sungjin-community-fe`
- Frontend infra report: `../2-sungjin-community-fe/docs/community-infra-reliability-report.md`
- Frontend deployment checklist: `../2-sungjin-community-fe/docs/deployment-execution-checklist.md`

## License
This project is released under the `MIT` License unless stated otherwise.
