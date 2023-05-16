from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail

@receiver(user_logged_in)
def notify_user_on_login(sender, user, request, **kwargs):
    email = '2100032245@kluniversity.in'
    subject = 'Login notification'
    message = f'Hello {user.username}, you have logged in to our website.'
    send_mail(subject, message, 'sandeepnaga763@example.com', [email], fail_silently=False)

