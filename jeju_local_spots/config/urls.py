"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from spots.views import SpotViewSet, SpotImageViewSet, SpotCategoryViewSet
from events.views import EventViewSet
from reviews.views import ReviewViewSet
from .views import HomeView

router = DefaultRouter()
router.register(r'spots', SpotViewSet)
router.register(r'spot-images', SpotImageViewSet)
router.register(r'spot-categories', SpotCategoryViewSet)
router.register(r'events', EventViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('accounts/', include('accounts.urls')),
    path('spots/', include('spots.urls')),
    path('events/', include('events.urls')),
    path('reviews/', include('reviews.urls')),
    path('search/', include('search.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
