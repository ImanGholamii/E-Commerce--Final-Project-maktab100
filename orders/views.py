from django.shortcuts import get_object_or_404, render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from products.models import Product
from users.models import Customer, User
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.views import APIView


class OrderApiVew(APIView):
    """ GET and POST Orders"""

    def get(self, request):
        if request.user.is_superuser:
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(customer=request.user.customer)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=OrderSerializer,
        responses={201: OrderSerializer()}
    )
    def post(self, request):
        if not request.user.is_authenticated:
            if 'guest_user' not in request.COOKIES:
                request.COOKIES['guest_user'] = User.objects.get(id=45)
                print(request.COOKIES)
                serializer = OrderSerializer(data=request.data)
                if serializer.is_valid():
                    instance = serializer.save()
                    instance.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderUpdateDeleteView(APIView):
    swagger = swagger_auto_schema(
        request_body=OrderSerializer,
        responses={200: OrderSerializer()}
    )

    def get(self, request, pk):
        if request.user.is_superuser:
            order_obj = Order.objects.filter(id=pk)
        else:
            order_obj = Order.objects.filter(customer=request.user.customer)
        serializer = OrderSerializer(order_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger
    def put(self, request, pk):
        if request.user.is_superuser:
            order_obj = Order.objects.get(id=pk)
        else:
            order_obj = Order.objects.get(customer=request.user.customer)
        serializer = OrderSerializer(order_obj, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger
    def delete(self, request, pk):
        try:
            if request.user.is_superuser:
                order_obj = Order.objects.get(id=pk)
            else:
                order_obj = Order.objects.get(customer=request.user.customer)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        order_obj.delete()
        return Response({"message": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class OrderItemApiView(APIView):
    """GET and POST order items"""

    def get(self, request):
        order_item = OrderItem.objects.filter(product__is_deleted=False)
        serializer = OrderItemSerializer(order_item, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=OrderItemSerializer,
        responses={201: OrderItemSerializer()}
    )
    def post(self, request):
        """Add or Remove items form Order(cart)"""
        product_id = request.data.get('product')
        quantities = request.data.get('quantities', 0)
        print('product_id= ', product_id, quantities)
        product = get_object_or_404(Product, id=product_id)

        if request.user.is_authenticated:
            user_id = request.user.id
            print('auth_user_id=', user_id)

        else:
            guest_user_id = request.COOKIES.get('guest_user')
            print(guest_user_id)
            if guest_user_id == '45':
                # guest_user_id = 45
                user_id = int(guest_user_id)
                print('guest_customer.id = ', user_id)
        order, created = Order.objects.get_or_create(customer=user_id, status='pending')

        print(order)

        order_item = order.order_items.filter(product=product).first()
        if order_item:
            order_item.quantities += quantities
            if order_item.quantities <= 0:
                order_item.delete()
            else:
                order_item.save()
            serializer = OrderItemSerializer(order_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = OrderItemSerializer(data={'product': product_id, 'order': order.id, 'quantities': quantities})
            if serializer.is_valid():
                instance = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def increase_quantity(self, request, pk=None):
        """Increase quantity of an order item"""
        order_item = self.get_object()
        order_item.quantities += 1
        order_item.save()
        serializer = self.get_serializer(order_item)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def decrease_quantity(self, request, pk=None):
        """Decrease quantity of an order item"""
        order_item = self.get_object()
        if order_item.quantities > 1:
            order_item.quantities -= 1
            order_item.save()
            serializer = self.get_serializer(order_item)
            return Response(serializer.data)
        else:

            return Response({"error": "Cannot decrease quantity further"}, status=status.HTTP_400_BAD_REQUEST)


class OrderItemUpdateDeleteApiView(APIView):
    """Update and Delete items of an Order"""
    swagger = swagger_auto_schema(
        request_body=OrderItemSerializer,
        responses={200: OrderItemSerializer()}
    )

    def get(self, request, pk):
        order_item = OrderItem.objects.filter(id=pk)
        # order_item = OrderItem.objects.filter(product__is_deleted=False)
        serializer = OrderItemSerializer(order_item, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger
    def put(self, request, pk):
        item = OrderItem.objects.get(id=pk)
        serialize = OrderItemSerializer(item, data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=status.HTTP_200_OK)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            item = OrderItem.objects.get(id=pk)
            item.delete()
            return Response({"data": f"Item deleted successfully."},
                            status=status.HTTP_204_NO_CONTENT)
        except OrderItem.DoesNotExist:
            return Response({'data': "Item doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)


def check_cart(request):
    """to show all ordered items in template"""
    # items = OrderItem.objects.all()
    items = OrderItem.objects.filter(order__customer=request.user.id, is_deleted=False)
    print('Customer: ', request.user)
    total_quantity = sum(item.quantities for item in items)
    total_price = sum(item.product.price * item.quantities for item in items)
    context = {
        'items': items,
        'total_quantity': total_quantity,
        'total_price': total_price,
    }
    return render(request, 'check_cart.html', context=context)


# ==================
class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
