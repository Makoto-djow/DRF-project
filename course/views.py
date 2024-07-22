from django.shortcuts import render
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

from course.models import Course, Lesson
from course.serializers import (
    CourseSerializer,
    LessonSerializer,
    CourseDetailSerializer,
)


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()

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
