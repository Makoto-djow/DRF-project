from django.test import TestCase

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model

from course.models import Lesson, Course

User = get_user_model()


class LessonTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user = User(email='test@mail.com')
        cls.user.set_password('2222')
        cls.user.save()
        cls.lesson = Lesson.objects.create(name='урок', user=cls.user)

    def test_create(self):
        data = {
            'name': 'test2'
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse('course:lessons-create'), data=data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertTrue(
            Lesson.objects.filter(pk=2).exists()
        )

    def test_retrieve(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse('course:lessons-retrieve', kwargs={'pk': 1}))
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "name": "урок",
                "description": None,
                "image": None,
                "link_to_video": None,
                "course": None
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse('course:lessons-list'))
        data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "name": "урок",
                    "description": None,
                    "course": None,
                    "image": None,
                    "link_to_video": None
                }
            ]
        }
        self.assertEqual(
            response.data,
            data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update(self):
        data = {
            'name': 'тест'
        }
        self.client.force_authenticate(self.user)
        response = self.client.put(reverse('course:lessons-update', kwargs={'pk': 1}), data=data, format='json')
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "name": "тест",
                "description": None,
                "image": None,
                "link_to_video": None,
                "course": None
            }
        )
        self.assertEqual(
            Lesson.objects.get(pk=1).name, 'тест'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_delete(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(reverse('course:lessons-delete', kwargs={'pk': 1}))
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class SubscriptionTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user = User(email='test@mail.com')
        cls.user.set_password('2222')
        cls.user.save()
        cls.course = Course.objects.create(name='курс', user=cls.user)

    def test_subscription(self):
        self.client.force_authenticate(self.user)
        data = {
            'course': 1
        }
        response = self.client.post(reverse('course:subscription'), data=data, format='json')
        self.assertEqual(
            response.data, {'course': 'subscribed'}
        )
        response = self.client.post(reverse('course:subscription'), data=data, format='json')
        self.assertEqual(
            response.data, {'message': 'unsubscribed'}
        )
