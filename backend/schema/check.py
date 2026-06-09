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
    