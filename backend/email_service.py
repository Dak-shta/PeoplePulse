import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv
import os

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def send_email(to_email, subject, body):

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email

    server = smtplib.SMTP("smtp.gmail.com",587)

    server.starttls()

    server.login(EMAIL,PASSWORD)

    server.send_message(msg)

    server.quit()



def send_welcome_email(email, hr_name, company_name):

    html = f"""
    <html>
    <body>
        <h2>🎉 Welcome to PeoplePulse!</h2>

        <p>Hi {hr_name},</p>

        <p>Your workspace for <b>{company_name}</b> has been created successfully.</p>

        <p>You can now:</p>

        <ul>
            <li>Upload employee data</li>
            <li>Track birthdays & anniversaries</li>
            <li>Manage employee engagement</li>
        </ul>

        <p>We're excited to have you onboard!</p>

        <br>
        <p>Team PeoplePulse</p>
    </body>
    </html>
    """
    try:
        msg = MIMEText(html, "html")
        msg["Subject"] = "Welcome to PeoplePulse 🎉"
        msg["From"] = EMAIL
        msg["To"] = email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Email failed for {email}:{e}")
        return False