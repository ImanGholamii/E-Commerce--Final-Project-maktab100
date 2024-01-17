from django.db import models
from django.utils.translation import gettext_lazy as _
from products.models import Product


class ProductImageAlbum(models.Model):
    image = models.ImageField(upload_to='product_images/', verbose_name=_('Image'))
    is_default = models.BooleanField(default=False, verbose_name=_('Is Default'))

    @property
    def url(self):
        return self.image.url

    def __str__(self):
        image_name = self.image.name.split("/")[-1]
        return f"Image {self.id}: 😋 {image_name}"

    class Meta:
        verbose_name = _("Product Images Album")
        verbose_name_plural = _("Product Images Album")


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name=_('Product'))
    image = models.ForeignKey(ProductImageAlbum, on_delete=models.CASCADE, verbose_name=_('Image'))

    def __str__(self):
        return f"Image for {self.product.name}"

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Image")
