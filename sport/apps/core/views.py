
# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'
    redirect = '/login'

    def get(self, request, **kwargs):
        if request.user and request.user.is_authenticated:
            return self.home(request, **kwargs)
        else:
            return HttpResponseRedirect(self.redirect)

    def home(self, request, **kwargs):
        from sport.apps.core.models import Exercice, Serie


        exos = Exercice.get_my_exercices(request.user)
        measures = Serie.get_home_series(exos)
        context = {
            'exos': exos
        }
        return render(request, self.template_name, context=context)
