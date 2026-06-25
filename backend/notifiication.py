from datetime import date



from connect import SessionLocal
from database.table import Employee

from email_service import send_email


def check_birthdays():

    db = SessionLocal()

    try:
        today = date.today()

        month = today.month
        day = today.day

        employees = db.query(Employee).all()
        print("birthday jjob stated")

        for employee in employees:
            print(
        f"Name: {employee.name}, "
        f"Email: {employee.email}, "
        f"DOB: {employee.date_birth}"
    )

            if (
                 employee.date_birth.month == month
                 and employee.date_birth.day == day):
                if not employee.email or "@" not in employee.email:
                    print(f"Invalid email for {employee.name}")
                    continue
            

                subject = "Happy Birthday 🎂"

                body = f"""
Hello {employee.name},

Wishing you a very Happy Birthday.

Have a wonderful year ahead.

Regards,
PeoplePulse
"""

                send_email(
                    employee.email,
                    subject,
                    body
                )

                print(f"Birthday email sent to {employee.name}")
    finally:
         db.close()
def check_anniversary():
    db = SessionLocal()

    try:
        today = date.today()

        month = today.month
        day = today.day

        employees = db.query(Employee).all()
        print("anniiversary job started")

        for employee in employees:
            print(
        f"Name: {employee.name}, "
        f"Email: {employee.email}, "
        f"Joining: {employee.date_joining}"
    )

            
            if ( employee.date_joining.month == month and employee.date_joining.day == day):
                if not employee.email or "@" not in employee.email:
                        print(f"Invalid email for {employee.name}")
                        continue
                today = date.today()

                years_completed = today.year - employee.date_joining.year
                if years_completed <= 0:
                        continue

            

                if years_completed == 1:
                    msg = "Congratulations on completing your first year with us."
                elif years_completed == 5:
                    msg = "Congratulations on reaching the remarkable 5-year milestone."
                elif years_completed == 10:
                    msg = "A decade of dedication and excellence. Thank you!"
                else:
                    msg = f"Congratulations on completing {years_completed} years with us."               

                subject = "Happy Work Anniversary 🎉"

                body = f"""
Hello {employee.name},

{msg}

Your dedication, hard work, and commitment have made a meaningful impact on the organization.

Thank you for being an important part of our journey.

Wishing you continued success and many more milestones ahead.   
                
Regards,
PeoplePulse
"""

                send_email(
                    employee.email,
                    subject,
                    body
                )

                print(f"Anniversary email sent to {employee.name}")

                

    finally:
        db.close()