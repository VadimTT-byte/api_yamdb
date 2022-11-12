from django.db import models


class Category(models.Model):
    """Categories of artworks"""

    name = models.CharField(
        max_length=256,
        verbose_name='Category name'
    )

    slug = models.SlugField(
        max_length=50,
        verbose_name='Shortname of group',
        unique=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Genre(models.Model):
    """Genres of artworks"""

    name = models.CharField(
        max_length=256,
        verbose_name='Genre name',
    )

    slug = models.SlugField(
        max_length=50,
        verbose_name='Shortname of genre',
        unique=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Title(models.Model):
    """Name of artwork"""

    name = models.CharField(
        max_length=256,
        verbose_name='name artwork',
    )

    year = models.PositiveSmallIntegerField(
        verbose_name='year of creation',
    )

    description = models.TextField(
        verbose_name='artwork description',
        blank=True,
    )

    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Category',
    )

    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Genre',
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Artwork'
        verbose_name_plural = 'Artworks'


class GenreTitle(models.Model):
    title = models.ForeignKey(
        'Title',
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.CASCADE
    )


    def __str__(self):
        return f'{self.genre}'
