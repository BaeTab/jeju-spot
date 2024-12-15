from django.db import models
from django.conf import settings
from spots.models import Spot
from events.models import Event
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    RATING_CHOICES = [
        (1, '매우 나쁨'),
        (2, '나쁨'),
        (3, '보통'),
        (4, '좋음'),
        (5, '매우 좋음')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    content = models.TextField(max_length=1000)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=RATING_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.spot:
            return f"{self.user.username}'s review for {self.spot.title}"
        elif self.event:
            return f"{self.user.username}'s review for {self.event.title}"
        return f"Review by {self.user.username}"

    class Meta:
        unique_together = [['user', 'spot'], ['user', 'event']]
        ordering = ['-created_at']
