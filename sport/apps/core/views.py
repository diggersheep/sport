# Create your views here.
from typing import (List, Optional, Iterable, Dict, Any)

from django.contrib.auth.decorators import login_required
from django.db.models import Max, QuerySet
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from sport.apps.core.forms import MachineForm, ExerciseForm
from sport.apps.core.models import Machine, Exercise, Serie


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


@login_required
def machine(request, machine_id: int, **kwargs):
    exercises: List[Exercise] = Exercise.objects.filter(machine__id=machine_id)
    exercises_today: List[int] = []

    for exo in exercises:
        if exo.has_today_serie(request.user):
            exercises_today.append(exo.id)

    context = {
        'machine': Machine.objects.get(id=machine_id),
        'exercises': exercises,
        'exercises_today': exercises_today,
    }
    return render(request, 'machine.html', context=context)


@login_required
def exercise(request, exo_id, **kwargs):
    context = {
        'exercise': Exercise.objects.get(id=exo_id),
        'max': Serie.objects.filter(user=request.user).aggregate(weight=Max('weight'))
    }
    return render(request, 'exercise.html', context=context)


@csrf_exempt
@login_required
def post_add_serie(request):
    weight = request.POST.get('weight', '0')
    reps = request.POST.get('reps', '0')
    exo_id = request.POST.get('exo_id', '0')

    if reps == '0' or (reps == '0' and weight == '0'):
        return redirect('exercise', exo_id)

    Serie(weight=weight, reps=reps, user=request.user, exercise_id=exo_id).save()
    return HttpResponse('ok')


def get_error(request, code, **kwargs):
    template_name = 'errors/{}.html'.format(code)
    return render(request, template_name)


@csrf_exempt
@login_required
def post_serie_delete(request):
    # exercise_id = request.POST['exo_id']
    serie_id: int = int(request.POST['serie_id'])

    s: Serie = Serie.objects.get(id=serie_id)
    if s.user == request.user:
        s.delete()
        return HttpResponse('ko')
    return HttpResponse('ok')


@login_required
def get_series(request, **kwargs):
    limit: int = 5
    exo_id: Optional[int] = request.GET.get('exo_id', None)
    try:
        limit = int(request.GET.get('limit', 5))
        if limit <= 5:
            limit = 5
    except ValueError:
        pass

    series: Iterable[Serie] = Serie.objects.filter(
        user_id=request.user,
        exercise_id=exo_id
    ).order_by('-date')[:limit]

    context: Dict[str, Iterable[Serie]] = {'series': series}
    return render(request, 'data/list.serie.html', context=context)


def get_additional_info(request, page):
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


@login_required
def add_new_machine(request):
    if not request.user.is_superuser:
        return redirect('error', 403)

    form: MachineForm = MachineForm()
    if request.method == 'POST':
        form = MachineForm(request.POST, request.FILES)
        print(request.POST)
        print(request.FILES)
        if form.is_valid():
            print('valid')
            form.save()
        else:
            print('not valid')
        ctx: Dict[str, MachineForm] = {'machine_form': form}
        return render(request, 'core/add_machine.html', context=ctx)
    else:
        ctx: Dict[str, MachineForm] = {'machine_form': form}
        return render(request, 'core/add_machine.html', context=ctx)


@login_required
def add_machine_code(request):

    if request.method == 'POST':
        machine_id: int = int(request.POST.get('id'))
        instance: Machine = Machine.objects.get(id=machine_id)
        data: Dict[str, Any] = request.POST.copy()
        data['name'] = instance.name
        form = MachineForm(data=data, instance=instance)

        if form.is_valid():
            form.save()
            return redirect('machine', instance.id)
        else:
            machines_without_code: Iterable[Machine] = Machine.objects.filter(code__isnull=True).order_by('name')
            ctx: Dict[str, Any] = {
                'machines': machines_without_code,
                'machine_form': form,
                'machine_id': 0,
            }
            return render(request, 'core/add_machine_code.html', context=ctx)

    machines_without_code: Iterable[Machine] = Machine.objects.filter(code__isnull=True).order_by('name')
    ctx: Dict[str, Any] = {
        'machines': machines_without_code,
        'machine_id': int(request.GET.get('id', 0)),
    }
    return render(request, 'core/add_machine_code.html', context=ctx)


@login_required
def redirect_machine_by_code(request, code: str):
    return redirect('machine', Machine.objects.get(code=code).id)


@login_required
def new_exercise(request, machine_id):
    machine: Machine = Machine.objects.get(id=machine_id)
    exercises = Exercise.objects.filter(machine=machine).order_by('setting')
    form: ExerciseForm = ExerciseForm()

    ctx: Dict[str, Any] = {
        'machine': machine,
        'exercises': exercises,
        'exercise_form': form,
    }

    if request.method == 'POST':
        form = ExerciseForm(data=request.POST.copy())
        if form.is_valid():
            form.save()
        else:
            ctx['exercise_form'] = form
            return render(request, 'core/new_exo.html', context=ctx)

        operation: str = request.POST.get('operation')
        if operation == 'add':
            return redirect('exercise', form.instance.id)
        elif operation == 'readd':
            pass

    return render(request, 'core/new_exo.html', context=ctx)