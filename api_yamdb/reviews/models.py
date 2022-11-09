import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=settings.LIMIT_CHAT,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=settings.LIMIT_SLUG,
        verbose_name='Идентификатор',
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Comment(models.Model):
    author = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='comments',
        to=User,
        verbose_name='Пользователь'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации'
    )
    review = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='comments',
        to='Review',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        verbose_name='Текст',
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Genre(models.Model):
    name = models.CharField(
        max_length=settings.LIMIT_CHAT,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=settings.LIMIT_SLUG,
        verbose_name='Идентификатор',
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class GenreTitle(models.Model):
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    title = models.ForeignKey('Title', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    author = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='reviews',
        to=User,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(settings.MIN_LIMIT_VALUE),
            MaxValueValidator(settings.MAX_LIMIT_VALUE)
        ],
    )
    text = models.TextField()
    title = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='reviews',
        to='Title',
        verbose_name='Произведение'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]
        ordering = ('pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:settings.LIMIT_REVIEW_STR]


class Title(models.Model):
    category = models.ForeignKey(
        null=True,
        on_delete=models.SET_NULL,
        to=Category
    )
    description = models.TextField(blank=True, default='')
    genre = models.ManyToManyField(
        related_name='genre',
        through='GenreTitle',
        to='Genre',
        verbose_name='Жанр'
    )
    name = models.CharField(max_length=settings.LIMIT_CHAT)
    year = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(datetime.datetime.now().year)
        ]
    )

    def __str__(self):
        return self.name

    class Meta:
        default_related_name = "titles"
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
