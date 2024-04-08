from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import LoginUserForm, UserRegisterForm, UserProfileForm


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'user/login.html'

    def get_success_url(self):
        return reverse_lazy('main:home')


class LogoutUserView(LogoutView):
    template_name = 'user/logout.html'


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'user/registration.html'
    success_url = reverse_lazy('user:login')


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserProfileForm
    template_name = 'user/profile.html'

    def get_success_url(self):
        return reverse_lazy('user:profile')

    def get_object(self, queryset=None):
        return self.request.user
