from django.urls import path

from . import views

name = 'orders'
urlpatterns = [
    path('', views.order_list, name='order-list'),
    path('<order_pk>/', views.order_detail, name='order-detail'),
]
