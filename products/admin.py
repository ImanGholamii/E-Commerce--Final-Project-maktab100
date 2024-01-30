from django.contrib import admin
from django.utils.translation import activate
from .models import Brand, Category, Product, Discount, PromoCode, Comment, ParentChildComment, ProductCategory
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Status', {
            'fields': (('is_active', 'is_deleted'),),
            'classes': ('collapse',),
        }),
        ('Product', {
            'fields': ('name', 'description', 'price', 'brand',)
        }),
    )
    list_display = ('name', 'description', 'display_image', 'price', 'brand', 'display_categories')
    raw_id_fields = ('category',)
    # search_fields = ('id', 'name', 'brand', 'description')
    list_filter = ('is_active', 'is_deleted', 'name', 'brand', 'category')

    def display_image(self, obj):
        images = obj.images.all()
        if images:
            image_url = images[0].image.url if hasattr(images[0].image, 'url') else "No Image"
            if image_url:
                return format_html(
                    '<div style="text-align: center;"><img src="{}" width="100" height="100" /></div>'.format(
                        image_url))
        return "No Image"

    display_image.short_description = _('Image')

    def display_categories(self, obj):
        categories = obj.productcategory_set.all()
        return ', '.join([category.category.name for category in categories])

    display_categories.short_description = _('Categories')

    actions = ['switch_to_persian']

    def switch_to_persian(self, request, queryset):
        activate('fa')

    switch_to_persian.short_description = _('Switch to Persian')


# admin.site.register(Product, ProductAdmin)
admin.site.register(Category, admin.ModelAdmin)
admin.site.register(Comment, admin.ModelAdmin)
admin.site.register(ParentChildComment, admin.ModelAdmin)
admin.site.register(Discount, admin.ModelAdmin)
admin.site.register(PromoCode, admin.ModelAdmin)
admin.site.register(Brand, admin.ModelAdmin)
admin.site.register(ProductCategory, admin.ModelAdmin)
