from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


async def create_student(db: AsyncSession, data: StudentCreate) -> Student:
    student = Student(**data.model_dump())
    db.add(student)
    try:
        await db.commit()
        await db.refresh(student)
        return student
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Student email already exists")


async def get_all_students(
    db: AsyncSession,
    page: int = 1,
    limit: int = 10,
    name: str = None,
    department: str = None
):
    offset = (page - 1) * limit
    query = select(Student)

    if name:
        query = query.where(Student.name.ilike(f"%{name}%"))
    if department:
        query = query.where(Student.department.ilike(f"%{department}%"))

    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    query = query.offset(offset).limit(limit).order_by(Student.id)
    result = await db.execute(query)
    students = result.scalars().all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "students": students
    }


async def get_student_by_id(db: AsyncSession, student_id: int) -> Student:
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with id {student_id} not found")
    return student


async def update_student(db: AsyncSession, student_id: int, data: StudentUpdate) -> Student:
    student = await get_student_by_id(db, student_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)
    try:
        await db.commit()
        await db.refresh(student)
        return student
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Student email already exists")


async def delete_student(db: AsyncSession, student_id: int) -> dict:
    student = await get_student_by_id(db, student_id)
    await db.delete(student)
    await db.commit()
    return {"message": f"Student {student_id} deleted successfully"}