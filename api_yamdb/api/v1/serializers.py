from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (CharField, ChoiceField,
                                        CurrentUserDefault, EmailField,
                                        IntegerField, ModelSerializer,
                                        Serializer, SlugRelatedField,
                                        ValidationError)

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import ROLE_CHOICES, USER, User


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

        if User.objects.filter(username__iexact=value).exists():
            raise ValidationError(
                'Пользователь с таким username уже существует.'
            )

        return value


class UserSerializer(ModelSerializer, ValidateUsernameEmailMixin):
    """Base user serializer. Inherit validation methods for email and
    username. Provides choosing roles with default value 'user'.
    """
    email = EmailField(required=True)
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


class CategorySerializer(ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = (
            'id',
            'text',
            'pub_date',
            'author',
        )
        model = Comment


class GenreSerializer(ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class ReviewSerializer(ModelSerializer):
    """Serializer для отзывов и оценок"""
    author = SlugRelatedField(
        default=CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        if (request.method not in ('GET', 'PATCH')
            and Review.objects.filter(
            title_id=title_id,
            author=author
        ).exists()):
            raise ValidationError('Может существовать только один отзыв!')
        return data

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )
        model = Review


class SignUpSerializer(ModelSerializer, ValidateUsernameEmailMixin):
    email = EmailField(required=True)

    class Meta:
        fields = ('email', 'username',)
        model = User


class TitleSerializer(ModelSerializer):
    category = SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )

    class Meta:
        fields = (
            'id',
            'category',
            'description',
            'genre',
            'name',
            'year',
        )
        model = Title


class ReadOnlyTitleSerializer(ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        model = Title


class TokenSerializer(Serializer):
    confirmation_code = CharField(required=True)
    username = CharField(required=True)


class UserSerializerProtected(UserSerializer):
    """Serializer with similar capabilities to the parent class but role field
    isn't mutable. For example, if user wants to GET or PATCH info about
    himself, GET request will give response with role field and PATCH request
    will ignore changing role and give response with that field.
    """
    role = CharField(read_only=True)
