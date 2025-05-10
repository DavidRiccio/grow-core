from django.db import models


# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
