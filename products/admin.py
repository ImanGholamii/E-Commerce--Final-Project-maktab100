from django.contrib import admin
from .models import Brand, Category, Product, Discount, PromoCode, Comment, ParentChildComment
from django.utils.html import format_html

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'brand', 'display_image', 'display_categories')
    raw_id_fields = ('category',)

    list_display = ('name', 'description', 'display_image', 'price', 'brand')

    def display_image(self, obj):
        images = obj.images.all()
        if images:
            image_url = images[0].image.url if hasattr(images[0].image, 'url') else "No Image"
            if image_url:
                return format_html('<img src="{}" width="100" height="100" />', image_url)
        return "No Image"

    display_image.short_description = 'Image'

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
