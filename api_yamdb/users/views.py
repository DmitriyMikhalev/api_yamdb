from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdmin
from .serializers import (AdminUsersSerializer, SignUpSerializer,
                          TokenSerializer, UserSerializer)
from .utils import send_verify_code


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)

    user = serializer.save()
    send_verify_code(user)

    return Response(data=serializer.data, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
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
    search_fields = ('username',)
    serializer_class = AdminUsersSerializer
    queryset = User.objects.all()

    # This action is working with one instance, but detail=False means that
    # DRF shouldn't create Detail View Route which required param like pk.
    @action(methods=['GET', 'PATCH'], detail=False,
            permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(instance=request.user)
            return Response(serializer.data, status=HTTP_200_OK)

        serializer = UserSerializer(
            instance=request.user,
            data=request.data,
            partial=True
        )
        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)
