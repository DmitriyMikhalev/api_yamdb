from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('v1/auth/signup/', views.signup, name='signup'),
    path('v1/auth/token/', views.token, name='token')
]
