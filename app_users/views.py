from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import UserRegistrationForm

from app_service.models import CSVFile


class UserRegister(generic.FormView):
    """
    Представление регистрации пользователя
    """
    template_name = 'app_users/register.html'
    form_class = UserRegistrationForm
    fields = ('first_name', 'last_name', 'username', 'password')

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('profile-detail')

        return super().post(request, *args, **kwargs)


class UserLogin(LoginView):
    """
    Представление авторизации пользователя
    """
    template_name = 'app_users/login.html'
    next_page = reverse_lazy('profile-detail')


class UserLogout(LogoutView):
    """
    Представление выхода пользователя из системы
    """
    next_page = reverse_lazy('main-page')


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    """
    Представление страницы профиля
    """
    template_name = 'app_users/detail.html'
    login_url = reverse_lazy('login-user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files'] = CSVFile.objects.filter(user=self.request.user)

        return context
