from django.urls import path
from products.views import ProductDetailView, HomeView, ProductListView, ProductCategoryListView, ParentCategoryListView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('products/', ProductListView.as_view(), name='list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('products/category/<str:category_name>/', ProductCategoryListView.as_view(), name='product_category'),
    path('products/parent-category/<str:category_name>/', ParentCategoryListView.as_view(), name='parent_category'),
]
