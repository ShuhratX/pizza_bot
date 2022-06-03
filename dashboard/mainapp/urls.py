from django.urls import path

from .views import (
    CategoryListView,
    SubCategoryListView,
    ProductListView,
    SubCategoryDetailView,
    ProductDetailView,
    CartCreateListView,
    UserDetailView,
    CartItemsView,
    CartClearView,
    UserCreateView,
    OrderCreateListView,
    OrderGetView,
    OrderProductView
    )

urlpatterns = [
    path('category', CategoryListView.as_view()),
    path('subcategories/<int:pk>/', SubCategoryListView.as_view()),
    path('subcategory/<int:pk>/', SubCategoryDetailView.as_view()),
    path('products/<int:pk>/', ProductListView.as_view()),
    path('product/<int:pk>/', ProductDetailView.as_view()),
    path('cart', CartCreateListView.as_view()),
    path('cart/<int:pk>/', CartItemsView.as_view()),
    path('clearcart/<int:pk>/', CartClearView.as_view()),
    path('order', OrderCreateListView.as_view()),
    path('orderproduct', OrderProductView.as_view()),
    path('order/last/<int:pk>/', OrderGetView.as_view()),
    path('user/<int:pk>/', UserDetailView.as_view()),
    path('user', UserCreateView.as_view()),
]
