from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'users'

router_v1 = DefaultRouter()
router_v1.register(prefix=r'^users', viewset=views.UserViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', views.signup, name='signup'),
    path('v1/auth/token/', views.token, name='token')
]
