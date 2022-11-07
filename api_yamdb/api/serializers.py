from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (CharField, ChoiceField,
                                        CurrentUserDefault, EmailField,
                                        ModelSerializer, Serializer,
                                        SlugRelatedField, ValidationError)
from reviews.models import (ROLE_CHOICES, USER, Category, Comment, Genre,
                            Review, Title, User)


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


class CategorySerializer(ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = '__all__'


class GenreSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        if self.context['request'] != 'POST':
            return data
        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(
            author=author,
            title=title_id
        ).exists():
            raise ValidationError(
                'Вы уже написали отзыв к этому произведению.'
            )
        return data

    def validate(self, value):
        if not 1 <= value <= 10:
            raise ValidationError(
                'Оценкой может быть целое число в диапазоне от 1 до 10.'
            )
        return value


class SignUpSerializer(ModelSerializer, ValidateUsernameEmailMixin):
    email = EmailField(max_length=254, required=True)

    class Meta:
        fields = ('email', 'username',)
        model = User


class TitleSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Title


class TokenSerializer(Serializer):
    confirmation_code = CharField(required=True)
    username = CharField(required=True)


class UserSerializer(BaseUserSerializer):
    role = CharField(read_only=True)
    username = CharField(required=True)
