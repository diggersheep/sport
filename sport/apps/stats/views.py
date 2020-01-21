
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from sport.apps.core.models import Machine, Exercice, Serie
from sport.apps.stats.utils import Stats


class StatsView(TemplateView):
    template_name = 'stats.html'

    def get(self, request, **kwargs):
        stats = Stats(user=request.user)
        stats.all()
        context = {
            'stats': stats
        }
        return render(request, self.template_name, context=context)

