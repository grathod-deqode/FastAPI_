
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from models.schema import EmployeesTable, Employee, EmployeePatch

router = APIRouter()


@router.get("/")
def welcome_crud():
    return "Smile, now you are starting CRUD implementation."


# GET ALL EMPLOYEES
@router.get("/employees")
def get_all_employees(db: Session = Depends(get_db)):
    employees = db.query(EmployeesTable).all()
    return employees


# CREATE EMPLOYEE
@router.post("/employees")
def create_employee(employee: Employee, db: Session = Depends(get_db)):
    new_employee = EmployeesTable(
        name=employee.name,
        department=employee.department,
        city=employee.city,
        mobile_num=employee.mobile_num,
        gmail=employee.gmail,
        age=employee.age
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


# GET EMPLOYEE BY ID
@router.get("/employees/{employee_id}")
def get_employee_by_id(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(EmployeesTable).filter(
        EmployeesTable.id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee


# PUT - UPDATE ALL FIELDS
@router.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    employee: Employee,
    db: Session = Depends(get_db)
):
    existing_employee = db.query(EmployeesTable).filter(
        EmployeesTable.id == employee_id
    ).first()

    if existing_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    existing_employee.name = employee.name
    existing_employee.department = employee.department
    existing_employee.city = employee.city
    existing_employee.mobile_num = employee.mobile_num
    existing_employee.gmail = employee.gmail
    existing_employee.age = employee.age

    db.commit()
    db.refresh(existing_employee)

    return existing_employee


# PATCH - UPDATE SELECTED FIELDS
@router.patch("/employees/{employee_id}")
def patch_employee(
    employee_id: int,
    employee: EmployeePatch,
    db: Session = Depends(get_db)
):
    existing_employee = db.query(EmployeesTable).filter(
        EmployeesTable.id == employee_id
    ).first()

    if existing_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    update_data = employee.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(existing_employee, key, value)

    db.commit()
    db.refresh(existing_employee)

    return existing_employee


# DELETE EMPLOYEE
@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(EmployeesTable).filter(
        EmployeesTable.id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()

    return {"message": "Employee deleted successfully"}
