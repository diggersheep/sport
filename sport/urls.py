from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path

from sport.apps.core import views
from sport.apps.core.views import ErrorView, SeriesView, \
    post_serie_delete, post_add_serie, get_additionnal_info, theme_view
from sport.apps.login.views import LoginView, LogoutView
from sport.apps.stats.views import StatsView

urlpatterns = [
    path('', views.home, name="home"),
    path('error/<int:code>', ErrorView.as_view(), name="error"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('admin/', admin.site.urls),

    path('machine/<int:machine_id>', views.machine, name='machine'),
    path('exercise', post_serie_delete, name='del_serie'),
    path('exercise/<int:exo_id>', views.exercise, name='exercise'),
    path('exercise/add_serie/', post_add_serie, name='add_serie'),

    path('stats/', StatsView.as_view(), name='stats'),
    path('series/', SeriesView.as_view(), name='series'),

    path('info/<str:page>', get_additionnal_info, name='info'),
    path('theme/<str:theme_name>', theme_view, name='theme'),
]
