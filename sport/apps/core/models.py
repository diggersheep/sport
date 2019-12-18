from typing import List

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


# Create your models here.
class Exercice(models.Model):
    """Exervice class"""
    name = models.CharField(max_length=32, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    common = models.BooleanField(default=False, null=False)

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
    date = models.DateTimeField(auto_now=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    counter = models.BooleanField(default=False, null=False)