from datetime import date
from database.table import Base,Employee
from connect import SessionLocal

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
    

today = date.today()

month = today.month
day = today.day
employess=db.query(Employee).all
if (employee.date_birth.month == month and employee.date_birth.day == day):
    subject = "Happy Birthday 🎂"

    body = f"""
    Hello {employee.name},

Wishing you a very Happy Birthday.

Have a wonderful year ahead.

Regards,
PeoplePulse
"""

