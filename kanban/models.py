from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Bereich(models.Model):
    title = models.CharField(("Titel"), max_length=100)
    description = models.TextField(("Beschreibung"), blank=True, null=True)
    
    class Meta:
        verbose_name = ("Bereich")
        verbose_name_plural = ("Bereiche")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Bereich_detail", kwargs={"pk": self.pk})

class Project(models.Model):
    title = models.CharField(("Titel"), max_length=100)
    privat = models.BooleanField(("Privat"))
    field = models.ForeignKey(Bereich, verbose_name=("Bereich"), on_delete=models.CASCADE)
    prio = models.IntegerField(("Priorität"))
    class Meta:
        verbose_name = ("Projekt")
        verbose_name_plural = ("Projekte")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Project_detail", kwargs={"pk": self.pk})


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(("Titel"), max_length=50)
    description = models.TextField(("Beschreibung"), null = True, blank = True)
    project = models.ForeignKey(Project, verbose_name=("Projekt"), on_delete=models.CASCADE)
    cyclical = models.BooleanField(("Zyklisch"), default=False)
    complete = models.BooleanField(("Fertig"), default=False)
    class Meta:
        verbose_name = ("Aufgabe")
        verbose_name_plural = ("Aufgaben")

    def __str__(self):
        return f"{self.title}/{self.project}/{self.user}"

    def get_absolute_url(self):
        return reverse("Task_detail", kwargs={"pk": self.pk})
