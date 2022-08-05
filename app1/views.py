from datetime import datetime, timedelta, date, time
from genericpath import exists

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)

from django.contrib import messages
from django.utils import timezone
from .forms import UploadFileForm

from .classForm import *

from .models import *


@permission_required('app1.view_teilnehmer')
def startAllg(request):
    print(request.user.id)
    return render(request, 'app1/list_start.html')


def auslogen(request):
    logout(request)
    return redirect("/pr1/")


def auth(request):
    message = ""
    ziel = request.GET["next"]
    if request.method != "POST":
        name = ""
    else:
        if request.POST['button'] == "save":
            name = request.POST['Benutzer']
            password = request.POST['Kennwort']
            user = authenticate(request, username=name, password=password)
            if user is not None:
                login(request, user)
                return redirect(ziel)
            # Redirect to a success page.
            else:
                # Return an 'invalid login' error message.
                message = "Eingabe inkorrekt"
    fname = FormInput("Benutzer", value=name)
    fpassword = FormInput("Kennwort", type='password')
    fpwneu1 = FormInput("Kennwort neu", type='password', required=False)
    fpwneu2 = FormInput("Kennwort bestätigen", type='password', required=False)
    btnNew = FormBtn("Neues Kennwort", "new")
    btnAbmelden = FormBtn("Abmelden", "logout", color="danger")
    forms = (formZeile(fname, fpassword), formZeile(fpwneu1, fpwneu2),
             "<hr />", FormBtnSave, FormBtnCancel, btnNew, btnAbmelden)
    return render(request, 'app1/base_form.html', {'forms': forms, 'h1': "Benutzerdaten eingeben", 'message': message})


def impress(request):
    return render(request, 'app1/impress.html')


@permission_required('app1.view_teilnehmer')
def fachAllg(request):
    test = Fach.objects.filter()
    return render(request, 'app1/list_fach.html', {'liste': test})


@permission_required('app1.view_teilnehmer')
def fachDetail(request, fach_slug):

    if fach_slug != "neu":
        if "bezeichnung" in request.POST:
            if request.POST['button'] == 'abbruch':
                return redirect("/pr1/fach")
            elif request.POST['button'] == 'save':
                fach = get_object_or_404(Fach, slug=fach_slug)
                fach.name = request.POST['bezeichnung']
                fach.save()
                return redirect("/pr1/fach")
            elif request.POST['button'] == 'remove':
                fach = get_object_or_404(Fach, slug=fach_slug)
                fach.delete()
                return redirect("/pr1/fach")
            else:
                return fachAllg(request)
        else:
            test = get_object_or_404(Fach, slug=fach_slug)
            return render(request, 'app1/fachdetailedt.html', {'fach': test})
    else:
        error = ""
        if "bezeichnung" in request.POST:
            if request.POST['button'] == 'abbruch':
                return redirect("/pr1/fach")

            bezeichnung = request.POST['bezeichnung']
            slug = request.POST['slug'].upper()
            test = Fach.objects.filter(slug=slug)
            if len(test) > 0:
                error += "SLUG schon vorhanden, "
            if error == "":
                temp = Fach(name=bezeichnung, slug=slug)
                temp.save()

                test = get_list_or_404(Fach)
                return render(request, 'app1/fach.html', {'liste': test})
        else:
            bezeichnung = ""
            slug = ""
        return render(request, 'app1/fachdetailnew.html',
                      {'error': error,
                       'slug': slug,
                       'bezeichnung': bezeichnung})


@permission_required('app1.view_teilnehmer')
def ausbAllg(request):
    test = Ausbildung.objects.filter()
    return render(request, 'app1/list_ausb.html', {'liste': test})


@permission_required('app1.view_teilnehmer')
def ausbDetail(request, ausb_slug):
    if ausb_slug == "neu":
        antwort = ausbNeu(request)
        return antwort
    if request.method == 'GET':
        satz = Ausbildung.objects.get(slug=ausb_slug, aktiv=True)
        name = FormInput("Bezeichnung", value=satz.name)
        slug = FormInput('Slug', value=satz.slug)
        slug.readonly = True
        forms = (name, slug, FormBtnSave, FormBtnCancel, FormBtnRemove)
    else:
        if request.POST['button'] == 'cancel':
            return redirect("/pr1/ausb")
        elif request.POST['button'] == 'save':
            ausb = get_object_or_404(Ausbildung, slug=ausb_slug)
            ausb.name = request.POST['Bezeichnung']
            ausb.save()
            return redirect("/pr1/ausb")
        elif request.POST['button'] == 'remove':
            fach = get_object_or_404(Ausbildung, slug=ausb_slug)
            fach.delete()
            return redirect("/pr1/ausb")
        else:
            return redirect("/pr1/ausb")

    return render(request, 'app1/base_form.html', {'forms': forms, 'h1': "Beruf", 'message': ""})


@permission_required('app1.view_teilnehmer')
def ausbNeu(request):
    if request.method == "GET":
        name = ""
        slug = ""
        message = ""
    elif request.POST["button"] == "cancel":
        return redirect("/pr1/ausb")
    else:
        name = request.POST["Bezeichnung"]
        slug = request.POST["Slug"].upper()
        test = Ausbildung.objects.filter(slug=slug, aktiv=True)
        if len(test) > 0:
            message = "SLUG schon vorhanden, "
        else:
            temp = Ausbildung(name=name, slug=slug)
            temp.save()
            return redirect("/pr1/ausb")
    name = FormInput("Bezeichnung", value=name)
    slug = FormInput("Slug", value=slug)
    forms = (name, slug, FormBtnSave, FormBtnCancel)
    return render(request, 'app1/base_form.html', {'forms': forms, 'h1': "Neu erfassen", 'message': message})


@permission_required('app1.view_teilnehmer')
def tnAllg(request):
    gruppe = Gruppe.objects.filter(aktiv=True).order_by("name")
    test = Teilnehmer.objects.filter(aktiv=True).order_by("name")
    return render(request, 'app1/list_tn.html', {'liste': test, 'gruppe': gruppe,
                                                 'gruppe_id': -1, })


@permission_required('app1.view_teilnehmer')
def tnAllgGrp(request, grp_id):
    gruppe = Gruppe.objects.filter(aktiv=True,).order_by("name")
    test = Teilnehmer.objects.filter(
        aktiv=True, gruppe__id=grp_id).order_by("name")
    return render(request, 'app1/list_tn.html', {'liste': test, 'gruppe': gruppe,
                                                 'gruppe_id': grp_id, })


@permission_required('app1.view_teilnehmer')
def tnDetail(request, tn_id):
    message = ""
    tn_ds = Teilnehmer.objects.get(id=str(tn_id))
    anwesend_liste = Anwesenheit.objects.filter(
        teilnehmer=tn_ds).order_by('datum')
    komments = TnInfo.objects.filter(
        tn=tn_ds, aktiv=True).order_by("-zeitpunkt")
    if request.method == "GET":
        if len(anwesend_liste)>0:
            von = anwesend_liste[0].datum.date()
            bis = anwesend_liste[len(anwesend_liste)-1].datum.date()
        else:
            von = bis = date.today().strftime("%Y-%m-%d")
        vname = tn_ds.name
        vvorname = tn_ds.vorname
        vausbildung = tn_ds.ausbildung.id
        vemail = tn_ds.email
        vmobil = tn_ds.mobil
        projekte = ProjekteTN.objects.filter(
            teilnehmer=tn_ds, offen=True).order_by("bis")
        if tn_ds.gruppe != None:
            vgruppe = tn_ds.gruppe.id
        else:
            vgruppe = -1
    else:
        von = request.POST['Von']
        bis = request.POST['Bis']
        bis = datetime.strptime(bis, '%Y-%m-%d')
        vname = request.POST['Name']
        vvorname = request.POST['Vorname']
        vausbildung = Ausbildung.objects.get(
            id=int(request.POST['Ausbildung']))
        vemail = request.POST['Email']
        vmobil = request.POST['Telefon']
        vgruppe = Gruppe.objects.get(id=request.POST['Gruppe'])
        if 'button' in request:
            if request.POST['button'] == "cancel":
                return redirect("/pr1/tn")
            if request.POST['button'] == "comment":
                tn = Teilnehmer.objects.get(id=str(tn_id))
                ds = TnInfo(
                    info=request.POST["Kommentar"], tn=tn, user=request.user)
                ds.save()
                return redirect("/pr1/tn")
            elif request.POST['button'] == "delete":
                ds = Teilnehmer.objects.get(id=str(tn_id))
                ds.aktiv = False
                ds.save()
                return redirect("/pr1/tn")
            else:
                ds = Teilnehmer.objects.get(id=str(tn_id))
                ds.name = vname
                ds.vorname = vvorname
                ds.ausbildung = vausbildung
                ds.mobil = vmobil
                ds.email = vemail
                ds.gruppe = vgruppe
                ds.save()
                # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                return redirect("/pr1/tn")

    name = FormInput("Name", value=vname)
    vorname = FormInput("Vorname", value=vvorname)
    ausbildung = FormAuswahl("Ausbildung", Ausbildung, value=vausbildung)
    email = FormInput("Email", type="mail", value=vemail, required=False)
    gruppe = FormAuswahl("Gruppe", Gruppe, value=vgruppe)
    mobil = FormInput("Telefon", type="tel", value=vmobil, required=False)
    komment = FormInput("Kommentar", required=False)
    btnKomm = FormBtn("Kommentar speichern", "comment")
    btn_del = FormBtn("Teilnehmer löschen", "delete", color="danger")
    f_von = FormInput("Von", value=str(von), type="date", submit=True)
    f_bis = FormInput("Bis", value=str(bis.strftime("%Y-%m-%d")), type="date", submit=True)
    # Bis eins hochzählen
    bis  = bis + timedelta(days=1)
    anwesend_liste = anwesend_liste.exclude(datum__lt=von)
    anwesend_liste = anwesend_liste.exclude(datum__gt=bis)
    liste_anw = []
    liste2 = []
    if len(anwesend_liste)>0:
        lfd_datum_alt = anwesend_liste[0].datum.strftime("%d.%m.%Y")
        for ds_akt in anwesend_liste:
            lfd_datum = ds_akt.datum.strftime("%d.%m.%Y")
            if lfd_datum != lfd_datum_alt:
                print("neue Zeile", ds_akt.datum.date())
                # Neue Zeile
                liste_anw.append((lfd_datum_alt, liste2))
                liste2 = []
                lfd_datum_alt = lfd_datum
            liste2.append((ds_akt.datum.time(), ds_akt.anwesend, ds_akt.user))
        liste_anw.append((lfd_datum_alt, liste2))
    forms = (formZeile(name, vorname), formZeile(ausbildung, gruppe), formZeile(email, mobil),
             "<hr />", FormBtnSave, FormBtnCancel, btn_del, formLinie, komment, formLinie, btnKomm, formZeile(f_von, f_bis))

    return render(request, 'app1/form_tnDetail.html', {'forms': forms, 'h1': "Teilnehmerinfo", 'message': message,
                                                       "komments": komments, 'liste2': liste_anw})


@permission_required('app1.view_teilnehmer')
def tnNeu(request):
    message = ""
    if request.method == "GET":
        vname = vvorname = vausbildung = vemail = vmobil = ""
        if "gruppe" in request.GET:
            sgruppe = int(request.GET["gruppe"])
        else:
            sgruppe = -1
        if "ausbildung" in request.GET:
            vausbildung = int(request.GET["ausbildung"])
        else:
            vausbildung = -1
    else:
        vname = request.POST['Name']
        vvorname = request.POST['Vorname']
        vausbildung = int(request.POST['Ausbildung'])
        vemail = request.POST['Email']
        vmobil = request.POST['Telefon']
        sgruppe = request.POST['Gruppe']
        vgruppe = Gruppe.objects.get(id=sgruppe)
        if request.POST['button'] == "cancel":
            return redirect("/pr1/tn")
        elif request.POST['button'] == 'mail':
            mail_cut = vemail.split("@")
            mail_cut = mail_cut[0].split(".")
            vname = mail_cut[1].capitalize()
            vvorname = mail_cut[0].capitalize()
        else:
            iausbildung = Ausbildung.objects.get(id=vausbildung)
            ds = Teilnehmer(name=vname,
                            vorname=vvorname, ausbildung=iausbildung, mobil=vmobil,
                            email=vemail, gruppe=vgruppe)
            ds.save()
            if request.POST['button'] == "save":
                return redirect("/pr1/tn")
            else:
                return redirect("/pr1/tn/neu?gruppe="+str(vgruppe.id)+"&ausbildung="+str(vausbildung))
    name = FormInput("Name", value=vname)
    vorname = FormInput("Vorname", value=vvorname)
    print(vausbildung)
    ausbildung = FormAuswahl("Ausbildung", Ausbildung, value=vausbildung)
    email = FormInput("Email", type="mail", value=vemail, required=False)
    mobil = FormInput("Telefon", type="tel", value=vmobil, required=False)
    print(sgruppe)
    gruppe = FormAuswahl("Gruppe", Gruppe, value=sgruppe)
    btnUeber = FormBtn("Mail übertragen", "mail", formnovalidate=True)
    forms = (formZeile(name, vorname), formZeile(ausbildung, gruppe), formZeile(email, mobil),
             "<hr />", FormBtnSave, FormBtnNext, FormBtnCancel, btnUeber)
    return render(request, 'app1/base_form.html', {'forms': forms, 'h1': "Teilnehmer erfassen", 'message': message})


@permission_required('app1.view_teilnehmer')
def grpAllg(request):
    liste = Gruppe.objects.filter(aktiv=True).order_by("name")
    return render(request, 'app1/list_grp.html', {'liste': liste})


@permission_required('app1.view_teilnehmer')
def grpNeu(request):
    message = ""
    if request.method == "GET":
        vname = ""
    else:
        print(request.POST)
        vname = request.POST['Name']

        if request.POST['button'] == "cancel":
            return redirect("/pr1/tn")
        else:
            ds = Gruppe(name=vname)
            ds.save()
            if request.POST["button"] == "import":
                form = UploadFileForm(request.POST, request.FILES)
                if form.is_valid():
                    # handle_uploaded_file(request.FILES['file'])
                    return HttpResponseRedirect('/success/url/')
            if request.POST['button'] == "save":
                return redirect("/pr1/grp")
            else:
                return redirect("/pr1/grp/neu")
    name = FormInput("Name", value=vname)
    btn_import = FormBtn("Import", "import")
    forms = (name,
             "<hr />", FormBtnSave, FormBtnNext, FormBtnCancel, btn_import)

    return render(request, 'app1/base_form.html', {'forms': forms, 'h1': "Gruppe erfassen", 'message': message})


@permission_required('app1.view_teilnehmer')
def grpDetail(request, grp_id):
    message = ""
    if request.method == "GET":
        ds = Gruppe.objects.get(id=str(grp_id))
        vname = ds.name
    else:
        print(request.POST)
        vname = request.POST['Name']

        if request.POST['button'] == "cancel":
            return redirect("/pr1/tn")
        else:
            ds = Gruppe.objects.get(id=str(grp_id))
            if request.POST['button'] == "remove":
                ds.aktiv = False
                ds.save()
                return redirect("/pr1/grp")
            else:
                ds.name = vname
                ds.save()
                return redirect("/pr1/grp")
    name = FormInput("Name", value=vname)
    area = '<textarea cols="50" rows="10" name="textar">Es war dunkel, feucht und neblig …</textarea>'
    forms = (name,
             "<hr />", FormBtnSave, FormBtnCancel, FormBtnRemove, formLinie, area)

    return render(request, 'app1/base_form.html', {'forms': forms, 'h1': "Gruppe bearbeiten", 'message': message})


@permission_required('app1.view_teilnehmer')
def kanbanAllg(request):
    liste1 = KanbanProject.objects.filter(
        stufe=1, aktiv=True, user=request.user).order_by('-prio')
    liste2 = KanbanProject.objects.filter(
        stufe=2, aktiv=True, user=request.user).order_by('-prio')
    liste3 = KanbanProject.objects.filter(
        stufe=3, aktiv=True, user=request.user).order_by('-prio')
    return render(request, 'app1/list_kanban.html', {'liste1': liste1, 'liste2': liste2, 'liste3': liste3, })


@permission_required('app1.view_teilnehmer')
def kanbanNeu(request):
    message = ""
    if request.method == "GET":
        if 'msg' in request.GET:
            vname = request.GET['name']
            vkommentar = request.GET['beschreibung']
        else:
            vname = ""
            vkommentar = ""
        auswahlBereich = FormAuswahl('Bereich', KanbanBereiche)
        btnNeu = FormBtn("Neuer Bereich", "newBer",
                         modal="kanbanZusatzModal", type="button")
        name = FormInput("Name", value=vname)
        prio = FormSlider("Priorität", value=5)
        kommentar = FormInput("Kommentar", value=vkommentar, required=False)
        forms = (formZeile(name, auswahlBereich), formZeile(kommentar, prio),
                 '<hr />', FormBtnSave, FormBtnCancel, btnNeu,)
        return render(request, 'app1/base_form.html', {'forms': forms, 'h1': "Projekt erstellen", 'message': message, 'modals': ("modalKanbanZusatz.html",), "js": ("js/eigenes.js", )})
    else:
        if request.POST['button'] == 'cancel':
            return redirect("/pr1/kanban")
        else:
            vname = request.POST['Name']
            vkommentar = request.POST['Kommentar']
            vbereich = request.POST['Bereich']
            vbereich = KanbanBereiche.objects.get(id=vbereich)
            vprio = int(request.POST['Priorität'])
            ds = KanbanProject(name=vname, beschreibung=vkommentar,
                               user=request.user, prio=vprio,
                               zeitpunkt=timezone.now(), bereich=vbereich)
            ds.save()
            return redirect("/pr1/kanban")


@permission_required('app1.view_teilnehmer')
def kanbanEdt(request, id):
    message = ""
    if request.method == "GET":
        ds = KanbanProject.objects.get(id=id, user=request.user)
        name = FormInput("Name", value=ds.name)
        kommentar = FormInput(
            "Kommentar", value=ds.beschreibung, required=False)
        auswahlBereich = FormAuswahl('Bereich', KanbanBereiche, value=ds.id)
        prio = FormSlider("Priorität", value=ds.prio)
        forms = (formZeile(name, auswahlBereich), formZeile(
            kommentar, prio), '<hr />', FormBtnSave, FormBtnCancel, FormBtnRemove)
        return render(request, 'app1/base_form.html', {'forms': forms, 'h1': "Projekt ändern", 'message': message})
    else:
        ds = KanbanProject.objects.get(id=id, user=request.user)
        if request.POST['button'] == 'cancel':
            return redirect("/pr1/kanban")
        elif request.POST['button'] == 'save':
            vname = request.POST['Name']
            vkommentar = request.POST['Kommentar']
            vbereich = request.POST['Bereich']
            vbereich = KanbanBereiche.objects.get(id=vbereich)
            vprio = request.POST['Priorität']
            ds.name = vname
            ds.beschreibung = vkommentar
            ds.bereich = vbereich
            ds.prio = vprio
            ds.save()
            return redirect("/pr1/kanban")
        elif request.POST['button'] == 'remove':
            ds.delete()
            return redirect("/pr1/kanban")


@permission_required('app1.view_teilnehmer')
def kanbanStufe(request, id, stufe):
    ds = KanbanProject.objects.get(id=id)
    ds.stufe = stufe
    ds.save()
    return redirect("/pr1/kanban")


def kanbanPck(request):
    liste1 = KanbanProject.objects.filter(
        stufe=1, aktiv=True, bereich__slug="PCK").order_by('-prio')
    liste2 = KanbanProject.objects.filter(
        stufe=2, aktiv=True, bereich__slug="PCK").order_by('-prio')
    liste3 = KanbanProject.objects.filter(
        stufe=3, aktiv=True, bereich__slug="PCK").order_by('-prio')
    return render(request, 'app1/list_kanbanPck.html', {'liste1': liste1, 'liste2': liste2, 'liste3': liste3, })


@permission_required('app1.view_teilnehmer')
def kanbanAll(request):
    bereich = ""
    if request.method == "GET" and 'bereich' in request.GET:
        bereich = request.GET['bereich']
    listebereich = KanbanBereiche.objects.exclude(slug__startswith="PRIVAT")
    if bereich != "":
        liste1 = KanbanProject.objects.filter(stufe=1, aktiv=True, bereich__slug=bereich).exclude(
            bereich__slug__startswith='PRIVAT').order_by('-prio')
        liste2 = KanbanProject.objects.filter(stufe=2, aktiv=True, bereich__slug=bereich).exclude(
            bereich__slug__startswith='PRIVAT').order_by('-prio')
        liste3 = KanbanProject.objects.filter(stufe=3, aktiv=True, bereich__slug=bereich).exclude(
            bereich__slug__startswith='PRIVAT').order_by('-prio')
    else:
        liste1 = KanbanProject.objects.filter(stufe=1, aktiv=True).exclude(
            bereich__slug__startswith='PRIVAT').order_by('-prio')
        liste2 = KanbanProject.objects.filter(stufe=2, aktiv=True).exclude(
            bereich__slug__startswith='PRIVAT').order_by('-prio')
        liste3 = KanbanProject.objects.filter(stufe=3, aktiv=True).exclude(
            bereich__slug__startswith='PRIVAT').order_by('-prio')
    return render(request, 'app1/list_kanbanAll.html', {'liste1': liste1, 'liste2': liste2, 'liste3': liste3,
                                                        'listebereich': listebereich, 'bereich': bereich, })


@permission_required('app1.view_teilnehmer')
def kanbanOnNeu(request):
    message = ""
    if request.method == 'GET':
        name = request.GET['bezeichnung'].strip()
        fehlerfrei = True
        if name == "":
            messages.warning(request, 'Name darf nicht leer sein.')
            fehlerfrei = False

        slug = request.GET['slug'].strip().upper()
        if slug == "":
            messages.warning(request, "Slug darf nicht leer sein! ")
            fehlerfrei = False
        else:
            test = KanbanBereiche.objects.filter(slug=slug)
            if len(test) > 0:
                messages.warning(request, "SLUG schon vorhanden. ")
                fehlerfrei = False
        kommentar = request.GET['kommentar'].strip()
        if kommentar == "":
            messages.warning(request, "Kommentar darf nicht leer sein! ")
            fehlerfrei = False
        fname = request.GET['name'].strip()
        beschreibung = request.GET['beschreibung'].strip()
        if fehlerfrei:
            ds = KanbanBereiche(name=name, slug=slug, beschreibung=kommentar)
            ds.save()
        return redirect("/pr1/kanban/neu?name="+fname+"&beschreibung="+beschreibung)


def getTimeDiff(eingabe):
    timeListe = eingabe.strip().split()
    stunden = minuten = tage = wochen = 0
    for i in range(1, len(timeListe), 2):
        if timeListe[i].upper() == "MINUTEN":
            minuten = int(timeListe[i-1])
        elif timeListe[i].upper() == "MINUTE":
            minuten = int(timeListe[i-1])
        elif timeListe[i].upper() == "M":
            minuten = int(timeListe[i-1])
        elif timeListe[i].upper() == "STUNDE":
            stunden = int(timeListe[i-1])
        elif timeListe[i].upper() == "H":
            stunden = int(timeListe[i-1])
        elif timeListe[i].upper() == "STUNDEN":
            stunden = int(timeListe[i-1])
        elif timeListe[i].upper() == "TAGE":
            tage = int(timeListe[i-1])
        elif timeListe[i].upper() == "TAG":
            tage = int(timeListe[i-1])
        elif timeListe[i].upper() == "WOCHE":
            wochen = int(timeListe[i-1])
        elif timeListe[i].upper() == "WOCHEN":
            wochen = int(timeListe[i-1])
    diff = timedelta(minutes=minuten, hours=stunden, days=tage, weeks=wochen)
    return diff


@permission_required('app1.view_teilnehmer')
def projekteNeu(request):
    if request.method == "GET":
        message = ""
        listGruppe = FormAuswahl("Gruppe", Gruppe)
        listFach = FormAuswahl("Fach", Fach)
        bezeichnung = FormInput("Bezeichnung")
        dauer = FormInput("Dauer")
        form = (formZeile(listFach, listGruppe), formLinie, formZeile(
            bezeichnung, dauer), formLinie, FormBtnSave, FormBtnCancel)
        return render(request, 'app1/base_form.html', {'forms': form, 'h1': "Projekte", "message": message})
    else:
        gruppe = Gruppe.objects.get(pk=int(request.POST["Gruppe"]))
        fach = Fach.objects.get(pk=int(request.POST["Fach"]))
        bezeichnung = request.POST["Bezeichnung"]
        dauer = request.POST['Dauer']
        td = getTimeDiff(dauer)
        bis = timezone.now()+td
        ds_projekt = Projekt(gruppe=gruppe, fach=fach,
                             bezeichnung=bezeichnung, user=request.user, bis=bis)
        ds_projekt.save()
        teilnehmerListe = Teilnehmer.objects.filter(gruppe=gruppe, aktiv=True)
        # print(teilnehmerListe)
        for teilnehmer in teilnehmerListe:
            ds_projektTn = ProjekteTN(
                teilnehmer=teilnehmer,
                projekt=ds_projekt,
                bis=bis
            )
            ds_projektTn.save()
        return redirect("/pr1/projekt/"+str(ds_projekt.pk))


@permission_required('app1.view_teilnehmer')
def projekt(request, p_id):
    if request.method == "POST":
        liste_k = list(request.POST.keys())
        liste_v = list(request.POST.values())
        print(liste_v)
        print(liste_k)
        if "Abgabe" in liste_v:
            projekt = liste_k[liste_v.index("Abgabe")]

            ds_projektTN = ProjekteTN.objects.get(pk=int(projekt))
            ds_projektTN.offen = False
            ds_projektTN.kommentar = request.POST["text_"+str(projekt)]
            ds_projektTN.abgabe = timezone.now()
            ds_projektTN.save()
        # print(request.POST.values.index("Abgabe"))
    projekt = Projekt.objects.get(id=int(p_id))
    max = len(ProjekteTN.objects.filter(projekt=projekt))
    fertig = len(ProjekteTN.objects.filter(projekt=projekt, offen=False))
    if max > 0:
        anteil = round(fertig*100/max, 1)
    else:
        anteil = 0
    bis = projekt.bis
    datum = (bis.year, bis.month, bis.day, bis.hour, bis.minute, bis.second)
    tn_liste = ProjekteTN.objects.filter(
        projekt_id=int(p_id)).order_by("-offen", "teilnehmer")
    return render(request, 'app1/projekt_list.html', {'liste': tn_liste, 'projekt': projekt, 'anteil': anteil, "js": ("js/timer.js",), "datum": datum, })


@permission_required('app1.view_teilnehmer')
def projekteAllg(request):
    listeProjekte = Projekt.objects.filter().order_by("-start")
    liste = []
    for projekt in listeProjekte:
        max = len(ProjekteTN.objects.filter(projekt=projekt))
        fertig = len(ProjekteTN.objects.filter(projekt=projekt, offen=False))
        if max > 0:
            anteil = round(fertig*100/max, 1)
        else:
            anteil = 0
        liste.append((projekt, anteil))
    return render(request, 'app1/projekt_allg.html', {"liste": liste, })


@permission_required('app1.view_teilnehmer')
def projekteTNDetail(request, ptn_id):
    ds = ProjekteTN.objects.get(pk=ptn_id)
    if request.method == "GET":
        ds = ProjekteTN.objects.get(pk=ptn_id)
        teilnehmer = FormInput("Teilnehmer", value=str(
            ds.teilnehmer), disabled=True)
        fach = FormInput("Fach", value=ds.projekt.fach.name, disabled=True)
        kommentar = FormInput("Kommentar", value=ds.kommentar)
        bewertung = FormSlider("Bewertung", value=ds.bewertung, min=1, max=6)
        form = (formZeile(teilnehmer, fach), formZeile(
            kommentar, bewertung), formLinie, FormBtnSave, FormBtnCancel)
        return render(request, 'app1/base_form.html', {"h1": "Details Projekt TN", "forms": form, })
    elif request.POST["button"] == "save":
        kommentar = request.POST["Kommentar"]
        bewertung = int(request.POST["Bewertung"])
        ds.kommentar = kommentar
        ds.bewertung = bewertung
        ds.save()
        return redirect("/pr1/projekt/"+str(ds.projekt.id))
    return redirect("/pr1/projekt/"+str(ds.projekt.id))


@permission_required('app1.view_teilnehmer')
def projekteRemove(request, project_id):
    ds = Projekt.objects.get(id=project_id)
    if request.method == "GET":
        question = FormInput(
            "Wirklich?", "Projekt wirklich löschen?", readonly=True)
        name = FormInput("Bezeichnung", value=ds.bezeichnung, readonly=True)
        user = FormInput("User", value=str(ds.user), readonly=True)
        fach = FormInput("Fach", value=str(ds.fach), readonly=True)
        forms = (question, name, formZeile(user, fach),
                 formLinie, FormBtnOk, FormBtnCancel)
        return render(request, 'app1/base_form.html', {"h1": "Projekt löschen", "forms": forms, })
    elif request.POST["button"] == "ok":
        print("Löschen")
        ds.delete()
        return redirect("/pr1/projekte/")
    else:
        return redirect("/pr1/projekte/")


def fuelle_listen_ma(thema, tn_liste):
    liste1 = []  # Offen
    liste2 = []  # Ok
    liste3 = []  # Unaufmerksam
    liste4 = []  # Abwesend

    for tn in tn_liste:
        ds = Mitarbeit.objects.filter(tn=tn).last()
        if ds is not None and ds.tn_abwesend == True:
            liste4.append(tn)
        else:
            ds = Mitarbeit.objects.filter(tn=tn, thema=thema).last()
            if ds is not None and ds.tn_inaktiv == True:
                liste3.append(tn)
            elif ds is not None and ds.tn_ok == True:
                liste2.append(tn)
            else:
                liste1.append(tn)

    return (liste1, liste2, liste3, liste4)


@permission_required('app1.view_teilnehmer')
def mitarbeit(request):
    if request.method == "GET":
        if "id" in request.GET:
            ds = Mitarbeit_thema.objects.get(id=int(request.GET["id"]))
            list_tn = Teilnehmer.objects.filter(gruppe=ds.gruppe)
            listen = fuelle_listen_ma(ds, list_tn)
            return render(request, 'app1/mitarbeit_liste.html', {"inhalt": ds, "listen": listen})
        else:
            name = FormAuswahl("Gruppe", Gruppe)
            thema = FormInput("Thema")
            forms1 = (name, thema, formLinie, FormBtnOk, FormBtnCancel)
            return render(request, 'app1/mitarbeit_start.html', {"forms1": forms1})
    else:
        print(request.POST)
        if "Gruppe" in request.POST:
            id_gr = int(request.POST["Gruppe"])
            thema = request.POST["Thema"]
            gruppe = Gruppe.objects.get(id=id_gr)
            ds = Mitarbeit_thema(gruppe=gruppe, thema=thema,
                                 user=request.user, start=timezone.now())
            ds.save()
            id = str(ds.id)
        else:
            id = request.POST["id"]
            if "ok" in request.POST:
                tn_nr = request.POST["ok"]
                ds_tn = Teilnehmer.objects.get(id=int(tn_nr))
                ds_thema = Mitarbeit_thema.objects.get(id=int(id))
                kommentar = request.POST["text_"+tn_nr]
                ds = Mitarbeit(tn=ds_tn, thema=ds_thema, tn_ok=True,
                               kommentar=kommentar, zeit=timezone.now())
                ds.save()
            elif "unaufmerksam" in request.POST:
                tn_nr = request.POST["unaufmerksam"]
                ds_tn = Teilnehmer.objects.get(id=int(tn_nr))
                ds_thema = Mitarbeit_thema.objects.get(id=int(id))
                kommentar = request.POST["text_"+tn_nr]
                ds = Mitarbeit(tn=ds_tn, thema=ds_thema, tn_inaktiv=True,
                               kommentar=kommentar, zeit=timezone.now())
                ds.save()
            elif "abwesend" in request.POST:
                tn_nr = request.POST["abwesend"]
                ds_tn = Teilnehmer.objects.get(id=int(tn_nr))
                ds_thema = Mitarbeit_thema.objects.get(id=int(id))
                kommentar = request.POST["text_"+tn_nr]
                ds = Mitarbeit(tn=ds_tn, thema=ds_thema, tn_abwesend=True,
                               kommentar=kommentar, zeit=timezone.now())
                ds.save()
            elif "anwesend" in request.POST:
                tn_nr = request.POST["anwesend"]
                ds_tn = Teilnehmer.objects.get(id=int(tn_nr))
                ds_thema = Mitarbeit_thema.objects.get(id=int(id))
                kommentar = request.POST["text_"+tn_nr]
                ds = Mitarbeit(tn=ds_tn, thema=ds_thema,
                               kommentar=kommentar, zeit=timezone.now())
                ds.save()
            elif "nochmal" in request.POST:
                tn_nr = request.POST["nochmal"]
                ds_tn = Teilnehmer.objects.get(id=int(tn_nr))
                ds_thema = Mitarbeit_thema.objects.get(id=int(id))
                kommentar = request.POST["text_"+tn_nr]
                ds = Mitarbeit(tn=ds_tn, thema=ds_thema,
                               kommentar=kommentar, zeit=timezone.now())
                ds.save()
            elif "zurueck" in request.POST:
                tn_nr = request.POST["zurueck"]
                ds_tn = Teilnehmer.objects.get(id=int(tn_nr))
                ds_thema = Mitarbeit_thema.objects.get(id=int(id))
                kommentar = request.POST["text_"+tn_nr]
                ds = Mitarbeit(tn=ds_tn, thema=ds_thema,
                               kommentar=kommentar, zeit=timezone.now())
                ds.save()
            elif "text_neu" in request.POST:
                thema = request.POST["text_neu"]
                ds_thema = Mitarbeit_thema.objects.get(id=int(id))
                ds = Mitarbeit_thema(
                    gruppe=ds_thema.gruppe, thema=thema, user=request.user, start=timezone.now())
                ds.save()
                id = str(ds.id)

        return redirect('/pr1/mitarbeit?id='+id)


@permission_required('app1.view_teilnehmer')
def ma_auswertung(request):
    if request.method == "GET":
        datum = date.today().strftime("%Y-%m-%d")
        gruppe = FormAuswahl("Gruppe", Gruppe)
        return render(request, 'app1/mitarbeit_auswertung.html', {"datum": datum, "gruppe": gruppe})
    else:
        eintraege = []
        gruppe = Gruppe.objects.get(id=int(request.POST["Gruppe"]))
        datum = datetime.strptime(request.POST["datum"], '%Y-%m-%d')
        liste_tn = Teilnehmer.objects.filter(gruppe=gruppe).order_by("name")
        for tn in liste_tn:
            person = []
            liste_tn_ma = Mitarbeit.objects.filter(
                tn=tn, zeit__date=datum).order_by("zeit")
            person.append(tn.name+", "+tn.vorname)
            for eintrag in liste_tn_ma:
                if eintrag.tn_abwesend:
                    person.append("<br />Abwesend ab: " +
                                  eintrag.zeit.strftime('%H:%M:%S'))
                elif eintrag.tn_inaktiv:
                    person.append("<br />Inaktiv ab: " +
                                  eintrag.zeit.strftime('%H:%M:%S'))
                elif not eintrag.tn_ok:
                    person.append("bis: "+eintrag.zeit.strftime('%H:%M:%S'))
            eintraege.append(person)
        datum = date.today().strftime("%Y-%m-%d")
        gruppe = FormAuswahl("Gruppe", Gruppe)
        return render(request, 'app1/mitarbeit_auswertung.html', {"datum": datum, "gruppe": gruppe, "eintraege": eintraege})


def essen_anmeldung(request):
    form_gruppe = FormAuswahl("Gruppe", Gruppe, aktiv=False)
    datum = datetime.now().strftime("%Y-%m-%d")
    form_dat = FormInput("Datum: ", type='date', value=datum)
    form_tn = FormInput("Anwesende :", type='number')
    form_essen = FormInput("evtl.  Essen:", type='number')
    forms = (formZeile(form_gruppe, form_dat), formZeile(
        form_tn, form_essen), formLinie, FormBtnOk, FormBtnCancel)
    return render(request, 'app1/base_form.html', {"h1": "Essen anmelden", "forms": forms, })


def plan_kurz(request, gruppe):
    return render(request, 'app1/base.html')


def plan(request, gruppe, jahr, kw):
    plan = Plan.objects.filter(gruppe=gruppe, jahr=jahr, kw=kw)
    zeiten = PlanZeiten.objects.all()
    print(plan)
    print(zeiten)
    return render(request, 'app1/base.html')


@permission_required('app1.view_teilnehmer')
def anwesenheit(request):
    if request.method == "POST":
        return redirect("/pr1/anwesenheit/"+request.POST["Gruppe"]+"/start")
    gruppe = FormAuswahl("Gruppe", Gruppe, aktiv=True)
    forms = (formZeile(gruppe), formLinie, FormBtnOk)
    return render(request, 'app1/base_form.html', {"h1": "Anwesenheit Gruppe auswählen", "forms": forms, })


@permission_required('app1.view_teilnehmer')
def anwesenheit_start(request, gruppe):
    if request.method == "POST":
        gruppe = Gruppe.objects.get(id=request.POST["gruppe"])
        teilnehmer = Teilnehmer.objects.filter(aktiv=True, gruppe=gruppe)
        for tn in teilnehmer:
            anwesend = "cbox_"+str(tn.id) in request.POST
            anwesenheit = Anwesenheit(
                teilnehmer=tn, user=request.user, anwesend=anwesend)
            anwesenheit.save()
        return redirect("/pr1/anwesenheit/"+str(gruppe.id))
    else:
        gruppe = Gruppe.objects.get(id=gruppe)
        teilnehmer = Teilnehmer.objects.filter(aktiv=True, gruppe=gruppe)
        return render(request, 'app1/anwesenheit_start.html', {"gruppe": gruppe, "teilnehmer": teilnehmer})


@permission_required('app1.view_teilnehmer')
def anwesenheit_laufend(request, gruppe):
    gruppe_ds = Gruppe.objects.get(id=gruppe)
    if request.method == "POST":
        if "button" not in request.POST:
            gruppe = request.POST["Gruppe"]
            return redirect("/pr1/anwesenheit/"+str(gruppe))
        if request.POST["button"] == "weiter":
            return redirect("/pr1/anwesenheit/auswertung/"+str(gruppe))
        else:
            tn = request.POST["button"]
            # print(tn)
            tn = Teilnehmer.objects.get(id=tn)
            satz = Anwesenheit.objects.filter(teilnehmer=tn).last()
            anwesend = not satz.anwesend
            anwesenheit = Anwesenheit(
                teilnehmer=tn, user=request.user, anwesend=anwesend)
            anwesenheit.save()
            return redirect("/pr1/anwesenheit/"+str(gruppe))
    else:
        liste = []
        teilnehmer = Teilnehmer.objects.filter(aktiv=True, gruppe=gruppe)
        gruppe_fm = FormAuswahl("Gruppe", Gruppe, gruppe,
                                submit=True, label=False)
        form = (gruppe_fm)
        time_old = False
        for tn in teilnehmer:
            satz = Anwesenheit.objects.filter(teilnehmer=tn).last()
            if satz:
                anwesend = satz.anwesend
                liste.append((tn, anwesend))
        return render(request, 'app1/anwesenheit.html', {"gruppe": gruppe, "teilnehmer": liste, "form": form})


@permission_required('app1.view_teilnehmer')
def anwesenheit_auswertung_gruppe(request, gruppe):
    date_akt = date.today()
    max_lenght = 15
    if request.method == "POST":
        date_akt = datetime.strptime(request.POST["Datum"], '%Y-%m-%d').date()
        gruppe = request.POST["Gruppe"]
        max_lenght = int(request.POST["Minimum"])
    print(max_lenght)
    gruppe_ds = Gruppe.objects.get(id=gruppe)
    gruppe_frm = FormAuswahl("Gruppe", Gruppe, gruppe, submit=True)
    datum_frm = FormInput("Datum", type="date",
                          value=str(date_akt), submit=True)
    max_lenght_fm = FormInput("Minimum", value=str(
        max_lenght), type="number", submit=True)
    forms = (formZeile(gruppe_frm, datum_frm,
             max_lenght_fm), formLinie, FormBtnOk)
    teilnehmer = Teilnehmer.objects.filter(aktiv=True, gruppe=gruppe)
    liste = []
    for tn in teilnehmer:
        anwesenheit = Anwesenheit.objects.filter(
            teilnehmer=tn, datum__date=date_akt)
        liste2 = []
        time_old = False
        for anwesend in anwesenheit:
            if not time_old:
                time_old = anwesend.datum
            else:
                time_diff = (anwesend.datum - time_old).total_seconds() / 60
                time_old = anwesend.datum
                # print(anwesend.anwesend, liste2[-1][1])
                if anwesend.anwesend and not liste2[-1][1] and time_diff <= max_lenght:
                    print("gelöscht zu kurz")
                    del liste2[-1]
                elif (anwesend.anwesend == liste2[-1][1]):
                    print("ignoriert doppelt")
                    continue
            if anwesend.anwesend:
                status = "Anwesend"
            else:
                status = "Abwesend"
            liste2.append((anwesend.datum.strftime("%H:%M"),
                          anwesend.anwesend, anwesend.user))
        liste.append((tn, liste2))
    return render(request, 'app1/ausbildung_auswertung.html', {"h1": "Auswertung Anwesenheit", "forms": forms,
                                                               "liste": liste, "datum": date_akt, "gruppe": gruppe_ds})
