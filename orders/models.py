from django.db import models
from users.models import Customer, Employee
from products.models import Product
from core.models import TimeStampBaseModel, LogicalBaseModel
class Order(TimeStampBaseModel, LogicalBaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='employee_orders')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_orders')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order #{self.id} - {self.status}"

class OrderItem(TimeStampBaseModel, LogicalBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Order #{self.order.id} - {self.product.name} - Quantity: {self.quantity}"

class OrderHistory(TimeStampBaseModel, LogicalBaseModel):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='history')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    time = models.DateTimeField(auto_now_add=True, auto_now=True)

    def __str__(self):
        return f"Order #{self.order.id} - Status: {self.status} - Timestamp: {self.time}"
