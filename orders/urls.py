from django.urls import path

from . import views

name = 'orders'
urlpatterns = [
    path('', views.user_order_list, name='user_order_list'),
    path('add/', views.add_order, name='add-order'),
    path('get-earnings/', views.get_earnings, name='get-earnings'),
    path('<order_pk>/', views.order_detail, name='order-detail'),
    path('<order_pk>/pay-order/', views.pay_order, name='pay-order'),
    path('<order_pk>/cancel-order/', views.cancel_order, name='cancel-order'),
    path('<order_pk>/delete/', views.delete_order, name='delete-order'),
    path('<order_pk>/add-product/', views.add_product_to_order, name='add-product'),

]
