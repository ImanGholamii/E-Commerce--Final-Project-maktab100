from django.shortcuts import render, get_object_or_404, redirect
from .models import ShoppingCart, CartItem
from products.models import Product


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('product_list')

def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    if cart_item and cart_item.quantity > 0:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('product_list')
def view_cart(request):
    cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    context = {'cart_items': cart_items}
    return render(request, 'view_cart.html', context)
