import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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
