from django.urls import path
from . import views

urlpatterns = [
    path('', views.unified_search, name='unified-search'),
]
