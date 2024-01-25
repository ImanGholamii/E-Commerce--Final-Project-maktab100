from django.core.mail import send_mail
from django.http import HttpResponse


def send_otp_code(recipient, subject, message):
    send_mail(
        subject,
        message,
        'sharlotimi@gmail.com',
        [recipient],
        fail_silently=False,
    )
    # return HttpResponse('Done')
