from django.db import models
from users.models import Customer, Employee
from products.models import Product, Brand, Category
from core.models import TimeStampBaseModel, LogicalBaseModel
from django.utils.translation import gettext_lazy as _


class Order(TimeStampBaseModel, LogicalBaseModel):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    ]
    products = models.ManyToManyField(Product, through='OrderItem')
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='employee_orders',
                                 verbose_name=_('Employee'))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_orders',
                                 verbose_name=_('Customer'))
    order_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Order Date'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name=_('Status'))

    def __str__(self):
        return f"Order #{self.id} - {self.status}"


class OrderItem(TimeStampBaseModel, LogicalBaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name=_('Order'))
    quantities = models.PositiveIntegerField(verbose_name=_('Quantities'))

    def __str__(self):
        return f"Order #{self.order.id} - {self.product.name} - Quantity: {self.quantities}"
    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Item")

class OrderHistory(TimeStampBaseModel, LogicalBaseModel):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_history',
                              verbose_name=_('Order'))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_('Customer'))
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES, verbose_name=_('Status'))
    time = models.DateTimeField(auto_now_add=True, verbose_name=_('Created Time'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('Modified Time'))

    def __str__(self):
        return f"Order #{self.order.id} - Status: {self.status} - Time: {self.time}"
