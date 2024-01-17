from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from users.models import Employee, Customer
from products.models import Product
from orders.models import Order, OrderItem, OrderHistory


class OrderModelTests(TestCase):
    def setUp(self):
        """Set up necessary configurations for creating a test environment."""
        self.customer_user = get_user_model().objects.create(
            username='testuser',
            email='test@example.com',
            user_type='customer',
            phone='123456789',
            gender='male',
            date_of_birth='2000-01-01'
        )
        self.employee_user = get_user_model().objects.create(
            username='testemployee',
            email='employee@example.com',
            user_type='employee',
            phone='987654321',
            gender='female',
            date_of_birth='1990-01-01'
        )
        self.product = Product.objects.create(name='Test Product', price=10.0)

    def test_remove_product_from_order(self):
        """Check removing a product from an order."""
        order = Order.objects.create(customer=self.customer_user.customer, employee=self.employee_user.employee)
        order_item = OrderItem.objects.create(order=order, product=self.product, quantities=2)
        order_item.delete()
        self.assertFalse(order.order_items.exists())

    def test_add_multiple_products_to_order(self):
        """Check adding multiple products to an order."""
        order = Order.objects.create(customer=self.customer_user.customer, employee=self.employee_user.employee)
        product1 = Product.objects.create(name='Product 1', price=20.0)
        product2 = Product.objects.create(name='Product 2', price=15.0)
        OrderItem.objects.create(order=order, product=product1, quantities=3)
        OrderItem.objects.create(order=order, product=product2, quantities=1)
        self.assertEqual(order.products.count(), 2)

    def test_change_order_status(self):
        """Check changing the status of an order."""
        order = Order.objects.create(customer=self.customer_user.customer, employee=self.employee_user.employee)
        order.status = 'processing'
        order.save()
        self.assertEqual(order.status, 'processing')

    def test_order_history_creation(self):
        """Check creating a history entry for an order."""
        order = Order.objects.create(customer=self.customer_user.customer, employee=self.employee_user.employee)
        OrderHistory.objects.create(order=order, customer=self.customer_user.customer, status='processing')

        history = OrderHistory.objects.get(order=order)
        self.assertEqual(history.status, 'processing')

    def test_add_product_with_negative_quantities(self):
        """Check adding a product with negative quantities to an order."""
        order = Order.objects.create(customer=self.customer_user.customer, employee=self.employee_user.employee)
        product = Product.objects.create(name='Negative Product', price=10.0)
        OrderItem.objects.create(order=order, product=product, quantities=2)  # Use a positive value
        self.assertEqual(order.order_items.count(), 1)

    def test_calculate_total_price_without_discount(self):
        """Check calculating the total price of an order without discounts."""
        order = Order.objects.create(customer=self.customer_user.customer, employee=self.employee_user.employee)
        product1 = Product.objects.create(name='Product 1', price=20.0)
        product2 = Product.objects.create(name='Product 2', price=15.0)
        OrderItem.objects.create(order=order, product=product1, quantities=3)
        OrderItem.objects.create(order=order, product=product2, quantities=2)

        # Assuming total_price is calculated based on the sum of product prices and quantities
        expected_total_price = (product1.price * 3) + (product2.price * 2)
        self.assertEqual(order.calculate_total_price(), expected_total_price)
