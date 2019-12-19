from typing import List

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, Max

class Machine(models.Model):
    name = models.CharField(max_length=32)
    picture = models.CharField(max_length=32, null=True)

class Exercice(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    setting = models.CharField(max_length=32, default='')
    description = models.CharField(max_length=256, default='')

class Serie(models.Model):
    """Exervice class"""
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    weight = models.FloatField(default=0.0)
    reps = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)