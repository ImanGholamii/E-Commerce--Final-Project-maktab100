from django.contrib import admin
from .models import Brand, Category, Product, Discount, PromoCode, Comment, ParentChildComment

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'brand', 'display_image', 'display_categories')
    raw_id_fields = ('category',)

    def display_image(self, obj):
        return '<img src="{url}" width="100" />'.format(url=obj.image.url)

    display_image.allow_tags = True

    def display_categories(self, obj):
        return ', '.join([category.name for category in obj.category.all()])

    display_categories.short_description = 'Categories'

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(ParentChildComment)
admin.site.register(Discount)
admin.site.register(PromoCode)
admin.site.register(Brand)
