from typing import Any, Dict

from django import forms
from django.core.exceptions import ObjectDoesNotExist

from sport.apps.core.models import Machine, Exercise


class MachineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        code: str = cleaned_data.get('code', None)

        if code is not None and isinstance(code, str) and code.strip() != '':
            ok: bool = False
            try:
                Machine.objects.get(code=code)
            except ObjectDoesNotExist:
                ok = True
                # todo: i18n
            if not ok:
                raise forms.ValidationError({'code': 'Ce code existe déjà pour une autre machine'})
        else:
            # todo: i18n
            raise forms.ValidationError({'code': 'Pas de code ou code non valide'})

        # todo: picture validation
        return cleaned_data

    class Meta:
        model = Machine
        fields = ('id', 'name', 'code', 'picture')


class ExerciseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data: Dict[str, Any] = super().clean()
        setting: str = cleaned_data.get('setting')
        machine_id: int = cleaned_data.get('machine')

        ok: bool = False
        try:
            Exercise.objects.get(machine_id=machine_id, setting=setting)
        except ObjectDoesNotExist:
            ok = True

        if not ok:
            raise forms.ValidationError({'setting': 'Une exercice a déjà cette configuration'})

        return cleaned_data

    class Meta:
        model = Exercise
        fields = ('machine', 'setting', 'description')

        widgets = {
            'setting': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'maximum 256 caractères', 'class': 'form-control'}),
        }

