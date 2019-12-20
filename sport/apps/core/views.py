
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from sport.apps.core.models import Machine, Exercice, Serie


class HomeView(TemplateView):
    template_name = 'home.html'
    redirect = '/login'

    def get(self, request, **kwargs):
        if request.user and request.user.is_authenticated:
            return self.home(request, **kwargs)
        else:
            return redirect('login')

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
            'series': Serie.objects.filter(exercice__id=exo_id, user=request.user).order_by('-date')[:5],
            'max': Serie.objects.filter(user=request.user).aggregate(weight=Max('weight'))
        }
        return render(request, self.template_name, context=context)

    def post(self, request, exo_id):
        weight = request.POST.get('weight', '0')
        reps = request.POST.get('reps', '0')

        if reps == '0' or (reps == '0' and weight == '0'):
            return redirect('exercice', exo_id)

        Serie(weight=weight, reps=reps, user=request.user, exercice_id=exo_id).save()
        return redirect('exercice', exo_id)


class ErrorView(TemplateView):

    def get(self, request, code, **kwargs):
        template_name = 'errors/{}.html'.format(code)
        return render(request, template_name)




class SerieDelView(TemplateView):
    def post(self, request):
        exo_id = request.POST.get('exo_id', None)
        serie_id = request.POST.get('serie_id', None)

        print(exo_id)
        print(serie_id)

        Serie.objects.get(id=serie_id).delete()
        return redirect('exercice', exo_id)

    def get(self, request, **kwargs):
        return redirect('error', 404)

