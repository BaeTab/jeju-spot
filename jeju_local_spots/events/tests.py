from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Event

class EventModelTestCase(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser', 
            password='testpassword123'
        )
        
        self.event = Event.objects.create(
            title='제주 축제',
            description='제주에서 열리는 멋진 축제',
            location='제주시 중앙로',
            start_date=timezone.now(),
            end_date=timezone.now(),
            created_by=self.user
        )

    def test_event_creation(self):
        self.assertEqual(self.event.title, '제주 축제')
        self.assertEqual(self.event.description, '제주에서 열리는 멋진 축제')
        self.assertEqual(self.event.location, '제주시 중앙로')
        self.assertEqual(self.event.created_by, self.user)

    def test_event_str_representation(self):
        self.assertEqual(str(self.event), '제주 축제')

    def test_event_views_count(self):
        initial_views = self.event.views_count
        self.event.increment_views()
        self.assertEqual(self.event.views_count, initial_views + 1)
