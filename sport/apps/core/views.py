
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from sport.apps.core.models import Machine, Exercice, Serie


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

        context = {
            'machines': Machine.objects.all()
        }
        return render(request, self.template_name, context=context)

class MachineView(TemplateView):
    template_name = 'machine.html'

#    @login_required
    def get(self, request, machine_id, **kwargs):
        context = {
            'machine': Machine.objects.get(id=machine_id),
            'exercices': Exercice.objects.filter(machine__id=machine_id)
        }
        return render(request, self.template_name, context=context)


class ExerciceView(TemplateView):
    template_name = 'exercice.html'

#    @login_required
    def get(self, request, exo_id, **kwargs):
        context = {
            'exercice': Exercice.objects.get(id=exo_id),
            'series': Serie.objects.filter(exercice__id=exo_id)
        }
        return render(request, self.template_name, context=context)

