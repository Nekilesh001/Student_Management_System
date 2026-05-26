from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database.connection import get_db
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse, StudentListResponse
from app.services.student_service import (
    create_student, get_all_students,
    get_student_by_id, update_student, delete_student
)
from app.auth.dependencies import get_current_user, require_admin, require_any_role
from app.models.user import User

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", response_model=StudentResponse, status_code=201)
async def create(
    data: StudentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return await create_student(db, data)


@router.get("/", response_model=StudentListResponse)
async def list_students(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    name: Optional[str] = Query(default=None),
    department: Optional[str] = Query(default=None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_any_role)
):
    return await get_all_students(db, page, limit, name, department)


@router.get("/{student_id}", response_model=StudentResponse)
async def get_one(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_any_role)
):
    return await get_student_by_id(db, student_id)


@router.put("/{student_id}", response_model=StudentResponse)
async def update(
    student_id: int,
    data: StudentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return await update_student(db, student_id, data)


@router.delete("/{student_id}")
async def delete(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return await delete_student(db, student_id)