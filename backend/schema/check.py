from pydantic import BaseModel
from datetime import date
class E_create(BaseModel):
 
    name:str
    email:str
    department:str
    date_birth:date
    date_joining:date

class E_response(BaseModel):
    id:int
    name:str
    email:str
    department:str
    date_birth:date
    date_joining:date

class Upcoming_days(BaseModel):
    name:str
    department:str
    rem_days:int
    birthday:date

class Upcoming_anniv(BaseModel):
    name:str
    department:str
    rem_days:int
    years_completed:int
    anniversary:date

class Upcoming_events(BaseModel):
    name:str
    department:str
    event_type:str
    event_date:date
    rem_days:int
    years_completed:int | None=None



class CompanyCreate(BaseModel):
    company_name: str
    hr_name: str
    hr_email: str



class GoogleLogin(BaseModel):
    token:str




class SignupRequest(BaseModel):
    company_name: str
    hr_name: str
    hr_email: str
    password: str


class LoginRequest(BaseModel):
    hr_email: str
    password: str

class GoogleSignup(BaseModel):
    # company_name:str
    hr_name:str
    hr_email:str