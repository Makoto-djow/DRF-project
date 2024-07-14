from django.contrib.auth.models import AbstractUser
from django.db import models
from course.models import Lesson, Course

METHOD_CHOISES = [("CASH", "оплата наличными"), ("TRAN", "перевод на счет")]


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )
    city = models.CharField(
        max_length=50, null=True, verbose_name="Город", help_text="Укажите свой город"
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите свой аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    date_of_pay = models.DateField(auto_now=True, verbose_name="дата оплаты")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.PositiveIntegerField()
    method = models.CharField(max_length=4, choices=METHOD_CHOISES)
    filterset_fields = ["category", "in_stock"]
