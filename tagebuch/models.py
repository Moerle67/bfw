from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    name = models.CharField(("Bezeichnung"), max_length=50)
    description = models.TextField(("Beschreibung"), blank= True, null=True) 
    privat = models.BooleanField(("Privat"), default = False)
    aktiv = models.BooleanField(("Aktiv"), default = True)

    class Meta:
        verbose_name = ("Projekt")
        verbose_name_plural = ("Projekte")

    def __str__(self):
        privat = "privat" if self.privat else "beruflich"
        aktiv = "aktiv" if self.aktiv else "inaktiv"
        return f"{self.name} ({privat}/{aktiv})"

    def get_absolute_url(self):
        return reverse("Project_detail", kwargs={"pk": self.pk})




class Entry(models.Model):
    task = models.CharField(("Tätigkeit"), max_length=50)
    description = models.TextField(("Beschreibung"), blank= True, null=True)
    begin = models.DateTimeField(("Start "), auto_now=False, auto_now_add=True)
    end = models.DateTimeField(("Ende"), auto_now=True, auto_now_add=False)
    project = models.ForeignKey(Project, verbose_name=("Projekt"), on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Eintrag")
        verbose_name_plural = ("Einträge")

    def __str__(self):
        return f"{self.task}/{self.user} ({self.project}:{self.begin} - {self.end})"

    def get_absolute_url(self):
        return reverse("Eintrag_detail", kwargs={"pk": self.pk})

