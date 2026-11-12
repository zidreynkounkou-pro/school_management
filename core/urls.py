# core/urls.py - Les URL de l'app core (Page 02 Dashboard)
from django.urls import path  # On importe path pour déclarer des URL
from . import views  # On importe views.py de core

urlpatterns = [  # Liste des URL de core
    path('', views.dashboard, name='dashboard'),  # path('') = page d'accueil http://127.0.0.1:8000/ -> dashboard. '' = vide = racine
    path('dashboard/', views.dashboard, name='dashboard'),  # /dashboard/ -> même vue dashboard. On a 2 chemins pour la même page, c'est volontaire
]