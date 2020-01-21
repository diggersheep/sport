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

    def __str__(self):
        return str(self.name)

    def has_today_serie(self, user):
        exos = Exercice.objects.filter(
            machine=self
        )
        for exo in exos:
            if Exercice.has_today_serie(exo.id, user=user):
                return True
        return False


class Exercice(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    setting = models.CharField(max_length=32, default='')
    description = models.CharField(max_length=256, default='')

    def __str__(self):
        return '{} - {}'.format(self.machine.name, self.setting)

    def has_today_serie(self, user):
        objs = Serie.objects.filter(
            exercice=self,
            date__gte=datetime.now().replace(hour=0, minute=0, second=0),
            user=user,
        )
        return len(objs) > 0


class Serie(models.Model):
    """Exervice class"""
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    weight = models.FloatField(default=0.0)
    reps = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '[{}@{}] {} {} - w:{} - r:{}'.format(
            self.user.username,
            self.date,
            self.exercice.machine.name,
            self.exercice.setting,
            self.weight,
            self.reps
        )

    def get_date(self):
        return self.date.strftime('%Y-%m-%d')



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=16, default='purple')

    def __str__(self):
        return str(self.user.username)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()






