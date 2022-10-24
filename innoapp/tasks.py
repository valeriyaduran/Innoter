from accounts.models import User
from accounts.services.user_service import UserService
from innotter.celery import app
from django.core.mail import send_mail


@app.task(name="send_email_after_new_post")
def send_email(user_post_email, username, request):
    page_followers = UserService.get_current_page(request).followers
    recipients = [follower.email for follower in page_followers.all() if follower.email != user_post_email]
    send_mail(subject='Innotter new post notification',
              message=f'Hi! User {username} has been added a new post! Check it in the app!',
              from_email=user_post_email,
              recipient_list=recipients,
              auth_user=user_post_email,
              auth_password='llrnrojdwuinxmej')