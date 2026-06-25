from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from database.table import Base,Employee,Company
from sqlalchemy.orm import Session
from connect import engine
from schema.check import E_create, E_response, Upcoming_days, Upcoming_anniv, Upcoming_events
from connect import SessionLocal
from datetime import date
from schema.check import CompanyCreate
from database.table import Company
import subprocess
from passlib.hash import bcrypt
from schema.check import SignupRequest, LoginRequest, GoogleLogin,GoogleSignup
from google.oauth2 import id_token
from google.auth.transport import requests
from email_service import send_welcome_email

app=FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import threading

from schedular import start_scheduler

@app.on_event("startup")
def startup_event():
    start_scheduler()
    print("Scheduler Started")
# @app.on_event("startup")
# def start_scheduler():
#     threading.Thread(
#         target=schedular.start,
#         daemon=True
#     ).start()

    # print("Scheduler Started")


# @app.on_event("startup")
# def start_scheduler():
#     subprocess.Popen(["python", "scheduler.py"])

@app.get("/")
def home():
    return {'message':'Finally! MADE IT'}

from fastapi import UploadFile, File, Depends
from sqlalchemy.orm import Session
import pandas as pd

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    hr_email: str = Form(...),
    db: Session = Depends(get_db)
):
    filename = file.filename

    # Read file
    if filename.endswith(".csv"):
        df = pd.read_csv(file.file)

    elif filename.endswith(".xlsx"):
        df = pd.read_excel(file.file)

    else:
        return {
            "success": False,
            "message": "Only CSV and Excel files are allowed"
        }

    # Normalize column names
    df.columns = df.columns.str.lower().str.strip()
    # print(df.columns.tolist())
    # print(row)

    # Check empty file
    if df.empty:
        return {
            "success": False,
            "message": "Uploaded file is empty"
        }

    # Required columns
    required_columns = [
        "name",
        "department",
        "email",
        "date_birth",
        "date_joining"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        return {
            "success": False,
            "message": f"Missing columns: {', '.join(missing_columns)}"
        }

    added = 0
    duplicates = 0
    company = db.query(Company).filter(
    Company.hr_email == hr_email
).first()

    # Insert records
    for _, row in df.iterrows():

        

        # Skip duplicates
        existing = db.query(Employee).filter(
            Employee.company_id==company.id,
            Employee.email == row["email"]
        ).first()

        if existing:
           existing = db.query(Employee).filter(
    Employee.company_id == company.id,
    Employee.email == row["email"]
).first()

        if existing:
            existing.name = row["name"]
            existing.department = row["department"]
            existing.date_birth = pd.to_datetime(row["date_birth"]).date()
            existing.date_joining = pd.to_datetime(row["date_joining"]).date()

            continue
        print(df.columns.tolist())


        # print(row)
        # print("EMAIL =", row.get("email"))
       

        if not company:
            raise HTTPException(
        status_code=404,
        detail="Company not found")

        employee = Employee(
            name=row["name"],
            department=row["department"],
            email=row["email"],
            date_birth=pd.to_datetime(row["date_birth"]).date(),
            date_joining=pd.to_datetime(row["date_joining"]).date(),
            company_id=company.id
        )

        db.add(employee)
        added += 1

    db.commit()

    return {
        "success": True,
        "message": "Upload completed successfully",
        "employees_added": added,
        "duplicates_skipped": duplicates,
        "total_rows": len(df)
    }

# @app.post("/google-signup")
# def google_signup(
#     data: GoogleSignup,
#     db: Session = Depends(get_db)
# ):

#     company = Company(
#         company_name=data.company_name,
#         hr_name=data.hr_name,
#         hr_email=data.hr_email,
#         password_hash=None
#     )

#     db.add(company)
#     db.commit()

#     return {
#         "message":"Account created"
#     }
@app.get("/company/{email}")
def get_company(
    email: str,
    db: Session = Depends(get_db)
):
    return db.query(Company).filter(
        Company.hr_email == email
    ).first()

@app.post("/company")
def create_company(data: CompanyCreate, db: Session = Depends(get_db)):
    existing = db.query(Company).filter(
    Company.hr_email == data.hr_email).first()

    if existing:
        existing.company_name = data.company_name
        existing.hr_name = data.hr_name
    else:
        company = Company(
        company_name=data.company_name,
        hr_name=data.hr_name,
        hr_email=data.hr_email
    )
        db.add(company)

        db.commit()

  
        db.refresh(company)

    return {
        "message": "Company created successfully"
    }


@app.get("/dashboard-stats/{email}")
def get_stats(
    email: str,
    db: Session = Depends(get_db)
):
    print("Email",email)
    company = db.query(Company).filter(
    Company.hr_email == email
).first()
    if not company:
        raise HTTPException(
        status_code=404,
        detail="Company not found"
    )

    employees = db.query(Employee).filter(
    Employee.company_id == company.id
).all()
   
    total_no=len(employees)
    upcoming_b=0
    upcoming_a=0
    today=date.today()

    for emp in employees:
        if emp.date_birth.month==today.month and emp.date_birth.day>=today.day:
            upcoming_b=upcoming_b+1
        if emp.date_joining.month==today.month and emp.date_joining.day>=today.day:
            upcoming_a=upcoming_a+1
    return{
        "total_employees":total_no,
        "upcoming_b":upcoming_b,
        "upcoming_a":upcoming_a

    }

@app.post("/preview")
async def preview_file(file: UploadFile = File(...)):

    if file.filename.endswith(".csv"):
        df = pd.read_csv(file.file)

    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(file.file)

    else:
        return {"error": "Invalid file"}

    return {
        "total_rows": len(df),
        "columns": list(df.columns),
        "preview": df.head(6).fillna("").to_dict(orient="records")
     
    }

@app.get("/employees-dir")
def get_employees(db: Session = Depends(get_db)):

    employees = db.query(Employee).all()

    return [
        {
            "name": emp.name,
            "department": emp.department
        }
        for emp in employees
    ]

@app.get("/employees",response_model=list[E_response])
def show_emp(db:Session=Depends(get_db)):
    emps=db.query(Employee).all()
    return emps

@app.get("/upcoming-births/{email}",response_model=list[Upcoming_days])
def get_birth_emp(company_id:int,db:Session=Depends(get_db)):
    # company=db.query(Company).filter(company.hr_email==email).first()
    employees = db.query(Employee).filter(
    Employee.company_id == company_id
).all()
    
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
            upcoming.append({"name":emp.name,"department":emp.department,"event_type":"Birthday",
                             "birthday":next_birthday,"rem_days":rem_days,})
    return upcoming

from datetime import date

@app.get("/upcoming-birthdays/{email}")
def upcoming_birthdays(db: Session = Depends(get_db)):
    company=db.query(Company).filter(Company.hr_email==email).first()
    employees = db.query(Employee).filter(
    Employee.company_id == company.id
).all()

   
    upcoming = []

    for emp in employees:
        upcoming.append({
            "name": emp.name,
            "date_birth": emp.date_birth.strftime("%b %d")
        })

    upcoming.sort(key=lambda x: x["date_birth"])

    return upcoming[:5]



@app.get("/upcoming-anniverasries/{email}")
def upcoming_anniversaries(db: Session = Depends(get_db)):
    company=db.query(Company).filter(company.hr_email==email).first()
    employees = db.query(Employee).filter(
    Employee.company_id == company.id
).all()
   

    upcoming = []

    for emp in employees:
        upcoming.append({
            "name": emp.name,
            "date_birth": emp.date_joining.strftime("%b %d")
        })

    upcoming.sort(key=lambda x: x["date_joining"])

    return upcoming[:5]


@app.get("/work-anniversary/{email}",response_model=list[Upcoming_anniv])
def get_work_emp(company_id:int,db:Session=Depends(get_db)):
    # company=db.query(Company).filter(company.hr_email==email).first()
    emps = db.query(Employee).filter(
    Employee.company_id == company_id
).all()
  
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
             
             "event_type":"Anniversary",
             "anniversary":next_anniversary,
             "years_completed":years_completed,
             "rem_days":rem_days,
             })
    return upcoming  

@app.get("/events/{email}", response_model=list[Upcoming_events])
def show_all_events(
    email: str,
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(
        Company.hr_email == email
    ).first()

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    birthday = get_birth_emp(company.id,db)
    anniversary = get_work_emp(company.id,db)

    events = []

    for b in birthday:
        events.append({
            "name": b["name"],
            "department": b["department"],
            "event_type": "Birthday",
            "event_date": b["birthday"],
            "rem_days": b["rem_days"]
        })

    for a in anniversary:
        events.append({
            "name": a["name"],
            "department": a["department"],
            "event_type": "Anniversary",
            "event_date": a["anniversary"],
            "rem_days": a["rem_days"],
            "years_completed": a["years_completed"]
        })

    events.sort(key=lambda x: x["rem_days"])

    return events
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
    
@app.delete("/delete_rec")
def delrec(email:str,db:Session=Depends(get_db)):
    company=db.query(Company).filter(Company.hr_email==email).first()
    if company:
        db.delete(company)
        db.commit()
    else:
        raise HTTPException(status_code=404,detail="Company does not exist")


@app.get("/workspace/{email}")
def workspace_exists(email: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(
        Company.hr_email == email
    ).first()

    return {
        "exists": company is not None
    }

@app.post("/signup")
def signup(
    data: SignupRequest,
    db: Session = Depends(get_db)
):

    existing = db.query(Company).filter(
        Company.hr_email == data.hr_email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Workspace already exists"
        )

    company = Company(
        company_name=data.company_name,
        hr_name=data.hr_name,
        hr_email=data.hr_email,
        password_hash=bcrypt.hash(data.password)
    )

    db.add(company)
    db.commit()
    send_welcome_email(
    company.hr_email,
    company.hr_name,
    company.company_name
)
    return {
        "message": "Workspace created"
    }

@app.post("/login")
def login(data: LoginRequest,
          db: Session = Depends(get_db)):

    company = db.query(Company).filter(
        Company.hr_email == data.hr_email
    ).first()

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Workspace Not Found"
        )

    if company.password_hash is None:
        raise HTTPException(
            status_code=400,
            detail="Use Google Sign In"
        )

    if not bcrypt.verify(
        data.password,
        company.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    return {
        "hr_email": company.hr_email
    }

# @app.post("/google-login")
# def google_login(
#     data: GoogleLogin,
#     db: Session = Depends(get_db)
# ):

#     try:

#         info = id_token.verify_oauth2_token(
#             data.token,
#             requests.Request(),
#             "1074085637658-vkdfthucnjeotitbmnltap7fthbai7gq.apps.googleusercontent.com"
#         )

#         email = info["email"]
#         name = info["name"]

#         company = db.query(Company).filter(
#             Company.hr_email == email
#         ).first()

#         if company:

#             return {
#                 "new_user": False,
#                 "email": email,
#                 "name": name,
#                 "company_name": company.company_name
#             }

#         return {
#             "new_user": True,
#             "email": email,
#             "name": name
#         }

#     except Exception:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid Google Token"
#         )