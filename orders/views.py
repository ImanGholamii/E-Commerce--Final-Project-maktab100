from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItem, OrderHistory
from products.models import Product
from django.conf import settings


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
