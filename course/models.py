from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=120, verbose_name="Название куса", help_text="Укажите название курса"
    )
    image = models.ImageField(
        upload_to="course/course/image",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Добавьте изображение"
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание курса", help_text="Укажите описание курса"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(
        max_length=150, verbose_name="Урок", help_text="Укажите название урока"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", help_text="Выберите курс"
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание урока", help_text="Укажите описание урока"
    )
    image = models.ImageField(
        upload_to="course/lesson/image",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Добавьте изображение"
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
