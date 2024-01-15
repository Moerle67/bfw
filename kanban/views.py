from django.shortcuts import render

# Create your views here.
def kanban(request):
    return render(request, 'kanban/start.html')

def tgbuttons(request):
    if request.POST["tg_btn"]=="tg_project":
        print("alles aus")
    elif request.POST["tg_btn"]=="tg_private":
        print("privat")
    