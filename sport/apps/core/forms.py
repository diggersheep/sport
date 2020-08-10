from django import forms
from django.core.exceptions import ObjectDoesNotExist

from sport.apps.core.models import Machine


class MachineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        name: str = cleaned_data.get('name', None)
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
