from django.shortcuts import render, get_object_or_404, redirect
from .models import ShoppingCart, CartItem
from products.models import Product
from django.conf import settings


def set_shopping_cart_cookie(request, response):
    response.set_cookie(settings.CART_COOKIE_NAME, request.shopping_cart.id, max_age=settings.SESSION_COOKIE_AGE)
    return response


def create_cart_for_anonymous_user(request):
    cart = ShoppingCart.objects.create()
    return cart


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.COOKIES.get(settings.CART_COOKIE_NAME)
        if cart_id:
            cart, created = ShoppingCart.objects.get_or_create(id=cart_id)
        else:
            cart = create_cart_for_anonymous_user(request)
            request.COOKIES[settings.CART_COOKIE_NAME] = cart.id
    return cart


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = get_or_create_cart(request)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    response = redirect('product_list')
    set_shopping_cart_cookie(request, response)
    return response


def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = get_or_create_cart(request)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    if cart_item and cart_item.quantity > 0:
        cart_item.quantity -= 1
        cart_item.save()
    response = redirect('product_list')
    set_shopping_cart_cookie(request, response)
    return response


def view_cart(request):
    cart = get_or_create_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    context = {'cart_items': cart_items}
    return render(request, 'shopping_cart/view_cart.html', context)
