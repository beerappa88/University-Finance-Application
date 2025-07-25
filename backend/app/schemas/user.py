from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
import uuid

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    student_id: Optional[str] = None
    employee_id: Optional[str] = None
    college_id: Optional[uuid.UUID] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None

class RoleRead(BaseModel):
    id: uuid.UUID
    name: str

    class Config:
        from_attributes = True

class UserInDB(UserBase):
    id: uuid.UUID
    is_verified: bool
    is_active: bool
    created_at: datetime
    roles: List[RoleRead] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
    permissions: List[str] = []
    college_id: Optional[uuid.UUID] = None
    role_ids: List[uuid.UUID] = []