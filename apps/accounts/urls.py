from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.home, name="home"),
    path("entrar/", views.LoginView.as_view(), name="login"),
    path("sair/", auth_views.LogoutView.as_view(), name="logout"),
    path("senha/alterar/", views.PasswordChangeView.as_view(), name="password_change"),
    path("senha/alterada/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("senha/recuperar/", views.PasswordResetView.as_view(), name="password_reset"),
    path("senha/recuperar/enviado/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("senha/redefinir/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("senha/redefinida/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("usuarios/", views.user_list, name="user_list"),
    path("usuarios/novo/", views.user_create, name="user_create"),
    path("usuarios/<int:pk>/editar/", views.user_edit, name="user_edit"),
    path("usuarios/<int:pk>/senha/", views.user_set_password, name="user_set_password"),
]
