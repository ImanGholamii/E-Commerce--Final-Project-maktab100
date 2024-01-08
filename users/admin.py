from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from users.models import User, Employee, Customer, UserProfile
# Register your models here.
admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(UserProfile)

# admin.site.unregister(Group)  # این کد گروه‌های از پیش تعریف شده را از admin panel حذف می‌کند

Group.objects.get_or_create(name='Customer')
Group.objects.get_or_create(name='Employee')

customer_group = Group.objects.get(name='Customer')
employee_group = Group.objects.get(name='Employee')

permissions = Permission.objects.filter(name__icontains='product')
customer_group.permissions.add(*permissions)

all_permissions = Permission.objects.all()
employee_group.permissions.set(all_permissions)