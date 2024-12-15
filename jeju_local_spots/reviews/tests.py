from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Review
from spots.models import Spot

class ReviewModelTestCase(TestCase):
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
        
        self.review = Review.objects.create(
            spot=self.spot,
            user=self.user,
            content='좋은 장소입니다.',
            rating=4
        )

    def test_review_creation(self):
        self.assertEqual(self.review.spot, self.spot)
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.content, '좋은 장소입니다.')
        self.assertEqual(self.review.rating, 4)

    def test_review_str_representation(self):
        expected_str = f"Review for {self.spot.title} by {self.user.username}"
        self.assertEqual(str(self.review), expected_str)
