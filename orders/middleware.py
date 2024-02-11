# middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from users.models import Customer


class SetGuestCookieMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            if 'guest_user' not in request.COOKIES:
                request.COOKIES['guest_user'] = 'guest'

# class RedirectGuestToLoginMiddleware(MiddlewareMixin):
#     def process_view(self, request, view_func, view_args, view_kwargs, check_cart=None):
#         if not request.user.is_authenticated:
#             if view_func == check_cart.post:
#                 return redirect(reverse('login'))
# class MergeGuestCartMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         if request.user.is_authenticated:
#             if 'guest_user' in request.COOKIES:
#                 guest_customer_id = request.COOKIES['guest_user']
#                 try:
#                     guest_customer = Customer.objects.get(id=guest_customer_id)
#                 except Customer.DoesNotExist:
#                     return
#
#                 user = request.user
#
#                 guest_cart_items = guest_customer.order_items.all()
#                 for product in guest_cart_items:
#                     product.customer = user
#                     product.save()
#
#                 guest_customer.delete()