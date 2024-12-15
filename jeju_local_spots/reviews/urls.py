from django.urls import path
from . import views

urlpatterns = [
    path('spot/<int:spot_id>/review/', views.create_spot_review, name='create-spot-review'),
    path('event/<int:event_id>/review/', views.create_event_review, name='create-event-review'),
    path('delete/<int:review_id>/', views.delete_review, name='delete-review'),
]
