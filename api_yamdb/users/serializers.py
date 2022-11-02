from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (CharField, ChoiceField, EmailField,
                                        ModelSerializer, Serializer)

from .models import ROLE_CHOICES, USER, User


class SignUpSerializer(ModelSerializer):
    email = EmailField(required=True, max_length=254)

    class Meta:
        fields = ('email', 'username',)
        model = User

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise ValidationError(
                'Пользователь с таким email уже существует.'
            )

        return value

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(
                'Запрещено использовать "me" в качестве имени пользователя'
            )

        return value


class AdminUsersSerializer(ModelSerializer):
    role = ChoiceField(choices=ROLE_CHOICES, default=USER)
    email = EmailField(required=True, max_length=254)

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise ValidationError(
                'Пользователь с таким email уже существует.'
            )

        return value

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(
                'Запрещено использовать "me" в качестве имени пользователя'
            )

        return value


class TokenSerializer(Serializer):
    confirmation_code = CharField(required=True)
    username = CharField(required=True)


class UserSerializer(ModelSerializer):
    role = CharField(read_only=True)
    email = EmailField(required=True, max_length=254)
    username = CharField(required=True)

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise ValidationError(
                'Пользователь с таким email уже существует.'
            )

        return value

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError(
                'Запрещено использовать "me" в качестве имени пользователя'
            )

        return value
