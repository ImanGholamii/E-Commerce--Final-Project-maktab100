from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import ProductImageAlbum, ProductImages

@admin.register(ProductImageAlbum)
class ProductImageAlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_thumbnail', 'is_default')
    list_display_links = ('id', 'image_thumbnail')

    def image_thumbnail(self, obj):
        return mark_safe('<img src="{}" width="50" height="50" />'.format(obj.url))

    image_thumbnail.short_description = 'Image'

@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image_thumbnail')
    list_display_links = ('id', 'product', 'image_thumbnail')

    def image_thumbnail(self, obj):
        return mark_safe('<img src="{}" width="50" height="50" />'.format(obj.image.url))

    image_thumbnail.short_description = 'Image'
