import os
from email.message import EmailMessage
import ssl
import smtplib


def sendmail(email_receiver:str , subject, body):
    email_sender = "keynova.auto@gmail.com"
    email_password = "qscu furx vwzt tago"

    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.add_alternative(body, subtype="html")  # Add HTML content

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as smtp:
        smtp.login(email_sender,email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
