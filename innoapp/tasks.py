from accounts.services.user_service import UserService
from accounts.models import User
from innotter import settings
from innotter.celery import app
from innoapp.email_message_params import EMAIL_SUBJECT, EMAIL_BODY
from django.core.mail import send_mail


@app.task(name="send_email_after_new_post")
def send_email(recipients, page_owner):
    send_mail(
        subject=EMAIL_SUBJECT,
        message=EMAIL_BODY.format(page_owner_username=page_owner["username"]),
        from_email=page_owner["email"],
        recipient_list=recipients,
        auth_user=settings.EMAIL_HOST_USER,
        auth_password=settings.EMAIL_HOST_PASSWORD,
    )
