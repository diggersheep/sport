import os
from typing import Iterable

import PIL
from PIL import Image
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.datetime_safe import datetime


class Machine(models.Model):
    THUMB_WIDTH = 300

    name = models.CharField(max_length=32)
    code = models.CharField(max_length=32, null=True, blank=True)
    # picture = models.CharField(max_length=32, null=True)
    picture = models.ImageField(upload_to='machines', null=True)

    def __str__(self) -> str:
        return str(self.name)

    def has_today_serie(self, user) -> bool:
        exercises: Iterable[Exercise] = Exercise.objects.filter(
            machine=self
        )
        for exercise in exercises:
            if Exercise.has_today_serie(exercise.id, user=user):
                return True
        return False

    def save(self, *args, **kwargs):
        extension: str = os.path.splitext(self.picture.name)[1]
        new_name: str = f'machines/machine_{self.name}{extension}'

        if self.picture.name != new_name:
            new_path: str = os.path.join(settings.MEDIA_ROOT, new_name)
            os.rename(self.picture.path, new_path)
            self.picture.name = new_name
        self.resize_image()
        super(Machine, self).save(*args, **kwargs)

    def resize_image(self) -> None:
        img: PIL.Image = Image.open(self.picture)
        w, h = img.size
        alpha: float = self.THUMB_WIDTH / w
        new_w: int = int(w * alpha)
        new_h: int = int(h * alpha)

        if w != new_w or h != new_h:
            new_image: Image = img.resize((new_w, new_h), Image.LANCZOS)
            new_image.save(self.picture.path)


class Exercise(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    setting = models.CharField(max_length=32, default='')
    description = models.CharField(max_length=256, default='')

    def __str__(self) -> str:
        return f'{self.machine.name} - {self.setting}'

    def has_today_serie(self, user) -> bool:
        series: QuerySet = Serie.objects.filter(
            exercise=self,
            date__gte=datetime.now().replace(hour=0, minute=0, second=0),
            user=user,
        )
        return len(series) > 0


class Serie(models.Model):
    """Exercise class"""
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    weight = models.FloatField(default=0.0)
    reps = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return '[{}@{}] {} {} - w:{} - r:{}'.format(
            self.user.username,
            self.date,
            self.exercise.machine.name,
            self.exercise.setting,
            self.weight,
            self.reps
        )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=16, default='purple')

    def __str__(self) -> str:
        return str(self.user.username)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()






