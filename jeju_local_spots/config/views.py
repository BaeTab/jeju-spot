from django.views.generic import TemplateView
from django.db.models import Q
from spots.models import Spot, SpotCategory
from events.models import Event
from datetime import timedelta
from django.utils import timezone
from reviews.models import Review

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 카테고리
        context['categories'] = SpotCategory.objects.all()
        
        # 최근 장소
        context['recent_spots'] = Spot.objects.order_by('-created_at')[:6]
        
        # 최근 이벤트
        context['recent_events'] = Event.objects.order_by('-created_at')[:6]
        
        # 실시간 인기 장소 (최근 7일 내 조회수 기준)
        week_ago = timezone.now() - timedelta(days=7)
        context['trending_spots'] = Spot.objects.filter(
            created_at__gte=week_ago
        ).order_by('-views_count')[:6]
        
        # 실시간 인기 이벤트 (최근 7일 내 조회수 기준)
        context['trending_events'] = Event.objects.filter(
            created_at__gte=week_ago
        ).order_by('-views_count')[:6]
        
        # 가장 많은 리뷰가 있는 장소와 이벤트
        context['most_reviewed_spots'] = sorted(
            Spot.objects.all(), 
            key=lambda spot: Review.objects.filter(spot=spot).count(), 
            reverse=True
        )[:6]
        
        context['most_reviewed_events'] = sorted(
            Event.objects.all(), 
            key=lambda event: Review.objects.filter(event=event).count(), 
            reverse=True
        )[:6]
        
        return context
