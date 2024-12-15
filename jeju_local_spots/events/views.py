from django.shortcuts import render
from rest_framework import viewsets, permissions
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Event
from .serializers import EventSerializer
from .forms import EventForm
from reviews.models import Review
from reviews.forms import ReviewForm

# Create your views here.

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        queryset = Event.objects.all()
        event_type = self.request.query_params.get('type', None)
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        return queryset

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 9

    def get_queryset(self):
        queryset = Event.objects.all()
        event_type = self.request.GET.get('type')
        
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        
        return queryset.order_by('-start_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_types'] = dict(Event.TYPES)
        context['selected_type'] = self.request.GET.get('type')
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 관련 이벤트
        context['related_events'] = Event.objects.filter(
            event_type=self.object.event_type
        ).exclude(pk=self.object.pk)[:3]
        
        # 리뷰 관련 컨텍스트
        context['reviews'] = Review.objects.filter(event=self.object)
        context['review_form'] = ReviewForm()
        
        # 평균 평점 계산
        reviews = context['reviews']
        if reviews:
            context['average_rating'] = sum(review.rating for review in reviews) / len(reviews)
        else:
            context['average_rating'] = None
        
        return context

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('event-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '새 이벤트 등록'
        return context

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('event-list')

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.created_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '이벤트 수정'
        return context

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('event-list')

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.created_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '이벤트 삭제'
        return context
