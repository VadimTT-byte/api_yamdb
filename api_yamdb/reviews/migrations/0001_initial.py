# Generated by Django 2.2.16 on 2022-11-05 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Category name')),
                ('slug', models.SlugField(unique=True, verbose_name='Shortname of group')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Genre name')),
                ('slug', models.SlugField(unique=True, verbose_name='Shortname of genre')),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='name artwork')),
                ('year', models.PositiveSmallIntegerField(verbose_name='year of creation')),
                ('description', models.TextField(blank=True, verbose_name='artwork description')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.Category', verbose_name='Category')),
                ('genre', models.ManyToManyField(related_name='titles', to='reviews.Genre', verbose_name='Genre')),
            ],
            options={
                'verbose_name': 'Artwork',
                'verbose_name_plural': 'Artworks',
            },
        ),
    ]
