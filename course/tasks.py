from celery import shared_task
from django.core.mail import send_mail
from course.models import Course


@shared_task
def send_notification(course_id):
    course = Course.objects.get(pk=course_id)
    users_email = [
        subscription.user.email for subscription in course.subscription.all()
    ]
    subject = "обновление курса"
    message = f"Курс {course.name} обновлен"
    send_mail(subject, message, None, users_email, fail_silently=False)
