from django.urls import path

from user import views

app_name = "user"


urlpatterns = [
    path("signup/", views.CreateUserView.as_view(), name="signup"),
    path("auth/login/", views.CreateLoginTokenView.as_view(), name="login"),
]
