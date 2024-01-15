from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Bereich(models.Model):
    title = models.CharField(("Titel"), max_length=100)
    beschreibung = models.TextField(("Beschreibung"), blank=True, null=True)
    
    class Meta:
        verbose_name = ("Bereich")
        verbose_name_plural = ("Bereiche")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Bereich_detail", kwargs={"pk": self.pk})

class Project(models.Model):
    title = models.CharField(("Titel"), max_length=100)
    class Meta:
        verbose_name = ("Projekt")
        verbose_name_plural = ("Projekte")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Project_detail", kwargs={"pk": self.pk})


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = ("Aufgabe")
        verbose_name_plural = ("Aufgaben")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Task_detail", kwargs={"pk": self.pk})
