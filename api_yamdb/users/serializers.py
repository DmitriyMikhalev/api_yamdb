from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (CharField, ChoiceField, EmailField,
                                        ModelSerializer, Serializer)

from .models import ROLE_CHOICES, USER, User


class ValidateUsernameEmailMixin:
    """Every custom serializer for users contains validate_email() and
    validate_username methods. This mixin created for inherit his behavior.
    """
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


class BaseUserSerializer(ModelSerializer, ValidateUsernameEmailMixin):
    """Base user serializer. Inherit validation methods for email and
    username. Provides choosing roles with default value 'user'.
    Content is equal to admin serializer.
    """
    email = EmailField(max_length=254, required=True)
    role = ChoiceField(choices=ROLE_CHOICES, default=USER)

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


class AdminUserSerializer(BaseUserSerializer):
    pass


class SignUpSerializer(ModelSerializer, ValidateUsernameEmailMixin):
    email = EmailField(max_length=254, required=True)

    class Meta:
        fields = ('email', 'username',)
        model = User


class TokenSerializer(Serializer):
    confirmation_code = CharField(required=True)
    username = CharField(required=True)


class UserSerializer(BaseUserSerializer):
    role = CharField(read_only=True)
    username = CharField(required=True)
