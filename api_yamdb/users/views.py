from __future__ import annotations

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import Http404
from django.utils.crypto import get_random_string
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from . import permissions
from .models import User
from .serializers import (AuthSignUpSerializer, AuthTokenSerializer,
                          MeUserSerrializer, UserSerializer)


class Auth:
    @staticmethod
    def create_conf_code() -> str:
        return get_random_string(settings.RND_STR_LENTH)

    @staticmethod
    def hash_confirmation_code(conf_code: str) -> str:
        return make_password(password=conf_code)

    @staticmethod
    def check_conf_code(conf_code: str, hashed_conf_code: str) -> bool:
        return check_password(
            password=conf_code,
            encoded=hashed_conf_code,
        )


class SignUpView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = AuthSignUpSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except IntegrityError:
            pass

        username = serializer.data['username']
        email = serializer.data['email']
        user = User.objects.filter(
            username=username,
            email=email
        ).first()
        if not user or user.confirmation_code:
            raise ValidationError(
                f'Username \'{username}\''
                f' or email \'{email}\' is already taken'
            )

        conf_code = Auth.create_conf_code()
        user.confirmation_code = Auth.hash_confirmation_code(
            conf_code
        )
        user.save()

        message = f'confirmation_code: {conf_code}'

        send_mail(
            subject='Registration confirmation',
            message=message,
            from_email=settings.EMAIL_CONF_CODE,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class JWTTokenView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = get_object_or_404(
                User,
                username=serializer.data['username']
            )
        except Http404:
            return Response(
                data={'detail': 'User is not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if not Auth.check_conf_code(
            conf_code=serializer.data['confirmation_code'],
            hashed_conf_code=user.confirmation_code
        ):
            return Response(
                data={'confirmation_code': ['Not a valid']},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            data=self._get_jwt_token_for_user(user),
            status=status.HTTP_200_OK
        )

    def _get_jwt_token_for_user(self, user) -> dict[str, str]:
        return {
            'token': str(AccessToken.for_user(user))
        }


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAdministrator]

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
        serializer_class=MeUserSerrializer,
        url_path='me'
    )
    def current_user(self, request):
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                instance=self.request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

        else:
            serializer = self.get_serializer(self.request.user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
