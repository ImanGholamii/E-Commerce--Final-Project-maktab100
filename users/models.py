from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _
from core.validators import Validator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("Email is required!"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_active"):
            raise ValueError(_("Superuser must have is_active=True."))
        if not extra_fields.get("is_staff"):
            raise ValueError(_("Superuser must have is_staff=True."))
        if not extra_fields.get("is_superuser"):
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    GENDER_CHOICES = [
        ('male', _('Male')),
        ('female', _('Female')),
        ('other', _('Other')),
    ]
    USER_TYPE_CHOICES = [
        ('customer', _('Customer')),
        ('employee', _('Employee')),
    ]
    username = models.CharField(
        max_length=150,
        unique=True,
        null=True, blank=True,
        verbose_name=_('Username')
    )
    user_type = models.CharField(max_length=100, choices=USER_TYPE_CHOICES, default='customer',
                                 verbose_name=_('User Type'))
    email = models.EmailField(unique=True, verbose_name=_('Email'))
    phone = models.CharField(max_length=20, validators=[Validator.phone_validator()],
                             help_text=_("Enter your phone number."), verbose_name=_('Phone'))
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name=_('Gender'))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('Date of Birth'))
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Registration Date'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Employee(models.Model):
    ROLE_CHOICES = [
        ('manager', _('Manager')),
        ('staff', _('Staff')),
        ('customer_support', _('Customer Support')),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name=_('User'))
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, verbose_name=_('Role'))
    is_manager = models.BooleanField(default=False, verbose_name=_('Is Manager'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Is Staff'))
    is_customer_support = models.BooleanField(default=False, verbose_name=_('Is Customer Support'))


# ...

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name=_('User'))
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True,
                                        verbose_name=_('Profile Picture'))
    is_subscribed = models.BooleanField(default=False, verbose_name=_('Is Subscribed'))  # to send news


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name=_('User'))
    state = models.CharField(max_length=100, verbose_name=_('State'))
    city = models.CharField(max_length=100, verbose_name=_('City'))
    street = models.CharField(max_length=255, verbose_name=_('Street'))
    alley = models.CharField(max_length=50, verbose_name=_('Alley'))
    no = models.CharField(max_length=50, verbose_name=_('NO'))
    unit_number = models.CharField(max_length=50, verbose_name=_('Unit Number'))
    postal_code = models.CharField(max_length=20, verbose_name=_('Postal Code'))
    is_default = models.BooleanField(default=False, verbose_name=_('Is Default'))  # to choose default
    additional_info = models.TextField(blank=True, verbose_name=_('Additional Info'))


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name=_('User'))
    bio = models.TextField(verbose_name=_('Bio'))
    social_media = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Social Media'))
    interests = models.TextField(null=True, blank=True, verbose_name=_('Interests'))
    addresses = models.ManyToManyField(Address, related_name='user_profiles', blank=True, verbose_name=_('Addresses'))

    def __str__(self):
        return f"{self.user.username[0].upper()}{self.user.username[1:]}'s Profile"
