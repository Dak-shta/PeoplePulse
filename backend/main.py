from fastapi import FastAPI, Depends
from database.table import Base,Employee
from sqlalchemy.orm import Session
from connect import engine
from schema.check import E_create, E_response
from connect import SessionLocal
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


@app.post("/add",response_model=E_response)
def add_emp(newemp:E_create,db:Session=Depends(get_db)):
    emps=Employee(**newemp.model_dump())
    db.add(emps)
    db.commit()
    db.refresh(emps)

    return emps