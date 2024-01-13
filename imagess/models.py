from django.db import models
from django.utils.translation import gettext_lazy as _
from products.models import Product


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name=_('Product'))
    image = models.ImageField(upload_to='product_images/', verbose_name=_('Image'))
    is_default = models.BooleanField(default=False, verbose_name=_('Is Default'))

    def __str__(self):
        return f"Image for {self.product.name}"

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
