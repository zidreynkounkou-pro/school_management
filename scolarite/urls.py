# scolarite/urls.py - Chaque page = 1 ligne
from django.urls import path  # path = fonction pour déclarer une URL
from . import views  # On importe nos vues
urlpatterns = [  # Liste des URLs de l'app scolarite
    path('eleves/', views.liste_eleves, name='liste_eleves'),  # /eleves/ -> vue liste_eleves. name = petit nom pour {% url %}
    path('eleves/import/', views.importer_excel_eleves, name='importer_eleves'),  # Déjà fait
    path('eleves/inscription/', views.inscription_view, name='inscription'),  # NOUVEAU : /eleves/inscription/ -> vue inscription_view
]