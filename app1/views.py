import datetime

from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required
from django.http.response import HttpResponse
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)

from django.contrib import messages
from django.template import loader
from django.utils.timezone import now

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
    btnNew = Btn("Neues Kennwort", "new")
    btnAbmelden = Btn("Abmelden", "logout", color="danger")
    forms = (formZeile(fname, fpassword), formZeile(fpwneu1, fpwneu2),
             "<hr />", BtnSave, BtnCancel, btnNew, btnAbmelden)
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
        forms = (name, slug, BtnSave, BtnCancel, BtnRemove)
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
    forms = (name, slug, BtnSave, BtnCancel)
    return render(request, 'app1/base_form.html', {'forms': forms, 'h1': "Neu erfassen", 'message': message})


@permission_required('app1.view_teilnehmer')
def tnAllg(request):
    gruppe = Gruppe.objects.filter(aktiv=True).order_by("name")
    test = Teilnehmer.objects.filter(aktiv=True).order_by("name")
    return render(request, 'app1/list_tn.html', {'liste': test, 'gruppe': gruppe, 
    'gruppe_id' : -1, })

@permission_required('app1.view_teilnehmer')
def tnAllgGrp(request, grp_id):
    gruppe = Gruppe.objects.filter(aktiv=True,).order_by("name")
    test = Teilnehmer.objects.filter(aktiv=True, gruppe__id=grp_id).order_by("name")
    return render(request, 'app1/list_tn.html', {'liste': test, 'gruppe': gruppe, 
    'gruppe_id' : grp_id, })


@permission_required('app1.view_teilnehmer')
def tnDetail(request, tn_id):
    message = ""
    if request.method == "GET":
        ds = Teilnehmer.objects.get(id=str(tn_id))
        vname = ds.name
        vvorname = ds.vorname
        vausbildung = ds.ausbildung.id
        vemail = ds.email
        vmobil = ds.mobil
        komments = TnInfo.objects.filter(tn=ds, aktiv=True).order_by("-zeitpunkt")
        if ds.gruppe != None:
            vgruppe = ds.gruppe.id
        else:
            vgruppe = 0
    else:
        vname = request.POST['Name']
        vvorname =request.POST['Vorname']
        vausbildung = Ausbildung.objects.get(id=int(request.POST['Ausbildung']))
        vemail = request.POST['Email']
        vmobil = request.POST['Telefon']
        vgruppe = Gruppe.objects.get(id=request.POST['Gruppe'])
        if request.POST['button'] == "cancel":
            return redirect("/pr1/tn")
        if request.POST['button'] == "comment":
            tn = Teilnehmer.objects.get(id=str(tn_id))
            ds = TnInfo(info=request.POST["Kommentar"], tn=tn, user=request.user)
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
            return redirect("/pr1/tn")

    name = FormInput("Name", value=vname)
    vorname = FormInput("Vorname", value=vvorname)
    ausbildung = FormAuswahl("Ausbildung", Ausbildung, value=vausbildung)
    email = FormInput("Email", type="mail", value=vemail)
    gruppe = FormAuswahl("Gruppe", Gruppe, value=vgruppe)
    mobil = FormInput("Telefon", type="tel", value=vmobil, required=False)
    komment = FormInput("Kommentar")
    btnKomm = Btn("Kommentar speichern", "comment")
    forms = (formZeile(name, vorname), formZeile(ausbildung, gruppe), formZeile(email, mobil),
             "<hr />", BtnSave, BtnCancel,"<hr />", komment, "<hr />", btnKomm)

    return render(request, 'app1/form_tnDetail.html', {'forms': forms, 'h1': "Teilnehmerinfo", 'message': message, 
    "komments": komments })

@permission_required('app1.view_teilnehmer')
def tnNeu(request):
    message = ""
    if request.method == "GET":
        vname = vvorname = vausbildung = vemail = vmobil = ""
        if "gruppe" in request.GET:
            sgruppe=int(request.GET["gruppe"])
        else:
            sgruppe=-1
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
            mail_cut=vemail.split("@")
            mail_cut=mail_cut[0].split(".")
            vname = mail_cut[1]
            vvorname = mail_cut[0]
        else:
            iausbildung = Ausbildung.objects.get(id=vausbildung)
            ds = Teilnehmer(name=vname,
                            vorname=vvorname, ausbildung=iausbildung, mobil=vmobil,
                            email=vemail, gruppe=vgruppe)
            ds.save()
            if request.POST['button'] == "save":
                return redirect("/pr1/tn")
            else:
                return redirect("/pr1/tn/neu?gruppe="+str(vgruppe.id))
    name = FormInput("Name", value=vname)
    vorname = FormInput("Vorname", value=vvorname)
    ausbildung = FormAuswahl("Ausbildung", Ausbildung, value=vausbildung)
    email = FormInput("Email", type="mail", value=vemail)
    mobil = FormInput("Telefon", type="tel", value=vmobil, required=False)
    gruppe = FormAuswahl("Gruppe", Gruppe, value=sgruppe)
    btnUeber = Btn("Mail übertragen","mail", formnovalidate=True)
    forms = (formZeile(name, vorname), formZeile(ausbildung, gruppe), formZeile(email, mobil),
             "<hr />", BtnSave, BtnNext, BtnCancel, btnUeber)
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
            if request.POST['button'] == "save":
                return redirect("/pr1/grp")
            else:
                return redirect("/pr1/grp/neu")
    name = FormInput("Name", value=vname)
    forms = (name, 
             "<hr />", BtnSave, BtnNext, BtnCancel)

    return render(request, 'app1/base_form.html', {'forms': forms, 'h1': "Gruppe erfassen", 'message': message})


@permission_required('app1.view_teilnehmer')
def grpDetail(request, grp_id):
    message = ""
    if request.method == "GET":
        ds = Gruppe.objects.get(id=str(grp_id))
        vname = ds.name
    else:
        vname = request.POST['Name']
 
        if request.POST['button'] == "cancel":
            return redirect("/pr1/tn")
        else:
            ds = Gruppe.objects.get(id=str(grp_id))
            if request.POST['button'] == "remove":
                ds.aktiv=False
                ds.save()
                return redirect("/pr1/grp")
            else:
                ds.name = vname
                ds.save()
                return redirect("/pr1/grp")
    name = FormInput("Name", value=vname)
    forms = (name, 
             "<hr />", BtnSave, BtnCancel, BtnRemove)

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
        btnNeu = Btn("Neuer Bereich", "newBer",
                     modal="kanbanZusatzModal", type="button")
        name = FormInput("Name", value=vname)
        prio = FormSlider("Priorität", value=5)
        kommentar = FormInput("Kommentar", value=vkommentar)
        forms = (formZeile(name, auswahlBereich), formZeile(kommentar, prio),
                 '<hr />', BtnSave, BtnCancel, btnNeu,)
        return render(request, 'app1/base_form.html', {'forms': forms, 'h1': "Projekt erstellen", 'message': message, 'modals': ("modalKanbanZusatz.html",)})
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
                               zeitpunkt=now(), bereich=vbereich)
            ds.save()
            return redirect("/pr1/kanban")


@permission_required('app1.view_teilnehmer')
def kanbanEdt(request, id):
    message = ""
    if request.method == "GET":
        ds = KanbanProject.objects.get(id=id, user=request.user)
        name = FormInput("Name", value=ds.name)
        kommentar = FormInput("Kommentar", value=ds.beschreibung)
        auswahlBereich = FormAuswahl('Bereich', KanbanBereiche, value=ds.bereich)
        prio = FormSlider("Priorität", value=ds.prio)        
        forms = (formZeile(name,auswahlBereich), formZeile(kommentar, prio), '<hr />', BtnSave, BtnCancel, BtnRemove)
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
        liste1 = KanbanProject.objects.filter(stufe=1, aktiv=True, bereich__slug="PCK").order_by('-prio')
        liste2 = KanbanProject.objects.filter(stufe=2, aktiv=True, bereich__slug="PCK").order_by('-prio')
        liste3 = KanbanProject.objects.filter(stufe=3, aktiv=True, bereich__slug="PCK").order_by('-prio')
        return render(request, 'app1/list_kanbanPck.html', {'liste1': liste1, 'liste2': liste2, 'liste3': liste3, })
@permission_required('app1.view_teilnehmer')
def kanbanAll(request):
    bereich = ""
    if request.method == "GET" and 'bereich' in request.GET:
        bereich = request.GET['bereich']
    listebereich = KanbanBereiche.objects.exclude(slug__startswith="PRIVAT")
    if bereich != "":
        liste1 = KanbanProject.objects.filter(stufe=1, aktiv=True, bereich__slug=bereich).exclude(bereich__slug__startswith='PRIVAT').order_by('-prio')
        liste2 = KanbanProject.objects.filter(stufe=2, aktiv=True, bereich__slug=bereich).exclude(bereich__slug__startswith='PRIVAT').order_by('-prio')
        liste3 = KanbanProject.objects.filter(stufe=3, aktiv=True, bereich__slug=bereich).exclude(bereich__slug__startswith='PRIVAT').order_by('-prio')
    else:
        liste1 = KanbanProject.objects.filter(stufe=1, aktiv=True).exclude(bereich__slug__startswith='PRIVAT').order_by('-prio')
        liste2 = KanbanProject.objects.filter(stufe=2, aktiv=True).exclude(bereich__slug__startswith='PRIVAT').order_by('-prio')
        liste3 = KanbanProject.objects.filter(stufe=3, aktiv=True).exclude(bereich__slug__startswith='PRIVAT').order_by('-prio')
    return render(request, 'app1/list_kanbanAll.html', {'liste1': liste1, 'liste2': liste2, 'liste3': liste3, 
    'listebereich': listebereich, 'bereich' : bereich, })

@permission_required('app1.view_teilnehmer')
def kanbanOnNeu(request):
    message = ""
    if request.method == 'GET':
        name = request.GET['bezeichnung'].strip()
        fehlerfrei=True
        if name == "":
            messages.warning(request, 'Name darf nicht leer sein.')
            fehlerfrei=False

        slug = request.GET['slug'].strip().upper()
        if slug == "":
            messages.warning(request, "Slug darf nicht leer sein! ")
            fehlerfrei=False
        else:
            test = KanbanBereiche.objects.filter(slug=slug)
            if len(test) > 0:
                messages.warning(request, "SLUG schon vorhanden. ")
                fehlerfrei=False
        kommentar = request.GET['kommentar'].strip()
        if kommentar == "":
            messages.warning(request, "Kommentar darf nicht leer sein! ")
            fehlerfrei=False
        fname = request.GET['name'].strip()
        beschreibung = request.GET['beschreibung'].strip()
        if fehlerfrei:
            ds = KanbanBereiche(name=name, slug=slug, beschreibung=kommentar)
            ds.save()
        return redirect("/pr1/kanban/neu?name="+fname+"&beschreibung="+beschreibung)
