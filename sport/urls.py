from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path

from sport.apps.core.views import HomeView
from sport.apps.login.views import LoginView, LogoutView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('admin/', admin.site.urls),
]
