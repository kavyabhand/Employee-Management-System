from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeOut, EmployeeUpdate

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("", response_model=list[EmployeeOut])
def list_employees(db: Session = Depends(get_db)):
    return db.query(Employee).order_by(Employee.id).all()


@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="employee not found")
    return employee


@router.post("", response_model=EmployeeOut, status_code=201)
def create_employee(body: EmployeeCreate, db: Session = Depends(get_db)):
    employee = Employee(**body.model_dump())
    db.add(employee)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="email already exists")
    db.refresh(employee)
    return employee


@router.put("/{employee_id}", response_model=EmployeeOut)
def update_employee(employee_id: int, body: EmployeeUpdate, db: Session = Depends(get_db)):
    employee = db.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="employee not found")

    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(employee, key, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="email already exists")
    db.refresh(employee)
    return employee


@router.delete("/{employee_id}", status_code=204)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.get(Employee, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="employee not found")
    db.delete(employee)
    db.commit()
