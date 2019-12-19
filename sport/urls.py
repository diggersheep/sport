from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path

from sport.apps.core.views import HomeView, MachineView, ExerciceView
from sport.apps.login.views import LoginView, LogoutView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('admin/', admin.site.urls),

    path('machine/<int:machine_id>', MachineView.as_view(), name='machine'),
    path('exercice/<int:exo_id>', ExerciceView.as_view(), name='exercice'),
]
