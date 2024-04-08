from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy
from .views import LoginUserView, LogoutUserView, UserRegisterView, UserProfileView

app_name = 'user'

urlpatterns = [
    # Общее
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('registration/', UserRegisterView.as_view(), name='registration'),
    path('profile/', UserProfileView.as_view(), name='profile'),

    # Смена пароля
    path('password-change/', PasswordChangeView.as_view(
        template_name='user/password_change_form.html',
        success_url=reverse_lazy('user:password_change_done')), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name='user/password_change_done.html'), name='password_change_done'),

    # Восстановление пароля
    path('password-reset/', PasswordResetView.as_view(
        template_name='user/password_reset_form.html',
        email_template_name="user/password_reset_email.html",
        success_url=reverse_lazy('user:password_reset_done')
    ), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='user/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='user/password_reset_confirm.html',
        success_url=reverse_lazy("user:password_reset_complete")
    ), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(
        template_name='user/password_reset_complete.html'
    ), name='password_reset_complete'),
]
