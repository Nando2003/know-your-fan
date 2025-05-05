from django.db import models
from datetime import datetime


class ESportsNews(models.Model):
    title = models.CharField(max_length=255)
    source = models.URLField()

    image_url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    published_at = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.title