from django.urls import path

from .views import UserRegister, ProfileView, UserLogin, UserLogout


urlpatterns = [
    path('register/', UserRegister.as_view(), name='register-user'),
    path('', ProfileView.as_view(), name='profile-detail'),
    path('login/', UserLogin.as_view(), name='login-user'),
    path('logout/', UserLogout.as_view(), name='logout-user'),
]
