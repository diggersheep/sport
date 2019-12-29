from typing import List

from django import template
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, Max, Count
from django.db.models.functions import TruncMonth
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.datetime_safe import datetime


class Machine(models.Model):
    name = models.CharField(max_length=32)
    picture = models.CharField(max_length=32, null=True)

    def has_today_serie(self):
        exos = Exercice.objects.filter(
            machine=self
        )
        for exo in exos:
            if Exercice.has_today_serie(exo.id):
                return True
        return False


class Exercice(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    setting = models.CharField(max_length=32, default='')
    description = models.CharField(max_length=256, default='')

    def has_today_serie(self):
        objs = Serie.objects.filter(
            exercice=self,
            date__gte=datetime.now().replace(hour=0, minute=0, second=0),
        )
        return len(objs) > 0


class Serie(models.Model):
    """Exervice class"""
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    weight = models.FloatField(default=0.0)
    reps = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=16, default='purple')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()






