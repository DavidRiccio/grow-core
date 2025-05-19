from django.urls import path

from . import views

name = 'products'
urlpatterns = [
    path('', views.product_list, name='product-detail'),
    path('add/', views.add_product, name='add_product'),
    path('<int:product_pk>/edit/', views.edit_product, name='edit-product'),
    path('<int:product_pk>/delete/', views.delete_product, name='delete-product'),
]
