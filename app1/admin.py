from django.contrib import admin

from .models import *

admin.site.register(Ausbildung)
admin.site.register(Fach)
admin.site.register(Teilnehmer)
admin.site.register(Gruppe)
admin.site.register(KanbanProject)
admin.site.register(KanbanBereiche)
admin.site.register(TnInfo)
admin.site.register(Projekt)
admin.site.register(ProjekteTN)
admin.site.register(Mitarbeit)
admin.site.register(PlanFarbe)
admin.site.register(PlanZeiten)
admin.site.register(Ausbilder)
admin.site.register(Plan)
admin.site.register(Raum)

admin.site.register(Anwesenheit)
