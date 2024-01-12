"""Defines URL patterns for learning_logs."""

from django.urls import path
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from users.forms import AuthenticationFormNew


from . import views

app_name = 'users'
urlpatterns = [
    path('', include('userpanel.urls')),
    # 2FA
    path('2fa/', include('django_mfa.urls')),

    path('settings/', user_views.usersettings, name='settings'),
   
   
    path('login/', user_views.LoginNew.as_view(redirect_authenticated_user=True, template_name='users/login.html', authentication_form=AuthenticationFormNew), name='login'),
    path('profile/', user_views.profile, name='profile'),
    path('register/', user_views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-change/', user_views.UpdatePassword.as_view(),
         name="password-change"),
    path('password-change/password-changed/',
         user_views.passwordchanged, name="password-changed"),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password-reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password-reset-complete.html'
         ),
         name='password_reset_complete'),

]