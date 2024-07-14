from rest_framework.serializers import ModelSerializer, SerializerMethodField

from course.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    count_lesson_in_course = SerializerMethodField()
    lesson = LessonSerializer(many=True, read_only=True)

    def get_count_lesson_in_course(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ("name", "description", "image", "count_lesson_in_course", "lesson")


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"
