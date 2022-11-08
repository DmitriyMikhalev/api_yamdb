from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, signup, token)

app_name = 'api_v1'

router_v1 = DefaultRouter()
router_v1.register(prefix='categories', viewset=CategoryViewSet)
router_v1.register(prefix='genres', viewset=GenreViewSet)
router_v1.register(prefix='titles', viewset=TitleViewSet)
router_v1.register(prefix='users', viewset=UserViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', token, name='token'),
    path('', include(router_v1.urls)),
]
