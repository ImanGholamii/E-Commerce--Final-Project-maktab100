from django.contrib import admin
from .models import User, Employee, Customer
# Register your models here.
admin.site.register(User, Employee, Customer,)