from django.urls import path
from . import views

app_name = 'projets'

urlpatterns = [
    # Projets
    path('', views.projets_index, name='index'),
    path('creer/', views.projets_creer, name='creer'),
    path('<int:pk>/', views.projets_afficher, name='afficher'),
    path('<int:pk>/modifier/', views.projets_modifier, name='modifier'),
    path('<int:pk>/supprimer/', views.projets_supprimer, name='supprimer'),

    # Tâches
    path('<int:projet_pk>/taches/', views.taches_enregistrer, name='taches_enregistrer'),
    path('taches/<int:pk>/supprimer/', views.taches_supprimer, name='taches_supprimer'),

    # Diagramme PERT
    path('<int:projet_pk>/pert/', views.pert_afficher, name='pert_afficher'),
]
