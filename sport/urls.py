from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path

from sport.apps.core import views
from sport.apps.login.views import (LoginView, LogoutView)
from sport.apps.stats.views import StatsView

urlpatterns = [
    path('', views.home, name="home"),
    path('error/<int:code>', views.get_error, name="error"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('admin/', admin.site.urls),

    path('machine/new/', views.add_new_machine, name='new_machine'),
    path('machine/code/', views.add_machine_code, name='add_machine_code'),
    path('machine/code/<str:code>', views.redirect_machine_by_code, name='machine_code'),
    path('machine/<int:machine_id>', views.machine, name='machine'),
    path('machine/<int:machine_id>/new_exercise', views.new_exercise, name="new_exercise"),

    path('exercise', views.post_serie_delete, name='del_serie'),
    path('exercise/<int:exo_id>', views.exercise, name='exercise'),
    path('exercise/add_serie/', views.post_add_serie, name='add_serie'),

    path('stats/', StatsView.as_view(), name='stats'),
    path('series/', views.get_series, name='series'),

    path('info/<str:page>', views.get_additional_info, name='info'),
    path('theme/<str:theme_name>', views.theme_view, name='theme'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
