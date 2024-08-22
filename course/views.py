from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework
from rest_framework import viewsets, generics, filters

from rest_framework.permissions import IsAuthenticated
from course import models, serializers
from users.permissions import IsModerator, UserListOnly, IsOwner

from course.models import Course, Lesson, Subscription
from course.paginators import CoursePagination, LessonPagination

from course.serializers import (
    CourseSerializer,
    LessonSerializer,
    CourseDetailSerializer,
)

from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="description from swagger_auto_schema via method_decorator"
))


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = CoursePagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsModerator|UserListOnly]
        elif self.action == 'create':
            self.permission_classes = [~IsModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwner]
        else:
            self.permission_classes = [IsOwner|IsModerator]
        return [permission() for permission in [IsAuthenticated] + self.permission_classes]


class LessonCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, ~IsModerator]

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsModerator|UserListOnly]

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator|IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator|IsOwner]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class PaymentListAPIView(generics.ListAPIView):
    queryset = models.Payment.objects.all()
    serializer_class = serializers.PaymentSerializer

    filter_backends = [filters.OrderingFilter, rest_framework.DjangoFilterBackend]
    filterset_fields = ['method', 'lesson', 'course']
    ordering_fields = ['payment_date']
    permission_classes = [IsAuthenticated]


class SubscriptionAPIView(APIView):
    def post(self, *args, **kwargs):
        user = self.request.user
        course = get_object_or_404(Course.objects.filter(pk=self.request.data.get('course')))
        subscription_data = {
            'user': user,
            'course': course
        }
        is_subscribed = Subscription.objects.filter(**subscription_data).exists()
        if is_subscribed:
            Subscription.objects.filter(**subscription_data).delete()
            message = 'unsubscribed'
        else:
            Subscription.objects.create(**subscription_data)
            message = 'subscribed'
        return Response({'message': message})
