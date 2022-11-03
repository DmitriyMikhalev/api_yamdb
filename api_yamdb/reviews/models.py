import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

ADMIN = 'admin'
USER = 'user'
MODERATOR = 'moderator'

ROLE_CHOICES = (
    (ADMIN, 'Администратор'),
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор')
)


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        unique=True,
        max_length=50
    )


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        unique=True,
        max_length=50
    )


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(datetime.datetime.now().year)])
    description = models.TextField(blank=True, default='')
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)


class User(AbstractUser):
    bio = models.TextField(
        blank=True,
        default='',
        verbose_name='Биография'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта'
    )
    role = models.CharField(
        choices=ROLE_CHOICES,
        default=USER,
        max_length=13,
        verbose_name='Статус прав'
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER
