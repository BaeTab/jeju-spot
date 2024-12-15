from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Spot, SpotCategory, SpotImage

class SpotModelTestCase(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser', 
            password='testpassword123'
        )
        
        self.category = SpotCategory.objects.create(
            name='맛집',
            description='제주도의 맛있는 음식점'
        )
        
        self.spot = Spot.objects.create(
            title='제주 맛집',
            description='맛있는 제주 음식점',
            address='제주시 어딘가',
            category='restaurant',
            created_by=self.user
        )

    def test_spot_creation(self):
        self.assertEqual(self.spot.title, '제주 맛집')
        self.assertEqual(self.spot.description, '맛있는 제주 음식점')
        self.assertEqual(self.spot.address, '제주시 어딘가')
        self.assertEqual(self.spot.category, 'restaurant')
        self.assertEqual(self.spot.created_by, self.user)

    def test_spot_str_representation(self):
        self.assertEqual(str(self.spot), '제주 맛집')

    def test_spot_likes(self):
        self.spot.likes.add(self.user)
        self.assertEqual(self.spot.likes.count(), 1)
        self.assertEqual(self.spot.total_likes(), 1)

    def test_spot_views_count(self):
        initial_views = self.spot.views_count
        self.spot.increment_views()
        self.assertEqual(self.spot.views_count, initial_views + 1)

class SpotImageModelTestCase(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser', 
            password='testpassword123'
        )
        
        self.spot = Spot.objects.create(
            title='테스트 스팟',
            description='테스트 설명',
            address='제주시 테스트',
            category='cafe',
            created_by=self.user
        )
        
        self.spot_image = SpotImage.objects.create(
            spot=self.spot,
            image=None  # 실제 이미지 파일 테스트는 별도로 필요
        )

    def test_spot_image_creation(self):
        self.assertEqual(self.spot_image.spot, self.spot)
        self.assertEqual(str(self.spot_image), f'Image for {self.spot.title}')
