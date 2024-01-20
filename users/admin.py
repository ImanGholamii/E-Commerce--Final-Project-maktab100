from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from users.models import User, Employee, Customer, UserProfile, Address
from django.utils.translation import gettext_lazy as _


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'is_customer', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('id', 'username', 'email', 'phone')
    list_filter = ('is_customer', 'is_employee', 'is_active', 'is_staff', 'date_joined')
    ordering = ('-date_joined',)


class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'city', 'state', 'street', 'postal_code', 'is_default')
    search_fields = ('id', 'user__username', 'city', 'state', 'street', 'postal_code', 'is_default')
    list_filter = ('is_default',)


admin.site.register(User, UserAdmin)
admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(UserProfile)
admin.site.register(Address, AddressAdmin)

admin.site.unregister(Group)  # این کد گروه‌های از پیش تعریف شده django را از admin panel حذف می‌کند

Group.objects.get_or_create(name=_('Customer'))
Group.objects.get_or_create(name=_('Employee'))

customer_group = Group.objects.get(name=_('Customer'))
employee_group = Group.objects.get(name=_('Employee'))

permissions = Permission.objects.filter(name__icontains='product')
customer_group.permissions.add(*permissions)

all_permissions = Permission.objects.all()
employee_group.permissions.set(all_permissions)
