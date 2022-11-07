from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import (CharField, ChoiceField,
                                        CurrentUserDefault, EmailField,
                                        IntegerField, ModelSerializer,
                                        Serializer, SlugRelatedField,
                                        ValidationError)

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
    review = SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'


class GenreSerializer(ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class ReviewSerializer(ModelSerializer):
    title = SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = SlugRelatedField(
        default=CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Вы не можете добавить более'
                                      'одного отзыва на произведение')
        return data

    class Meta:
        model = Review
        fields = '__all__'


class SignUpSerializer(ModelSerializer, ValidateUsernameEmailMixin):
    email = EmailField(max_length=254, required=True)

    class Meta:
        fields = ('email', 'username',)
        model = User


class TitleSerializer(ModelSerializer):
    genre = SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            '__all__'
        )


class ReadOnlyTitleSerializer(ModelSerializer):
    rating = IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class TokenSerializer(Serializer):
    confirmation_code = CharField(required=True)
    username = CharField(required=True)


class UserSerializer(BaseUserSerializer):
    role = CharField(read_only=True)
    username = CharField(required=True)
