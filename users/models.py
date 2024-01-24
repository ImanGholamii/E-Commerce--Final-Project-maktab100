from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _
from core.validators import Validator
from core.models import TimeStampBaseModel

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone, password, **extra_fields):
        if not email:
            raise ValueError(_("Email is required!"))
        if not phone:
            raise ValueError(_("Phone is required!"))
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_employee", True)

        if not extra_fields.get("is_active"):
            raise ValueError(_("Superuser must have is_active=True."))
        if not extra_fields.get("is_staff"):
            raise ValueError(_("Superuser must have is_staff=True."))
        if not extra_fields.get("is_superuser"):
            raise ValueError(_("Superuser must have is_superuser=True."))
        if not extra_fields.get("is_employee"):
            raise ValueError(_("Employee must have is_employee=True."))

        return self.create_user(email, phone, password, **extra_fields)


class User(AbstractUser, TimeStampBaseModel):
    username = models.CharField(
        max_length=150,
        unique=True,
        null=True, blank=True,
        verbose_name=_('Username')
    )

    email = models.EmailField(unique=True, verbose_name=_('Email'))
    phone = models.CharField(max_length=20, validators=[Validator.phone_validator()],
                             help_text=_("Enter your phone number."), verbose_name=_('Phone'), unique=True)
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Registration Date'))
    is_customer = models.BooleanField(default=True)
    is_employee = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Employee(TimeStampBaseModel):
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

    def __str__(self):
        return f"{self.user.username} employee type: {self.role}"


class Customer(TimeStampBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name=_('User'))
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True,
                                        verbose_name=_('Profile Picture'))
    is_subscribed = models.BooleanField(default=False, verbose_name=_('Is Subscribed'))  # to send news

    def __str__(self):
        return f"customer: {self.user.username[0].upper()}{self.user.username[1:]}  {10 * '_'}id: {self.user.id}"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name=_('User'))
    state = models.CharField(max_length=100, verbose_name=_('State'))
    city = models.CharField(max_length=100, verbose_name=_('City'))
    street = models.CharField(max_length=255, verbose_name=_('Street'))
    alley = models.CharField(max_length=50, null=True, verbose_name=_('Alley'))
    no = models.CharField(max_length=50, default=0, verbose_name=_('NO'))
    unit_number = models.CharField(max_length=50, default=0, verbose_name=_('Unit Number'))
    postal_code = models.CharField(max_length=20, verbose_name=_('Postal Code'))
    is_default = models.BooleanField(default=False, verbose_name=_('Is Default'))  # to choose default
    additional_info = models.TextField(blank=True, verbose_name=_('Additional Info'))


    def __str__(self):
        addresses_list = []

        if self.is_default:
            default_str = f"{self.user.username}, {self.state}, {self.city}, {self.street},{self.alley}, {self.no}, {self.unit_number}, {self.postal_code} (Default پیش فرض)"
            addresses_list.append(default_str)

        other_addresses = [
            f"{addr.user.username}, {addr.state}, {addr.city}, {addr.street}, {addr.alley}, {addr.no}, {addr.unit_number}, {addr.postal_code} (Default)" if addr.is_default else f"{addr.user.username}, {addr.state}, {addr.city}, {addr.street}, {addr.alley}, {addr.no}, {addr.unit_number}, {addr.postal_code}"
            for addr in self.user.addresses.filter(is_default=False)]

        addresses_list.extend(other_addresses)

        # return '\n'.join(addresses_list)
        for address in addresses_list:
            return str(address)


class UserProfile(TimeStampBaseModel):
    GENDER_CHOICES = [
        ('male', _('Male')),
        ('female', _('Female')),
        ('other', _('Other')),
    ]
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True,
                                        verbose_name=_('Profile Picture'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name=_('User'))
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name=_('Gender'), null=True)
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('Date of Birth'))
    bio = models.TextField(null=True, blank=True, verbose_name=_('Bio'))
    social_media = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Social Media'))
    interests = models.TextField(null=True, blank=True, verbose_name=_('Interests'))
    # addresses = models.ManyToManyField(Address, related_name='user_profiles', blank=True, verbose_name=_('Addresses'))
    addresses = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='user_profiles',null=True, blank=True, verbose_name=_('Address'))

    def __str__(self):
        return f"{self.user.username[0].upper()}{self.user.username[1:]}'s Profile"


class OtpCode(models.Model):
    email = models.EmailField()
    otp_code = models.PositiveIntegerField()
    created = models. DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email} otp code : {self.otp_code} - {self.created}"

# phone = models.CharField(max_length=20, validators=[
#         RegexValidator(regex=r'^(\+98|0)?9\d{9}$',
#         message=_("Phone number must be start with +98 or 0 in IR format."),code='invalid_IR_phone_number'), ],
#                              help_text=_("Enter your phone number."), verbose_name=_('Phone'), unique=True)

# phone = models.CharField(max_length=20, validators=[Validator.phone_validator()],
#                              help_text=_("Enter your phone number."), verbose_name=_('Phone'), unique=True)