from django.shortcuts import render, get_object_or_404, redirect
from orders.models import Order, OrderItem
from products.models import Product
from django.conf import settings
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from orders.serializers import OrderSerializer


class CreateShoppingCartView(CreateAPIView):
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:

            serializer.save(customer=self.request.user)
        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.save()
                session_key = self.request.session.session_key

            cart_data = self.request.session.get('cart', [])
            cart_data.append({'product_id': 1, 'quantity': 2})
            self.request.session['cart'] = cart_data

            self.request.session.save()


class ShoppingCartDetailView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Order.objects.get(customer=self.request.user, status='pending')


class AddProductToCartView(UpdateAPIView):
    serializer_class = OrderSerializer

    def get_object(self):
        if self.request.user.is_authenticated:
            return Order.objects.get_or_create(customer=self.request.user, status='pending')[0]
        else:
            order_id = self.request.session.get('order_id')
            if order_id:
                return get_object_or_404(Order, id=order_id, status='pending')
            else:
                order = Order(status='pending')
                order.save()

                self.request.session['order_id'] = order.id
                return order

    def perform_update(self, serializer):
        product_id = self.request.data.get('product_id')
        quantity = self.request.data.get('quantity')

        serializer.save()


# =======================================================================================
def set_order_cookie(request, response):
    response.set_cookie(settings.ORDER_COOKIE_NAME, request.order.id, max_age=settings.SESSION_COOKIE_AGE)
    return response


def create_order_for_anonymous_user(request):
    order = Order.objects.create()
    return order


def get_or_create_order(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user)
    else:
        order_id = request.COOKIES.get(settings.ORDER_COOKIE_NAME)
        if order_id:
            order, created = Order.objects.get_or_create(id=order_id)
        else:
            order = create_order_for_anonymous_user(request)
            request.COOKIES[settings.ORDER_COOKIE_NAME] = order.id
    return order


def add_to_order(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    order = get_or_create_order(request)
    order_item, item_created = OrderItem.objects.get_or_create(order=order, product=product)
    if not item_created:
        order_item.quantities += 1
        order_item.save()
    response = redirect('product_list')
    set_order_cookie(request, response)
    return response


def remove_from_order(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    order = get_or_create_order(request)
    order_item = OrderItem.objects.get(order=order, product=product)
    if order_item and order_item.quantities > 0:
        order_item.quantities -= 1
        order_item.save()
    response = redirect('product_list')
    set_order_cookie(request, response)
    return response


def view_order(request):
    order = get_or_create_order(request)
    order_items = OrderItem.objects.filter(order=order)
    context = {'order_items': order_items}
    return render(request, 'orders/view_order.html', context)
