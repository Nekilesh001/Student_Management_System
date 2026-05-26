from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.database.connection import engine, Base
from app.models import User, Student
from app.api.auth import router as auth_router
from app.api.students import router as students_router
from app.middleware.error_handlers import (
    validation_exception_handler,
    sqlalchemy_exception_handler,
    http_exception_handler,
    generic_exception_handler
)
from app.middleware.logging_middleware import RequestLoggingMiddleware
from app.middleware.rate_limiter import RateLimitMiddleware
from app.services.redis_service import get_redis, close_redis

app = FastAPI(
    title="Student Management System",
    description="Enterprise Student Management API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)
#app.add_middleware(RateLimitMiddleware)
# Error handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await get_redis()

    print("✅ Database tables created successfully")
    print("✅ Redis connected successfully")


@app.on_event("shutdown")
async def shutdown():
    await close_redis()
    print("🔴 Redis connection closed")

app.include_router(auth_router)
app.include_router(students_router)

@app.get("/")
async def root():
    return {
        "message": "Student Management System API",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
