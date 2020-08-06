
# Create your views here.
from typing import List

from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from sport.apps.core.models import Machine, Exercice, Serie


def home(request):
    if request.user and request.user.is_authenticated:
        machines = Machine.objects.all()
        machines_today: List[int] = []
        for machine in machines:
            if machine.has_today_serie(request.user):
                machines_today.append(machine.id)

        context = {
            'machines': machines,
            'machines_today': machines_today,
        }
        return render(request, 'home.html', context=context)
    else:
        return redirect('login')


class HomeView(TemplateView):
    template_name = 'home.html'
    redirect = '/login'

    def get(self, request, **kwargs):
        if request.user and request.user.is_authenticated:
            return self.home(request, **kwargs)
        else:
            return redirect('login')

    def home(self, request, **kwargs):
        machines = Machine.objects.all()
        machines_today: List[int] = []
        for machine in machines:
            if machine.has_today_serie(request.user):
                machines_today.append(machine.id)

        context = {
            'machines': machines,
            'machines_today': machines_today,
        }
        return render(request, self.template_name, context=context)

class MachineView(TemplateView):
    template_name = 'machine.html'

#    @login_required
    def get(self, request, machine_id: int, **kwargs):
        exos: List[Exercice] = Exercice.objects.filter(machine__id=machine_id)
        exos_today: List[int] = []

        for exo in exos:
            if exo.has_today_serie(request.user):
                exos_today.append(exo.id)

        context = {
            'machine': Machine.objects.get(id=machine_id),
            'exercices': exos,
            'exos_today': exos_today,
        }
        return render(request, self.template_name, context=context)


class ExerciceView(TemplateView):
    template_name = 'exercice.html'

#    @login_required
    def get(self, request, exo_id, **kwargs):
        context = {
            'exercice': Exercice.objects.get(id=exo_id),
            'max': Serie.objects.filter(user=request.user).aggregate(weight=Max('weight'))
        }
        return render(request, self.template_name, context=context)


@csrf_exempt
def post_add_serie(request):
    weight = request.POST.get('weight', '0')
    reps = request.POST.get('reps', '0')
    exo_id = request.POST.get('exo_id', '0')

    if reps == '0' or (reps == '0' and weight == '0'):
        return redirect('exercice', exo_id)

    Serie(weight=weight, reps=reps, user=request.user, exercice_id=exo_id).save()
    return HttpResponse('ok')


class ErrorView(TemplateView):

    def get(self, request, code, **kwargs):
        template_name = 'errors/{}.html'.format(code)
        return render(request, template_name)


@csrf_exempt
def post_serie_delete(request):
    exo_id = request.POST['exo_id']
    serie_id = request.POST['serie_id']

    print(exo_id)
    print(serie_id)


    s= Serie.objects.get(id=serie_id)
    if s.user == request.user:
        s.delete()
        return HttpResponse('ko')
    return HttpResponse('ok')

class SeriesView(TemplateView):
    template_name = 'data/list.serie.html'

    def get(self, request, **kwargs):
        # return redirect('error', 404)

        exo_id = request.GET.get('exo_id', None)
        try:
            limit = int(request.GET.get('limit', 5))
            if limit <= 5:
                limit = 5
        except ValueError:
            limit = 5

        context = {
            'series': Serie.objects.filter(
                user_id=request.user,
		exercice_id=exo_id
            ).order_by('-date')[:limit],
        }

        return render(request, self.template_name, context=context)

def get_additionnal_info(request, page):
    cases = {
        'add_serie_success': 'info/add_serie.success.html',
        'add_serie_error': 'info/add_serie.error.html',
    }
    try:

        return render(request, cases[page])
    except KeyError:
        return HttpResponse('Failure')


@login_required
def theme_view(request, theme_name):
    themes = [
        'darkster',
        'greyson',
        'lovely',
        'monotony',
        'purple',
        'signal',
    ]
    my_theme = theme_name.strip().lower().replace(' ', '_')
    next = request.GET.get('next', None)
    if my_theme in themes:
        request.user.profile.theme = my_theme
        request.user.save()

    if next:
        return redirect(next)
    else:
        return redirect('home')
