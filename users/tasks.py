from config.celery import app
from django.core.mail import send_mail

@app.task
def send_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        'xoliqberdiyevbehruz6@gmail.com',
        recipient_list
    )