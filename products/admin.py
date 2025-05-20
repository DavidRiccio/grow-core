from django.contrib import admin

# Register your models here.
from .models import Product


# Register your models here.
# Registrar Event (si tienes un modelo de eventos, aquí un ejemplo general)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
