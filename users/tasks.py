from datetime import timedelta
from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


@shared_task
def periodic_block():
    User.objects.exclude(is_superuser=True).exclude(is_staff=True).filter(
        last_login__lt=timezone.now() - timedelta(days=30)
    ).update(is_active=False)
