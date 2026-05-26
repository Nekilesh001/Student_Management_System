import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate
from app.services.redis_service import get_redis

CACHE_TTL = 300  # 5 minutes


def student_cache_key(student_id: int) -> str:
    return f"student:{student_id}"


def students_list_cache_key(page: int, limit: int, name: str, department: str) -> str:
    return f"students:list:{page}:{limit}:{name}:{department}"


async def invalidate_student_cache(student_id: int = None):
    try:
        redis = await get_redis()
        if student_id:
            await redis.delete(student_cache_key(student_id))
        # Always clear list cache on any mutation
        keys = await redis.keys("students:list:*")
        if keys:
            await redis.delete(*keys)
    except Exception:
        pass  # Cache errors should never break the app


async def create_student(db: AsyncSession, data: StudentCreate) -> Student:
    student = Student(**data.model_dump())
    db.add(student)
    try:
        await db.commit()
        await db.refresh(student)
        await invalidate_student_cache()
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
    cache_key = students_list_cache_key(page, limit, name, department)

    try:
        redis = await get_redis()
        cached = await redis.get(cache_key)
        if cached:
            return json.loads(cached)
    except Exception:
        pass

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

    students_data = [
        {
            "id": s.id,
            "name": s.name,
            "age": s.age,
            "department": s.department,
            "email": s.email,
            "phone": s.phone,
            "address": s.address,
            "created_at": s.created_at.isoformat()
        }
        for s in students
    ]

    response = {
        "total": total,
        "page": page,
        "limit": limit,
        "students": students_data
    }

    try:
        redis = await get_redis()
        await redis.setex(cache_key, CACHE_TTL, json.dumps(response))
    except Exception:
        pass

    return response


async def get_student_by_id(db: AsyncSession, student_id: int) -> Student:
    cache_key = student_cache_key(student_id)

    try:
        redis = await get_redis()
        cached = await redis.get(cache_key)
        if cached:
            data = json.loads(cached)
            student = Student(**{k: v for k, v in data.items() if k != "created_at"})
            return student
    except Exception:
        pass

    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with id {student_id} not found")

    try:
        redis = await get_redis()
        data = {
            "id": student.id,
            "name": student.name,
            "age": student.age,
            "department": student.department,
            "email": student.email,
            "phone": student.phone,
            "address": student.address,
            "created_at": student.created_at.isoformat()
        }
        await redis.setex(cache_key, CACHE_TTL, json.dumps(data))
    except Exception:
        pass

    return student


async def update_student(db: AsyncSession, student_id: int, data: StudentUpdate) -> Student:
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with id {student_id} not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)
    try:
        await db.commit()
        await db.refresh(student)
        await invalidate_student_cache(student_id)
        return student
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Student email already exists")


async def delete_student(db: AsyncSession, student_id: int) -> dict:
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with id {student_id} not found")

    await db.delete(student)
    await db.commit()
    await invalidate_student_cache(student_id)
    return {"message": f"Student {student_id} deleted successfully"}
