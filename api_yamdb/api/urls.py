from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet, UserViewSet,
                    signup, token)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(prefix='categories', viewset=CategoryViewSet)
router_v1.register(prefix='genres', viewset=GenreViewSet)
router_v1.register(prefix='titles', viewset=TitleViewSet)
router_v1.register(prefix='users', viewset=UserViewSet)


urlpatterns = [
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', token, name='token'),
    path('v1/', include(router_v1.urls)),
]
