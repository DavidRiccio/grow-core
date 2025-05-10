from django.contrib import admin

# Register your models here.
from .models import Order, Product


# Register your models here.
# Registrar Event (si tienes un modelo de eventos, aquí un ejemplo general)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
