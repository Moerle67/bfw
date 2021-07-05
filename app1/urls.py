from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.startAllg, name='start'),
    path('auth/', views.auth, name='auth'),
    path('logout/', views.auslogen, name='logout'),

    path('impress/', views.impress, name='impress'),
    path('fach/', views.fachAllg, name='fach'),
    path('fach/<str:fach_slug>/', views.fachDetail, name='fachDetail'),

    path('ausb/', views.ausbAllg, name="ausb"),
    path('ausb/<str:ausb_slug>/', views.ausbDetail, name="ausbDetail"),

    path('tn/lst/<int:grp_id>/', views.tnAllgGrp, name="tn"),
    path('tn/', views.tnAllg, name="tn"),
    path('tn/<int:tn_id>/', views.tnDetail, name="tnDetail"),
    path('tn/neu/', views.tnNeu, name="tnNeu"),

    path('grp/', views.grpAllg, name="grp"),
    path('grp/<int:grp_id>/', views.grpDetail, name="grpDetail"),
    path('grp/neu/', views.grpNeu, name="grpNeu"),

    path('kanban/', views.kanbanAllg, name="kanbanAllg"),
    path('kanban/neu', views.kanbanNeu, name="kanbanNeu"),
    path('kanban/<int:id>/<int:stufe>', views.kanbanStufe, name="kanbanStufe"),
    path('kanban/<int:id>/', views.kanbanEdt, name="kanbanEdt"),
    path('kanban/all/', views.kanbanAll, name="kanbanAll"),
    path('kanban/onNeu/', views.kanbanOnNeu, name = "kanbanOnNeu"),
    path('kanban/pck/', views.kanbanPck, name = "kanbanPcKlinik"),

    path('projekte/neu/', views.projekteNeu, name = 'projekteNeu'),
    path('projekt/<int:p_id>/', views.projekt, name = 'projekt'),
    path('projekte/', views.projekteAllg, name = 'projekteAllg'),
    path('projekte/tndetail/<int:ptn_id>', views.projekteTNDetail, name = 'projekteAllg'),
    path('projekt/<int:project_id>/remove/', views.projekteRemove, name = 'projekteRemove'),
    
    path('mitarbeit', views.mitarbeit, name = 'mitarbeit'),
    path('ma_auswertung', views.ma_auswertung, name = 'ma_auswertung'),

    path('essen/anmeldung/', views.essen_anmeldung, name = 'essenAnmeldung'),
    # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
