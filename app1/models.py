# todo
# Gruppe erhalten bei E-Mail übertragen
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import BooleanField, TextField
from django.db.models.fields.related import ForeignKey
from django.db.models.query_utils import check_rel_lookup_compatibility
from django.utils import timezone

class Ausbildung(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=10, unique=True)
    aktiv = models.BooleanField(default=True)
    def __str__(self):
        return self.slug+" - "+self.name
    class Meta:
        ordering = ['slug']
        verbose_name_plural = "Ausbildungen"

class Fach(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=10, unique=True)
    aktiv = models.BooleanField(default=True)
    def __str__(self):
        return self.slug+" - "+self.name
    class Meta:
        ordering = ['slug']
        verbose_name_plural = "Fächer"

class Raum(models.Model):
    standort = models.CharField(max_length=50)
    bezeichnung = models.CharField(max_length=50)
    groesse = models.IntegerField()
    def __str__(self):
        return self.bezeichnung+"/"+self.standort+" - "+str(self.id)


class Gruppe(models.Model):
    name = models.CharField(max_length=50)
    aktiv = models.BooleanField(default=True)
    raum = models.ForeignKey(Raum, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name+ "("+str(self.id)+")"
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Gruppen"



class Teilnehmer(models.Model):
    name = models.CharField(max_length=50)
    vorname = models.CharField(max_length=50)
    ausbildung = models.ForeignKey(Ausbildung, on_delete=models.CASCADE)
    gruppe = models.ForeignKey(Gruppe, on_delete=models.CASCADE, null=True)
    aktiv = models.BooleanField(default=True)
    email = models.CharField(max_length=255, blank=True)
    mobil = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.name+", "+self.vorname+" - "+self.ausbildung.slug+" / "+str(self.gruppe)
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Teilnehmer"

class TnInfo(models.Model):
    tn = models.ForeignKey(Teilnehmer, on_delete=models.CASCADE)
    zeitpunkt = models.DateTimeField(auto_now=False, auto_now_add=True)
    info = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    aktiv = models.BooleanField(default=True)
    def __str__(self):
        return str(self.user.username)+", "+str(self.zeitpunkt)+", "+self.info
    class Meta:
        verbose_name_plural = "Teilnehmer Infos"


class KanbanBereiche(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=10, unique=True)
    beschreibung = models.TextField()
    aktiv = models.BooleanField(default=True)
    def __str__(self):
        return self.name + "/" + self.slug
    class Meta:
        verbose_name_plural = "Kanban Bereiche"

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
    class Meta:
        verbose_name_plural = "Kanban Projekte"

class KanbanProtokoll(models.Model):
    kommentar = models.TextField()
    stufeNeu = models.IntegerField()
    zeitpunkt = models.TimeField(auto_now=False, auto_now_add=True)
    project = models.ForeignKey(KanbanProject, on_delete=models.CASCADE)
    def __str__(self):
        return self.project.name + " ("+self.stufeNeu+") "+str(self.zeitpunkt)+" - "+self.kommentar
    class Meta:
        verbose_name_plural = "Kanban Protokolle"

class Projekt(models.Model):
    bezeichnung = models.CharField(max_length=100)
    fach = models.ForeignKey(Fach,  on_delete=models.CASCADE)
    gruppe = models.ForeignKey(Gruppe, on_delete=models.CASCADE)
    start = models.DateTimeField(auto_now=False, auto_now_add=True)
    bis = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username+", "+self.fach.slug+", "+self.gruppe.name+", "+str(self.start)+", "+self.bezeichnung
    class Meta:
        verbose_name_plural = "Projekte"

class ProjekteTN(models.Model):
    teilnehmer = models.ForeignKey(Teilnehmer, on_delete=models.CASCADE)
    projekt = models.ForeignKey(Projekt, on_delete=models.CASCADE)
    bis = models.DateTimeField(auto_now=False, auto_now_add=False)
    abgabe = models.DateTimeField(auto_now=False, auto_now_add=True)
    bewertung = models.IntegerField(default=0)
    kommentar = models.CharField(max_length=100, default="")
    offen = models.BooleanField(default=True)
    def laenger(self):
        return self.bis-timezone.now()
    def __str__(self):
        return self.teilnehmer.name+", "+self.projekt.bezeichnung
    class Meta:
        verbose_name_plural = "Projekte Teilnehmer"

class Mitarbeit_thema(models.Model):
    gruppe = models.ForeignKey(Gruppe, on_delete=models.CASCADE)
    start = models.DateTimeField(auto_now=True, auto_now_add=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thema = models.CharField(max_length=255, default="")

    def __str__(self):
        return self.gruppe.name + ", "+ self.thema

class Mitarbeit(models.Model):
    tn = models.ForeignKey(Teilnehmer, on_delete=models.CASCADE)
    thema = models.ForeignKey(Mitarbeit_thema, on_delete=models.CASCADE)
    zeit = models.DateTimeField(auto_now=True, auto_now_add=False)
    tn_inaktiv = models.BooleanField(default=False)
    tn_abwesend = models.BooleanField(default=False)
    tn_ok = models.BooleanField(default=False)
    kommentar = models.CharField(max_length=255, default="")
    def __str__(self):
        return self.tn.name + ", "+ str(self.zeit)

class Essenanmeldung(models.Model):
    gruppe = models.ForeignKey(Gruppe, on_delete=models.CASCADE)
    datum = models.DateField(auto_now=False, auto_now_add=False)
    gemeldet = models.DateTimeField(auto_now=False, auto_now_add=True)
    anzahl_tn = models.IntegerField()
    anzahl_essen = models.IntegerField()
    gemeldet_durch = models.ForeignKey(User, on_delete=models.CASCADE)

class PlanFarbe(models.Model):
    farbe = models.CharField(max_length=50)
    def __str__(self):
        return self.farbe+" - "+str(self.id)

class PlanZeiten(models.Model):
    einheit = models.IntegerField(unique=True)
    von = models.CharField(max_length=10)
    bis = models.CharField(max_length=10)
    def __str__(self):
        return str(self.einheit)+"-"+self.von+":"+self.bis+" - "+str(self.id)

class Ausbilder(models.Model):
    aktiv = models.BooleanField(default=True)
    anrede = models.CharField(max_length=50)
    vorname = models.CharField(max_length=50)
    nachname = models.CharField(max_length=50)
    kuerzel = models.CharField(max_length=4)
    def __str__(self):
            return self.nachname+"; "+self.vorname+" ("+self.kuerzel+") "+str(self.id)

class Plan(models.Model):
    gruppe = models.ForeignKey(Gruppe, on_delete=models.CASCADE)
    jahr = models.IntegerField()
    kw = models.IntegerField()
    tag = models.IntegerField()
    einheit = models.ForeignKey(PlanZeiten, on_delete=models.CASCADE)
    fach = models.CharField( max_length=50)
    ausbilder = models.ForeignKey(Ausbilder, on_delete=models.CASCADE)
    raum = models.ForeignKey(Raum, on_delete=models.CASCADE)
    farbe = models.ForeignKey(PlanFarbe, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.gruppe)+"/"+str(self.jahr)+"/"+str(self.kw)+"/"+str(self.tag)+"/"+str(self.einheit)+"/"+self.fach+"/"+str(self.ausbilder)+" - "+str(self.id)

class Anwesenheit(models.Model):
    teilnehmer = models.ForeignKey(Teilnehmer, on_delete=models.CASCADE)
    datum = models.DateTimeField(auto_now=False, auto_now_add=True)
    anwesend = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.teilnehmer)+", "+str(self.datum)+", "+str(self.anwesend)

