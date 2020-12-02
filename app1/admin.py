from django.contrib import admin

from .models import *

admin.site.register(Ausbildung)
admin.site.register(Fach)
admin.site.register(Teilnehmer)
admin.site.register(Gruppe)
admin.site.register(Project)
admin.site.register(Bewertung)
admin.site.register(KanbanProject)
admin.site.register(KanbanBereiche)
admin.site.register(TnInfo)