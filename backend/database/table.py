from sqlalchemy.orm import declarative_base
from sqlalchemy import Column,Integer,String,Boolean,Date
Base=declarative_base()
class Employee(Base):
    __tablename__='employees'
    id=Column(Integer,primary_key=True)
    name=Column(String)
    email=Column(String)
    department=Column(String)
    date_birth=Column(Date)
    date_joining=Column(Date)
    company_id = Column(Integer)

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    company_name = Column(String)
    hr_name = Column(String)
    hr_email = Column(String)
    password_hash = Column(String)
