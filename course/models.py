from django.db import models
from django.contrib.auth import get_user_model

METHOD_CHOICE = [
    ('CASH', 'оплата наличными'),
    ('TRAN', 'перевод на счет')
]

User = get_user_model()


class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True, default=None)

    name = models.CharField(
        max_length=120, verbose_name="Название куса", help_text="Укажите название курса"
    )
    image = models.ImageField(
        upload_to="course/course/image",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Добавьте изображение",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание курса",
        help_text="Укажите описание курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True, default=None)

    name = models.CharField(
        max_length=150, verbose_name="Урок", help_text="Укажите название урока"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Курс",
        help_text="Выберите курс",
        related_name="lesson",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание урока",
        help_text="Укажите описание урока",
    )
    image = models.ImageField(
        upload_to="course/lesson/image",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Добавьте изображение",
    )
    link_to_video = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Ссылка на видео",
        help_text="Укажите ссылку на видео",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    date_of_pay = models.DateField(auto_now=True, verbose_name='дата оплаты')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True,)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True,)
    amount = models.PositiveIntegerField()
    method = models.CharField(max_length=4, choices=METHOD_CHOICE)
    filterset_fields = ['category', 'in_stock']

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"


class Subscription(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscription')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscription')

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(fields=['course', 'user'], name='unique_subscription')
        ]
