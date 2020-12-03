from django.db import models
from django.contrib.auth.models import User

class Ausbildung(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=10, unique=True)
    aktiv = models.BooleanField(default=True)
    def __str__(self):
        return self.slug+" - "+self.name
    class Meta:
        ordering = ['slug']
    

class Fach(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=10, unique=True)
    aktiv = models.BooleanField(default=True)
    def __str__(self):
        return self.slug+" - "+self.name
    class Meta:
        ordering = ['slug']

class Gruppe(models.Model):
    name = models.CharField(max_length=50)
    aktiv = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Teilnehmer(models.Model):
    name = models.CharField(max_length=50)
    vorname = models.CharField(max_length=50)
    ausbildung = models.ForeignKey(Ausbildung, on_delete=models.CASCADE)
    gruppe = models.ForeignKey(Gruppe, on_delete=models.CASCADE, null=True)
    aktiv = models.BooleanField(default=True)
    email = models.CharField(max_length=50)
    mobil = models.CharField(max_length=50, blank=True)
    def __str__(self):
        return self.name+", "+self.vorname+" - "+self.ausbildung.slug+" / "+str(self.gruppe)
    class Meta:
        ordering = ['name']
        
class TnInfo(models.Model):
    tn = models.ForeignKey(Teilnehmer, on_delete=models.CASCADE)
    zeitpunkt = models.DateTimeField(auto_now=False, auto_now_add=True)
    info = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    aktiv = models.BooleanField(default=True)
    def __str__(self):
        return str(self.user.username)+", "+str(self.zeitpunkt)+", "+self.info


class KanbanBereiche(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=10, unique=True)
    beschreibung = models.TextField()
    aktiv = models.BooleanField(default=True)
    def __str__(self):
        return self.name + "/" + self.slug

class KanbanProject(models.Model):
    name = models.CharField(max_length=50)
    beschreibung = models.TextField()
    stufe = models.IntegerField(default=1)
    prio = models.IntegerField()
    zeitpunkt = models.DateTimeField(auto_now=True, auto_now_add=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bereich = models.ForeignKey(KanbanBereiche, on_delete=models.CASCADE)
    aktiv = models.BooleanField(default="True")
    def __str__(self):
        return self.name+" ("+str(self.stufe)+") - "+str(self.user)
    class Meta:
        permissions = [
            ("show_all", "Kann alle Projekte sehen"),
        ]

class KanbanProtokoll(models.Model):
    kommentar = models.TextField()
    stufeNeu = models.IntegerField()
    zeitpunkt = models.TimeField(auto_now=False, auto_now_add=True)
    project = models.ForeignKey(KanbanProject, on_delete=models.CASCADE)
    def __str__(self):
        return self.project.name + " ("+self.stufeNeu+") "+str(self.zeitpunkt)+" - "+self.kommentar

class Projekt(models.Model):
    bezeichnung = models.CharField(max_length=100)
    fach = models.ForeignKey(Fach,  on_delete=models.CASCADE)
    gruppe = models.ForeignKey(Gruppe, on_delete=models.CASCADE)
    start = models.DateTimeField(auto_now=False, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username+", "+self.fach.slug+", "+self.gruppe.name+", "+str(self.start)+", "+self.bezeichnung

class ProjekteTN(models.Model):
    teilnehmer = models.ForeignKey(Teilnehmer, on_delete=models.CASCADE)
    projekt = models.ForeignKey(Projekt, on_delete=models.CASCADE)
    bis = models.DateTimeField(auto_now=False, auto_now_add=False)
    abgabe = models.DateTimeField(auto_now=False, auto_now_add=True)
    bewertung = models.IntegerField(default=0)
    kommentar = models.CharField(max_length=100, default="")
    offen = models.BooleanField(default=True)
    def __str__(self):
        return self.teilnehmer.name+", "+self.projekt.bezeichnung
