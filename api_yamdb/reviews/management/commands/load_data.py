import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)

MODELS_DICT = {'users.csv': User,
               'category.csv': Category,
               'genre.csv': Genre,
               'titles.csv': Title,
               'genre_title.csv': GenreTitle,
               'review.csv': Review,
               'comments.csv': Comment,
               }

files = os.listdir('static/data/')


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for file, model in MODELS_DICT.items():
            model.objects.all().delete()
            with open(
                f'{settings.BASE_DIR}/static/data/{file}',
                'r',
                encoding='utf-8'
            ) as opened_file:
                reader = csv.DictReader(opened_file)
                model.objects.bulk_create(
                    model(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('Все данные загружены'))
