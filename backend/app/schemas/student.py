from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ─── REQUEST SCHEMAS ──────────────────────────────

class StudentCreate(BaseModel):
    name: str
    age: int
    department: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    department: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None

# ─── RESPONSE SCHEMAS ─────────────────────────────

class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    department: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}

# ─── PAGINATED RESPONSE ───────────────────────────

class StudentListResponse(BaseModel):
    total: int
    page: int
    limit: int
    students: list[StudentResponse]