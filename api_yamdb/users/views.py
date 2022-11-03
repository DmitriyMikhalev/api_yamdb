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
from .serializers import (AdminUserSerializer, SignUpSerializer,
                          TokenSerializer, UserSerializer)
from .utils import send_verify_code


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
