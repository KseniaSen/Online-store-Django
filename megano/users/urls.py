from django.urls import path
from .views import (
    ProfileDetail,
    PasswordUpdateView,
    AvatarUpdateView,
    SingInView,
    SingOutView,
    SingUpView,
)
app_name = 'users'


urlpatterns = [
    path('api/sign-in', SingInView.as_view(), name='sing-in'),
    path('api/sign-out', SingOutView.as_view(), name='sing-out'),
    path('api/sign-up', SingUpView.as_view(), name='sing-up'),
    path('api/profile', ProfileDetail.as_view(), name='profile'),
    path('api/profile/avatar', AvatarUpdateView.as_view(), name='avatar'),
    path('api/profile/password', PasswordUpdateView.as_view(), name='password'),
]
