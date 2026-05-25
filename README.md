# Enterprise Student Management System

## Description
Production-grade full-stack application developed for the **ML Engineer Internship** at **ONEDATA SOFTWARE SOLUTIONS PVT LTD**.

---

## Tech Stack

| Technology | Purpose | Key Libraries / Features |
|---|---|---|
| **FastAPI** | Backend Framework | Async handlers, Dependency Injection |
| **PostgreSQL** | Database | Relational storage for student/user data |
| **SQLAlchemy** | ORM | Async sessions, migrations via Alembic |
| **JWT** | Authentication | Token-based security, python-jose |
| **Redis** | Caching & Rate Limiting | In-memory key-value store |
| **React** | Frontend UI | Component-based, SPA routing |
| **Tailwind CSS** | Styling | Utility-first, clean visual components |
| **Docker** | Containerization | Multi-container setup via Docker Compose |
| **GitHub Actions**| CI/CD Pipeline | Automated builds, testing, and deployment |
| **Kubernetes** | Orchestration | Scalable deployment manifests |

---

## Folder Structure

```text
student_mangement_system/
├── .github/
│   └── workflows/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── auth/
│   │   ├── database/
│   │   ├── middleware/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   ├── tests/
│   ├── .env
│   ├── .gitignore
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   ├── index.html
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── vite.config.js
├── k8s/
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Setup Instructions

### Backend Setup
1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix/macOS:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy/Create your `.env` file and update credentials.
5. Start the FastAPI development server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```

---

## API Endpoints Table

| Category | HTTP Method | Endpoint | Description | Auth Required |
|---|---|---|---|---|
| **System** | GET | `/` | Root entrypoint, API status | No |
| **System** | GET | `/health` | Application health check | No |
| **Auth** | POST | `/api/v1/auth/register` | Register new admin/user | No |
| **Auth** | POST | `/api/v1/auth/login` | Login and retrieve JWT token | No |
| **Students** | GET | `/api/v1/students` | Get list of all students | Yes (JWT) |
| **Students** | GET | `/api/v1/students/{id}` | Get specific student profile | Yes (JWT) |
| **Students** | POST | `/api/v1/students` | Add a new student record | Yes (JWT) |
| **Students** | PUT | `/api/v1/students/{id}` | Update existing student record| Yes (JWT) |
| **Students** | DELETE | `/api/v1/students/{id}` | Delete a student record | Yes (JWT) |

---

## Docker Commands

- Build and start all services (FastAPI, Postgres, Redis):
  ```bash
  docker-compose up --build
  ```
- Stop and remove containers and networks:
  ```bash
  docker-compose down
  ```
- View service logs:
  ```bash
  docker-compose logs -f
  ```

---

## API Documentation

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Author
**NEKILESH**  
ML Engineer Intern  
*ONEDATA SOFTWARE SOLUTIONS PVT LTD*  
