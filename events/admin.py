from django.contrib import admin

from .models import Event


# Register your models here.
# Registrar Event (si tienes un modelo de eventos, aquí un ejemplo general)
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
