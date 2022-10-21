from accounts.models import User
from innotter.celery import app
from django.core.mail import send_mail


@app.task(name="send_email_after_new_post")
def send_email(user_post_email, username):
    emails = User.objects.all().values('email').exclude(user_post_email)

    send_mail(subject='New post notification',
              message=f'Hi! {username} has been added a new post! Check it in the app!',
              from_email=user_post_email,
              recipient_list=emails)