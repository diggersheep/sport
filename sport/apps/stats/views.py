
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from sport.apps.core.models import Machine, Exercice, Serie


class StatsView(TemplateView):
    template_name = 'stats.html'

    def get(self, request, **kwargs):
        return render(request, self.template_name)

