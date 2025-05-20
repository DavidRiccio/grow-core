from django.urls import path

from . import views

name = 'orders'
urlpatterns = [
    path('', views.order_list, name='order-list'),
    path('add/', views.add_order, name='add-order'),
    path('<order_pk>/', views.order_detail, name='order-detail'),
    path('<order_pk>/delete/', views.delete_order, name='delete-order'),
    path('<order_pk>/add-product/', views.add_product_to_order, name='add-product-to-order'),
]
