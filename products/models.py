from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from core.models import LogicalBaseModel, TimeStampBaseModel
from django.core.exceptions import ValidationError


class Brand(LogicalBaseModel, TimeStampBaseModel):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))

    def __str__(self):
        return self.name


class Category(LogicalBaseModel, TimeStampBaseModel):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    image = models.ImageField(upload_to="category_images/", verbose_name=_('Image'))
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='child',
                               verbose_name=_('Parent'))

    class Meta:
        verbose_name_plural = "categories"
    def get_full_path(self):
        path = [self.name]
        current_category = self

        while current_category.parent:
            path.insert(0, current_category.parent.name)
            current_category = current_category.parent

        return ' > '.join(path)

    def __str__(self):
        return self.name


class Product(LogicalBaseModel, TimeStampBaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    category = models.ManyToManyField(Category, through='ProductCategory', verbose_name=_('Category'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price'))
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Brand'))

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Category'))

    class Meta:
        db_table = 'custom_product_category'
        verbose_name = _('Product Category')
        verbose_name_plural = _('Product Categories')

    def __str__(self):
        return f"{self.category.parent} >> {self.category.name} >> {self.product}"


class Discount(LogicalBaseModel, TimeStampBaseModel):
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', _('Percentage')),
        ('fixed', _('Fixed')),
    ]

    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, verbose_name=_('Discount Type'))
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Value'))
    max_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Max Amount'))

    def __str__(self):
        return f"{self.product} - {self.discount_type} Discount"


class PromoCode(LogicalBaseModel, TimeStampBaseModel):
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='promo_codes',
                                 verbose_name=_('Discount'))
    code = models.CharField(max_length=50, verbose_name=_('Code'))
    valid_from = models.DateTimeField(verbose_name=_('Valid From'))
    valid_to = models.DateTimeField(verbose_name=_('Valid To'))

    def __str__(self):
        return f'Promo Code: {self.code}'

    def clean(self):
        super().clean()
        if self.valid_from and self.valid_to and self.valid_from >= self.valid_to:
            raise ValidationError(_("valid_from must be before valid_to"))


class Comment(LogicalBaseModel, TimeStampBaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('User'))
    content = models.TextField(verbose_name=_('Content'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))


class ParentChildComment(LogicalBaseModel, TimeStampBaseModel):
    parent = models.ForeignKey(Comment, null=True, on_delete=models.SET_NULL, related_name='parent_comments',
                               verbose_name=_('Parent'))
    child = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='child_comments', verbose_name=_('Child'))
    depth = models.IntegerField(verbose_name=_('Depth'))

    class Meta:
        unique_together = ('parent', 'child')
        verbose_name = _('Parent-Child Comment')
        verbose_name_plural = _('Parent-Child Comments')
