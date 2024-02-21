import time

from django.core.mail import send_mail
from django.http import HttpResponse
from users.models import OtpCode


def send_otp_code(recipient, subject, message):
    send_mail(
        subject,
        message,
        'sharlotimi@gmail.com',
        [recipient],
        fail_silently=False,
    )
    # return HttpResponse('Done')


# from celery import shared_task
# from time import sleep
#
# @shared_task
# def otp_cleaner():
#     time.sleep(120)
#     code = OtpCode.objects.all()
#     code.delete()
#     print("OTP deleted successfully!")