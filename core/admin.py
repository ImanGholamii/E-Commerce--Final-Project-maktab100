from django.contrib import admin

# Register your models here.
admin.site.index_title = 'Fast Foodia'
admin.site.site_header = "Fast Foodia Admin 🍔"
admin.site.site_title = "🍔 Fast Foodia"

class AdminArea(admin.AdminSite):
    login_template = 'core/admin/login.html'