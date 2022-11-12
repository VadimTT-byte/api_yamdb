from rest_framework import (
    mixins,
    viewsets
)
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from reviews.models import (
    Category,
    Genre,
    Title
)

from .filters import FilterForTitle
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleCreateSerializer,
    TitleSerializer
)

# from users.permissions import (
#     IsAdministrator,
#     IsAuthorOrReadOnly,
#     IsModerator,
#     ReadOnly
# )


class CreateListModelViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CategoryViewSet(CreateListModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    # permission_classes = [IsAdministrator | ReadOnly]
    filter_backends = (SearchFilter,)
    search_field = ('name', )
    lookup_field = 'slug'


class GenreViewSet(CreateListModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
#    permission_classes = [IsAdministrator | ReadOnly]
    filter_backends = (SearchFilter,)
    search_field = ('name', )
    lookup_field = 'slug'


class TitleViewset(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
#    permission_classes = [IsAdministrator | ReadOnly]
    filterset_class = FilterForTitle

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleCreateSerializer
        return TitleSerializer
