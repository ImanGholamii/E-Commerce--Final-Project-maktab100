from django.urls import path
from products.views import ProductDetailView, homeview, ProductListView, ProductCategoryListView, \
    ParentCategoryListView, ProductDetailApiView

urlpatterns = [
    path('', homeview, name='index'),
    path('products/', ProductListView.as_view(), name='list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('products/category/<str:category_name>/', ProductCategoryListView.as_view(), name='product_category'),
    path('products/parent-category/<str:category_name>/', ParentCategoryListView.as_view(), name='parent_category'),
    # API
    path('api/product/<int:pk>/', ProductDetailApiView.as_view(), name='product_detail_api'),

]
