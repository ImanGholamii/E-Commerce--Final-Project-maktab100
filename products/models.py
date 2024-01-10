from django.core.exceptions import ValidationError
from django.db import models
from core.models import LogicalBaseModel, TimeStampBaseModel
from django.contrib.auth import get_user_model


class Brand(LogicalBaseModel, TimeStampBaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Category(LogicalBaseModel, TimeStampBaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="category_images/")
    parent = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='child')

    def __str__(self):
        return self.name


class Product(LogicalBaseModel, TimeStampBaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ManyToManyField(Category, through='ProductCategory')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'custom_product_category'


class Discount(LogicalBaseModel, TimeStampBaseModel):
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed'),
    ]

    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    max_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product} - {self.discount_type} Discount"


class PromoCode(LogicalBaseModel, TimeStampBaseModel):
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='promo_codes')
    code = models.CharField(max_length=50)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return f'Promo Code: {self.code}'

    def clean(self):
        super().clean()
        if self.valid_from and self.valid_to and self.valid_from >= self.valid_to:
            raise ValidationError("valid_from must be before valid_to")


class Comment(LogicalBaseModel, TimeStampBaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ParentChildComment(LogicalBaseModel, TimeStampBaseModel):
    parent = models.ForeignKey(Comment, null=True, on_delete=models.SET_NULL, related_name='parent_comments')
    child = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='child_comments')
    depth = models.IntegerField()

    class Meta:
        unique_together = ('parent', 'child')
