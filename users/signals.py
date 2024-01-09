from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Employee, Customer, UserProfile
from rest_framework.authtoken.models import Token
from django.conf import settings

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'employee':
            profile = UserProfile.objects.create(user=instance)
            Employee.objects.create(user=instance, role='staff')
        elif instance.user_type == 'customer':
            profile = UserProfile.objects.create(user=instance)
            Customer.objects.create(user=instance)



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
