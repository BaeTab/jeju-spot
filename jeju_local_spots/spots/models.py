from django.db import models
from django.conf import settings

# Create your models here.

class SpotCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Spot(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=200)
    category = models.ForeignKey(SpotCategory, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_spots', blank=True)
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    
    def total_likes(self):
        return self.likes.count()

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

    def __str__(self):
        return self.title

class SpotImage(models.Model):
    spot = models.ForeignKey(Spot, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='spot_images/', blank=True, null=True)

    def __str__(self):
        return f"Image for {self.spot.title}"
