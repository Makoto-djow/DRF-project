from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from course import models

from course.models import Course, Lesson
from course.validators import YouTubeLinkOnlyValidator


class LessonSerializer(ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [YouTubeLinkOnlyValidator(fields=['name', 'description', 'link_to_video'])]


class CourseDetailSerializer(ModelSerializer):
    count_lesson_in_course = SerializerMethodField()
    lesson = LessonSerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    def get_subscription(self, obj):
        return obj.subscription.filter(user=self.context.get('request').user).exists()

    class Meta:
        model = Course
        fields = ("name", "description", "image", "count_lesson_in_course", "lesson")
        validators = [YouTubeLinkOnlyValidator(fields=['name', 'description'])]


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = '__all__'
