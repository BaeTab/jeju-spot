from django.urls import path
from . import views

urlpatterns = [
    path('', views.SpotListView.as_view(), name='spot-list'),
    path('<int:pk>/', views.SpotDetailView.as_view(), name='spot-detail'),
    path('create/', views.SpotCreateView.as_view(), name='spot-create'),
    path('<int:pk>/update/', views.SpotUpdateView.as_view(), name='spot-update'),
    path('<int:pk>/delete/', views.SpotDeleteView.as_view(), name='spot-delete'),
]
