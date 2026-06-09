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
