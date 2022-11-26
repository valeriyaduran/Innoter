from accounts.services.user_service import UserService


class EmailRecipientsService:
    @staticmethod
    def get_email_recipients(request):
        page = UserService.get_current_page(request)
        recipients = [follower.email for follower in page.followers.all() if follower.email != page.owner.email]
        return recipients, page.owner
