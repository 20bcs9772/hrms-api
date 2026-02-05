from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, crud
from datetime import date

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/", response_model=schemas.AttendanceResponse, status_code=201)
def mark_attendance(data: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    return crud.mark_attendance(db, data)


@router.get("/{employee_id}", response_model=list[schemas.AttendanceResponse])
def get_attendance(employee_id: int, db: Session = Depends(get_db)):
    return crud.get_attendance_for_employee(db, employee_id)

@router.get("/", response_model=list[schemas.AttendanceOverview])
def get_attendance_on_date(
    date: date = Query(..., description="Attendance date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    return crud.get_attendance_on_date(date, db)
