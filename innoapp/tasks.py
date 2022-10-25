from accounts.services.user_service import UserService
from innotter import settings
from innotter.celery import app
from innoapp.email_message_params import EMAIL_SUBJECT, EMAIL_BODY
from django.core.mail import send_mail


@app.task(name="send_email_after_new_post")
def send_email(user_post_email, page_owner_username, request):
    page_followers = UserService.get_current_page(request).followers
    recipients = [follower.email for follower in page_followers.all() if follower.email != user_post_email]

    send_mail(
        subject=EMAIL_SUBJECT,
        message=EMAIL_BODY.format(page_owner_username=page_owner_username),
        from_email=user_post_email,
        recipient_list=recipients,
        auth_user=settings.EMAIL_HOST_USER,
        auth_password=settings.EMAIL_HOST_PASSWORD,
    )
