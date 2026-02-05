from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from enum import Enum

class AttendanceStatus(str, Enum):
    Present = "Present"
    Absent = "Absent"


class EmployeeCreate(BaseModel):
    employee_id: str
    full_name: str
    email: EmailStr
    department: str


class EmployeeResponse(EmployeeCreate):
    id: int

    class Config:
        from_attributes = True


class AttendanceCreate(BaseModel):
    employee_id: int
    date: date
    status: AttendanceStatus


class AttendanceResponse(BaseModel):
    id: int
    date: date
    status: AttendanceStatus

    class Config:
        from_attributes = True

class AttendanceOverview(BaseModel):
    employee_id: int
    employee_code: str
    full_name: str
    department: str
    date: date
    status: Optional[AttendanceStatus]

    class Config:
        from_attributes = True