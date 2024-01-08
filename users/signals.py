from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Employee, Customer
from rest_framework.authtoken.models import Token
from django.conf import settings

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff:
            Employee.objects.create(user=instance, role='staff')  # Set the default role for staff
        elif not instance.is_superuser:
            Customer.objects.create(user=instance)  # Create a customer profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
