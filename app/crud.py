from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models, schemas
from datetime import date
from sqlalchemy import and_

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    existing = db.query(models.Employee).filter(
        (models.Employee.email == employee.email) |
        (models.Employee.employee_id == employee.employee_id)
    ).first()

    if existing:
        raise HTTPException(status_code=409, detail="Employee already exists")

    emp = models.Employee(**employee.dict())
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp


def get_employees(db: Session):
    return db.query(models.Employee).all()


def delete_employee(db: Session, employee_id: int):
    emp = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(emp)
    db.commit()


def mark_attendance(db: Session, data: schemas.AttendanceCreate):
    employee = db.query(models.Employee).filter(
        models.Employee.id == data.employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    attendance = models.Attendance(**data.dict())
    db.add(attendance)
    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Attendance already marked for this date"
        )
    db.refresh(attendance)
    return attendance


def get_attendance_for_employee(db: Session, employee_id: int):
    return db.query(models.Attendance).filter(
        models.Attendance.employee_id == employee_id
    ).all()

def get_attendance_on_date(db: Session, target_date: date):
    return (
        db.query(
            models.Employee.id.label("employee_id"),
            models.Employee.employee_id.label("employee_code"),
            models.Employee.full_name,
            models.Employee.department,
            models.Attendance.date,
            models.Attendance.status,
        )
        .outerjoin(
            models.Attendance,
            and_(
                models.Attendance.employee_id == models.Employee.id,
                models.Attendance.date == target_date,
            ),
        )
        .order_by(models.Employee.full_name.asc())
        .all()
    )