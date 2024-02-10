from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.views import APIView


class OrderApiVew(APIView):
    """ GET and POST Orders"""
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=OrderSerializer,
        responses={201: OrderSerializer()}
    )
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            instance.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OrderUpdateDeleteView(APIView):
    @swagger_auto_schema(
        request_body=OrderSerializer,
        responses={200: OrderSerializer()}
    )
    def put(self, request, pk):
        order_obj = Order.objects.get(id=pk)
        serializer = OrderSerializer(order_obj, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
