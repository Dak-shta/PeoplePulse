from fastapi import FastAPI, Depends, HTTPException
from database.table import Base,Employee
from sqlalchemy.orm import Session
from connect import engine
from schema.check import E_create, E_response, Upcoming_days, Upcoming_anniv
from connect import SessionLocal
from datetime import date

app=FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {'message':'Finally! MADE IT'}

@app.get("/employees",response_model=list[E_response])
def show_emp(db:Session=Depends(get_db)):
    emps=db.query(Employee).all()
    return emps

@app.get("/upcoming-births",response_model=list[Upcoming_days])
def get_birth_emp(db:Session=Depends(get_db)):
    employees=db.query(Employee).all()
    upcoming=[]
    for emp in employees:
        today=date.today()
        next_birthday=date(
            today.year,
            emp.date_birth.month,
            emp.date_birth.day
        )
        if next_birthday<today:
            next_birthday=date(
                today.year+1,
                emp.date_birth.month,
                emp.date_birth.day
            )
        rem_days=(next_birthday-today).days

        if 0<=rem_days<=7:
            upcoming.append({"name":emp.name,"department":emp.department,"rem_days":rem_days,
                             "birthday":next_birthday})
    return upcoming


@app.get("/work-anniversary",response_model=list[Upcoming_anniv])
def get_work_emp(db:Session=Depends(get_db)):
    emps=db.query(Employee).all()
    upcoming=[]
    for emp in emps:
        today=date.today()
        years=date(
            emp.date_joining.year,
            emp.date_joining.month,
            emp.date_joining.day
        )
        next_anniversary=date(
            today.year,
            emp.date_joining.month,
            emp.date_joining.day
        )
        if next_anniversary<today:
            next_anniversary=date(
                today.year+1,
                emp.date_joining.month,
                emp.date_joining.day
            )
        rem_days=(next_anniversary-today).days
        years_completed=today.year-years.year

        if 0<=rem_days<=7:
            upcoming.append({"name":emp.name,
             "department":emp.department,
             "rem_days":rem_days,
             "years_completed":years_completed,
             "anniversary":next_anniversary
             })
    return upcoming     

@app.post("/add",response_model=E_response)
def add_emp(newemp:E_create,db:Session=Depends(get_db)):
    emps=Employee(**newemp.model_dump())
    db.add(emps)
    db.commit()
    db.refresh(emps)

    return emps

@app.delete("/delete")
def delete_emp(id:int,db:Session=Depends(get_db)):
    emp=db.query(Employee).filter(Employee.id==id).first()
    if emp:
        db.delete(emp)
        db.commit()
    else:
        raise HTTPException(status_code=404,detail="NOT FOUND")
