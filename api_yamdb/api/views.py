from api.filters import TitleFilter
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorOrModeRatOrOrAdminOrReadOnly)
from .serializers import (AdminUserSerializer, CategorySerializer,
                          CommentSerializer, GenreSerializer,
                          ReadOnlyTitleSerializer, ReviewSerializer,
                          SignUpSerializer, TitleSerializer, TokenSerializer,
                          UserSerializer)
from .utils import send_verify_code

User = get_user_model()


class CreateDeliteViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          mixins.DestroyModelMixin,
                          GenericViewSet):
    pass


class CategoryViewSet(CreateDeliteViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Category.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModeRatOrOrAdminOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class GenreViewSet(CreateDeliteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")
    ).order_by("name")
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModeRatOrOrAdminOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Function for signup procedure. If given data is correct, user will get
    email with verification code to recieve JWT at ../token/ endpoint. Return
    given data and HTTP200 or errors that have occured and HTTP400.
    """
    serializer = SignUpSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

    user = serializer.save()
    send_verify_code(user)

    return Response(data=serializer.data, status=HTTP_200_OK)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")
    ).order_by("name")
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadOnlyTitleSerializer
        return TitleSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    """Function for receiving JWT via verification code from email. If given
    data is correct, returns JSON {'token': ...} and HTTP200 else returns
    errors that have occured and HTTP400.
    """
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

    username = serializer.data.get('username')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(klass=User, username=username)

    if not default_token_generator.check_token(user, token=confirmation_code):
        return Response(
            data={'confirmation_code': f'{confirmation_code}'},
            status=HTTP_400_BAD_REQUEST
        )

    jwt_token_pair = RefreshToken.for_user(user=user)

    return Response(
        data={'token': f'{str(jwt_token_pair.access_token)}'},
        status=HTTP_200_OK
    )


class UserViewSet(ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    search_fields = ('username',)
    serializer_class = AdminUserSerializer

    # This action is working with one instance, but detail=False means that
    # DRF shouldn't create Detail View Route which requests parameter like pk.
    @action(detail=False, methods=['GET', 'PATCH'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        """Allows to view or change information about yourself. Only for
        authorized users. If given data is correct returns this data and
        HTTP200 else returns errors that have occured and HTTP400.
        """
        if request.method == 'GET':
            serializer = UserSerializer(instance=request.user)
            return Response(serializer.data, status=HTTP_200_OK)

        serializer = UserSerializer(
            data=request.data,
            instance=request.user,
            partial=True
        )
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)
