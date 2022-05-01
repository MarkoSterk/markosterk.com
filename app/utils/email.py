import os
from flask import current_app
from flask_mail import Message
from app import mail

"""
Mrthod for sending emails from the app.
It relies on the sendgrid service.
Visit https://sendgrid.com/ for more information
"""

def sendEmailToken(recipient, subject, message):
    msg = Message(subject,
                  sender=current_app.config['MAIL_SENDGRID_SENDER'],
                  recipients=[recipient])
    msg.body = message
    msg.html = f"<b>{message}</b>"

    try:
        mail.send(msg)
    except Exception as e:
        print(e.body)


def sendContactEmail(message, email, name, surname):
    msg = Message('Contact via markosterk.com',
                  sender=current_app.config['MAIL_SENDGRID_SENDER'],
                  recipients=['marko.sterk@um.si'])
    
    msg.body = f'{message} \n\n from: {name} {surname}, {email}'
    msg.html = f"{message} <br><br> from: {name} {surname}, {email}"

    try:
        mail.send(msg)
    except Exception as e:
        print(e.body)
