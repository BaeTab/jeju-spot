from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from rest_framework import viewsets, permissions

from .forms import ReviewForm
from .models import Review
from .serializers import ReviewSerializer
from spots.models import Spot
from events.models import Event

@login_required
def create_spot_review(request, spot_id):
    spot = get_object_or_404(Spot, id=spot_id)
    
    # 이미 해당 스팟에 대한 리뷰를 작성했는지 확인
    existing_review = Review.objects.filter(user=request.user, spot=spot).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.spot = spot
            
            if existing_review:
                # 기존 리뷰 업데이트
                existing_review.rating = review.rating
                existing_review.content = review.content
                existing_review.save()
                messages.success(request, '리뷰가 성공적으로 수정되었습니다.')
            else:
                # 새 리뷰 생성
                review.save()
                messages.success(request, '리뷰가 성공적으로 작성되었습니다.')
            
            return redirect('spot-detail', pk=spot_id)
    else:
        # 기존 리뷰가 있다면 해당 리뷰로 폼 초기화
        form = ReviewForm(instance=existing_review) if existing_review else ReviewForm()
    
    return render(request, 'reviews/review_form.html', {
        'form': form, 
        'object': spot, 
        'type': 'spot',
        'existing_review': existing_review
    })

@login_required
def create_event_review(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # 이미 해당 이벤트에 대한 리뷰를 작성했는지 확인
    existing_review = Review.objects.filter(user=request.user, event=event).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.event = event
            
            if existing_review:
                # 기존 리뷰 업데이트
                existing_review.rating = review.rating
                existing_review.content = review.content
                existing_review.save()
                messages.success(request, '리뷰가 성공적으로 수정되었습니다.')
            else:
                # 새 리뷰 생성
                review.save()
                messages.success(request, '리뷰가 성공적으로 작성되었습니다.')
            
            return redirect('event-detail', pk=event_id)
    else:
        # 기존 리뷰가 있다면 해당 리뷰로 폼 초기화
        form = ReviewForm(instance=existing_review) if existing_review else ReviewForm()
    
    return render(request, 'reviews/review_form.html', {
        'form': form, 
        'object': event, 
        'type': 'event',
        'existing_review': existing_review
    })

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if review.spot:
        redirect_url = 'spot-detail'
        redirect_id = review.spot.id
    else:
        redirect_url = 'event-detail'
        redirect_id = review.event.id
    
    review.delete()
    messages.success(request, '리뷰가 삭제되었습니다.')
    
    return redirect(redirect_url, pk=redirect_id)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'
    success_url = reverse_lazy('spots:spot_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        spot_id = self.kwargs.get('spot_id')
        form.instance.spot = get_object_or_404(Spot, id=spot_id)
        return super().form_valid(form)

class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'
    success_url = reverse_lazy('spots:spot_list')

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/review_confirm_delete.html'
    success_url = reverse_lazy('spots:spot_list')

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
