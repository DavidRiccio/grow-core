from django.urls import path

from . import views

name = 'products'
urlpatterns = [
    path('', views.product_list, name='product-detail'),
    path('<int:booking_id>/', views.product_detail, name='product-detail'),
]
