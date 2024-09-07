from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from course.models import Course
from django.utils import timezone

from users.models import User


@shared_task
def send_notification(course_id):
    course = Course.objects.get(pk=course_id)
    users_email = [
        subscription.user.email for subscription in course.subscription.all()
    ]
    subject = "обновление курса"
    message = f"Курс {course.name} обновлен"
    send_mail(subject, message, None, users_email, fail_silently=False)


@shared_task
def check_user_activity():
    today = timezone.now().today()

    users = User.objects.all()

    def is_inactive(user):
        if not user.is_active or (today - user.last_login > timedelta(days=30)):
            user.is_active = False
            user.save()
            print("User {} blocked".format(user))
            return True
        else:
            return False

    results = list(map(is_inactive, users))