from django.contrib import admin

# Register your models here.
from sport.apps.core.models import Serie, Exercice, Machine, Profile

admin.site.register(Serie)
admin.site.register(Exercice)
admin.site.register(Machine)
admin.site.register(Profile)
