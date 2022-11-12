import csv

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from reviews.models import Category, Genre, Title
from users.models import User


class Command(BaseCommand):

    def load_table_users(self):
        with open('static/data/users.csv', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for row_num, row in enumerate(reader):
                if row_num == 0:
                    continue
                else:
                    User.objects.get_or_create(
                        id=row[0],
                        username=row[1],
                        email=row[2],
                        role=row[3],
                        bio=row[4],
                        first_name=row[5],
                        last_name=row[6]
                    )

    def load_table_title(self):
        with open('static/data/titles.csv', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for row_num, row in enumerate(reader):
                if row_num == 0:
                    continue
                else:
                    if Title.objects.filter(id=row[0]).exists():
                        continue
                    Title.objects.get_or_create(
                        id=row[0],
                        name=row[1],
                        year=row[2],
                        category=get_object_or_404(Category, id=row[3])
                    )

    def load_table_genre(self):
        with open('static/data/genre.csv', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row_num, row in enumerate(reader):
                    if row_num == 0:
                        continue
                    else:
                        Genre.objects.get_or_create(
                            id=row[0],
                            name=row[1],
                            slug=row[2]
                        )

    def load_table_category(self):
        with open('static/data/category.csv', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for row_num, row in enumerate(reader):
                if row_num == 0:
                    continue
                else:
                    Category.objects.get_or_create(
                        id=row[0],
                        name=row[1],
                        slug=row[2]
                    )

    def load_table_genre_title(self):
        with open(
            'static/data/genre_title.csv', encoding='utf-8'
        ) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row_num, row in enumerate(reader):
                if row_num == 0:
                    continue
                else:
                    title_obj = get_object_or_404(Title, id=row[1])
                    genre_obj = get_object_or_404(Genre, id=row[2])
                    title_obj.genre.add(genre_obj)
                    title_obj.save()

    def handle(self, *args, **options):
        self.load_table_users()
        self.load_table_category()
        self.load_table_genre()
        self.load_table_genre_title()
