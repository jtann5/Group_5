
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import index, application, maintenance, add_user_account, success_view, CustomLoginView
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', index, name='index'),
    path('forms/application', application, name='application'),
    path('forms/maintenance', maintenance, name='maintenance'),
    path('add_user_account/', add_user_account, name='add_user_account'),
    path('success/', success_view, name='success_view'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')
]