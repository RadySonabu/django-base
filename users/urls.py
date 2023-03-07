from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # authentication
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name="activate"),
    path('check-email/', views.CheckEmailView.as_view(), name="check-email"),
    path('success/', views.SuccessView.as_view(), name="success"),

    # reset password
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name = "users/reset_password.html"), name ='reset_password'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name = "users/password_reset_sent.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "users/password_reset_form.html"), name ='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "users/password_reset_done.html"), name ='password_reset_complete'),


    path("login/", auth_views.LoginView.as_view(redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('change-password/', auth_views.PasswordChangeView.as_view(
            template_name='users/change-password.html',
            success_url = '/'
        ),
        name='change-password'
    ),

    path("", views.Dashboard.as_view(), name="home"),
    path("settings/", views.SettingsPage.as_view(), name="settings"),

    
]
