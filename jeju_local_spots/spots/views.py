from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
import logging

from .models import Spot, SpotImage, SpotCategory
from .forms import SpotForm
from .serializers import SpotSerializer, SpotImageSerializer, SpotCategorySerializer

from reviews.models import Review
from reviews.forms import ReviewForm
from reviews.serializers import ReviewSerializer

logger = logging.getLogger(__name__)

class SpotViewSet(viewsets.ModelViewSet):
    queryset = Spot.objects.all()
    serializer_class = SpotSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        spot = self.get_object()
        if spot.likes.filter(id=request.user.id).exists():
            spot.likes.remove(request.user)
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        else:
            spot.likes.add(request.user)
            return Response({'status': 'liked'}, status=status.HTTP_200_OK)

class SpotImageViewSet(viewsets.ModelViewSet):
    queryset = SpotImage.objects.all()
    serializer_class = SpotImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(spot_id=self.request.data.get('spot_id'))

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SpotCategoryViewSet(viewsets.ModelViewSet):
    queryset = SpotCategory.objects.all()
    serializer_class = SpotCategorySerializer
    permission_classes = [permissions.IsAdminUser]

class SpotListView(ListView):
    model = Spot
    template_name = 'spots/spot_list.html'
    context_object_name = 'spots'
    paginate_by = 9

    def get_queryset(self):
        queryset = Spot.objects.all()
        category_name = self.request.GET.get('category')
        
        if category_name:
            try:
                category = SpotCategory.objects.get(name=category_name)
                queryset = queryset.filter(category=category)
            except SpotCategory.DoesNotExist:
                # 카테고리가 존재하지 않으면 빈 쿼리셋 반환
                queryset = Spot.objects.none()
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = SpotCategory.objects.all()
        context['selected_category'] = self.request.GET.get('category')
        return context

class SpotDetailView(DetailView):
    model = Spot
    template_name = 'spots/spot_detail.html'
    context_object_name = 'spot'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        context['reviews'] = Review.objects.filter(spot=self.object)
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.increment_views()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

from .models import Spot, SpotImage, SpotCategory

logger = logging.getLogger(__name__)

class SpotCreateView(LoginRequiredMixin, CreateView):
    model = Spot
    template_name = 'spots/spot_form.html'
    success_url = reverse_lazy('spot-list')
    form_class = SpotForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = SpotCategory.objects.all()
        # CreateView에서는 object 대신 form을 사용
        context['form'] = context.get('form') or self.get_form()
        return context

    def form_valid(self, form):
        # 장소 객체 생성
        logger.info("=== Form Submission Debug Info ===")
        logger.info(f"Form data: {form.cleaned_data}")
        logger.info(f"Request POST data: {self.request.POST}")
        logger.info(f"Request FILES data: {dict(self.request.FILES)}")
        logger.info(f"Form is valid: {form.is_valid()}")
        logger.info(f"Form errors: {form.errors}")  # 항상 에러 로깅
        logger.info(f"Form files field: {form.files}")  # 폼의 파일 필드 로깅
        if not form.is_valid():
            logger.error(f"Form errors: {form.errors}")
            
        form.instance.created_by = self.request.user
        
        # 장소 저장
        try:
            spot = form.save()
            logger.info(f"Saved spot: {spot}")
            
            # 이미지 처리
            images = self.request.FILES.getlist('images')
            logger.info(f"Images to save: {images}")
            logger.info(f"Number of images: {len(images)}")
            
            if not images:
                error_msg = "최소 1개의 이미지를 업로드해야 합니다."
                form.add_error('images', error_msg)
                spot.delete()  # spot 삭제
                return self.form_invalid(form)
            
            image_errors = []
            saved_images = []
            
            for image_file in images:
                try:
                    # 이미지 크기 제한 (5MB)
                    if image_file.size > 5 * 1024 * 1024:
                        error_msg = f"이미지 {image_file.name}의 크기가 5MB를 초과합니다"
                        logger.error(error_msg)
                        image_errors.append(error_msg)
                        continue
                    
                    # 이미지 타입 검증
                    if not image_file.content_type.startswith('image/'):
                        error_msg = f"파일 {image_file.name}은(는) 이미지 파일이 아닙니다"
                        logger.error(error_msg)
                        image_errors.append(error_msg)
                        continue
                    
                    spot_image = SpotImage.objects.create(spot=spot, image=image_file)
                    saved_images.append(spot_image)
                    logger.info(f"Saved image: {image_file}")
                except Exception as e:
                    error_msg = f"이미지 {image_file.name} 저장 중 오류 발생: {e}"
                    logger.error(error_msg)
                    image_errors.append(error_msg)
            
            # 이미지 저장 중 오류 발생 시 처리
            if image_errors and not saved_images:  # 모든 이미지 저장 실패
                spot.delete()  # spot 삭제
                for error in image_errors:
                    form.add_error('images', error)
                return self.form_invalid(form)
            
            if image_errors:  # 일부 이미지만 저장 실패
                for error in image_errors:
                    form.add_error('images', error)
            
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Error saving spot: {e}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        # 폼 유효성 검사 실패 시 로깅 및 컨텍스트에 카테고리 추가
        logger.error(f"Form validation failed: {form.errors}")
        logger.error(f"Form data: {form.data}")
        logger.error(f"Form files: {form.files}")
        
        # 추가 오류 메시지 로깅
        if not form.errors:
            logger.error("Unknown form validation error")
        
        return self.render_to_response(self.get_context_data(form=form))

class SpotUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Spot
    form_class = SpotForm
    template_name = 'spots/spot_form.html'
    success_url = reverse_lazy('spot-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        
        if 'images' in form.cleaned_data and form.cleaned_data['images']:
            self.object.images.all().delete()
            
            for image in self.request.FILES.getlist('images'):
                SpotImage.objects.create(spot=self.object, image=image)
        
        return response

    def test_func(self):
        spot = self.get_object()
        return self.request.user == spot.created_by

class SpotDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Spot
    template_name = 'spots/spot_confirm_delete.html'
    success_url = reverse_lazy('spot-list')

    def test_func(self):
        spot = self.get_object()
        return self.request.user == spot.created_by
