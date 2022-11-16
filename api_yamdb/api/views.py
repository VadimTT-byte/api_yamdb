from rest_framework import mixins, viewsets
from django.db.models import Avg
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from reviews.models import Category, Genre, Title, Review, Comment
from users.permissions import IsAdministrator, ReadOnly, IsAuthorOrReadOnly, IsModerator

from .filters import FilterForTitle
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleCreateSerializer, TitleSerializer, CommentSerializer, ReviewSerializer)


class CreateListModelViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass

from rest_framework.generics import get_object_or_404


class CategoryViewSet(CreateListModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdministrator | ReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdministrator | ReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewset(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")  # добавил агрегацию
    ).order_by("name")
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdministrator | ReadOnly]
    filterset_class = FilterForTitle

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleCreateSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    permission_classes = [IsAdministrator | IsAuthorOrReadOnly | IsModerator]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    permission_classes = [IsAdministrator | IsAuthorOrReadOnly | IsModerator]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
