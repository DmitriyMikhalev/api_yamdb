import csv

from django.core.management.base import BaseCommand

from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open('static/data/users.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Advance past the header
            User.objects.all().delete()
            for row in reader:
                print(row)
                users = User.objects.create(id=row[0],
                                            username=row[1],
                                            email=row[2],
                                            role=row[3],
                                            bio=row[4],
                                            first_name=row[5],
                                            last_name=row[6],
                                            )
                users.save()

        with open('static/data/category.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Advance past the header
            Category.objects.all().delete()
            for row in reader:
                print(row)
                category = Category.objects.create(id=row[0],
                                                   name=row[1],
                                                   slug=row[2],
                                                   )
                category.save()

        with open('static/data/genre.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Advance past the header
            Genre.objects.all().delete()
            for row in reader:
                print(row)
                genre = Genre.objects.create(id=row[0],
                                             name=row[1],
                                             slug=row[2],
                                             )
                genre.save()

        with open('static/data/titles.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Advance past the header
            Title.objects.all().delete()
            for row in reader:
                print(row)
                category = Category.objects.get(id=row[3])
                titles = Title.objects.create(id=row[0],
                                              name=row[1],
                                              year=row[2],
                                              category=category,
                                              )
                titles.save()

        with open('static/data/genre_title.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Advance past the header
            GenreTitle.objects.all().delete()
            for row in reader:
                print(row)
                genre_title = GenreTitle.objects.create(id=row[0],
                                                        title_id=row[1],
                                                        genre_id=row[2],
                                                        )
                genre_title.save()

        with open('static/data/review.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Advance past the header
            Review.objects.all().delete()
            for row in reader:
                print(row)
                author = User.objects.get(id=row[3])
                review = Review.objects.create(id=row[0],
                                               title_id=row[1],
                                               text=row[2],
                                               author=author,
                                               score=row[4],
                                               pub_date=row[5]
                                               )
                review.save()

        with open('static/data/comments.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Advance past the header
            Comment.objects.all().delete()
            for row in reader:
                print(row)
                author = User.objects.get(id=row[3])
                comment = Comment.objects.create(id=row[0],
                                                 review_id=row[1],
                                                 text=row[2],
                                                 author=author,
                                                 pub_date=row[4],
                                                 )
                comment.save()
        self.stdout.write(self.style.SUCCESS('###'))
        self.stdout.write(self.style.SUCCESS('!!!ВСЕ ДАННЫЕ ЗАГРУЖЕНЫ!!!'))
