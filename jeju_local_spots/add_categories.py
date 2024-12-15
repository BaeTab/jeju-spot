import os
import django

# Django 설정 파일 경로 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from spots.models import SpotCategory

# 카테고리 생성
categories = [
    {'name': '맛집', 'description': '제주도의 맛있는 음식점들'},
    {'name': '카페', 'description': '아름다운 제주도 카페'},
    {'name': '액티비티', 'description': '제주도에서 즐기는 다양한 활동'},
    {'name': '숨은 명소', 'description': '알려지지 않은 제주도의 숨겨진 명소들'}
]

for category_data in categories:
    category, created = SpotCategory.objects.get_or_create(**category_data)
    if created:
        print(f"Created category: {category.name}")
    else:
        print(f"Category already exists: {category.name}")
