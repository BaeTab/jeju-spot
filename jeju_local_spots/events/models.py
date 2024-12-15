from django.db import models
from django.conf import settings
from spots.models import Spot

# Create your models here.

class Event(models.Model):
    TYPES = [
        ('discount', '할인'),
        ('festival', '축제'),
        ('exhibition', '전시회'),
        ('concert', '공연'),
        ('other', '기타')
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=TYPES)
    related_spot = models.ForeignKey(Spot, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    discount_percentage = models.IntegerField(null=True, blank=True)
    contact_info = models.CharField(max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title

    def is_active(self):
        from django.utils import timezone
        return self.start_date <= timezone.now() <= self.end_date

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def add_like(self):
        self.likes_count += 1
        self.save(update_fields=['likes_count'])

    def remove_like(self):
        if self.likes_count > 0:
            self.likes_count -= 1
            self.save(update_fields=['likes_count'])
