from django.urls import path

from . import views

name = 'orders'
urlpatterns = [
    path('add/', views.add_order, name='add-order'),
    path('get-earnings/', views.get_earnings, name='get-earnings'),
    path('<order_pk>/', views.order_detail, name='order-detail'),
    path('<order_pk>/pay-order/', views.pay_order, name='pay-order'),
    path('<order_pk>/cancell-order/', views.cancell_order, name='cancell-order'),
]
