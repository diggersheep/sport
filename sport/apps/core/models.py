from typing import List

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, Max


# Create your models here.
class Exercice(models.Model):
    """Exervice class"""
    name = models.CharField(max_length=32, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    common = models.BooleanField(default=False, null=False)
    counter = models.BooleanField(default=False, null=False)

    @classmethod
    def get_my_exercices(cls, user: User) -> List[models.Model]:
        m = cls.objects.filter(
            Q(user=user.id) | Q(common=True)
        )
        return list(m)

class Serie(models.Model):
    """Exervice class"""
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE, null=False)
    weight = models.FloatField(default=0.0)
    reps = models.IntegerField(default=0, null=False)
    date = models.DateTimeField(auto_now=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    @classmethod
    def get_home_series(cls, exos: List[Exercice]):
        results = []
        for exo in exos:
            objs = Serie.objects.filter(exercice_id=exo)
            if exo.counter:
                objs = objs.aggregate(Max('reps'))
            else:
                objs = objs.aggregate(Max('weight'))

            print(len(objs))
            if len(objs) > 0:
                results.append(objs)
                print(objs)


        return results