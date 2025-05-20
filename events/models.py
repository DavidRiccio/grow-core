from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    image = models.ImageField(
        upload_to='media/events_images/',
        default='no_event.png',
        blank=True,
        null=True,
    )
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} on {self.date} at {self.location}'
