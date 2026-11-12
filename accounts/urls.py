# accounts/urls.py - Les URL de l'app accounts (Page 01 Connexion)
from django.urls import path  # path = fonction qui déclare une URL : "quand on tape ça, appelle cette vue"
from . import views  # . = dossier actuel (accounts). On importe views.py du même dossier. views = nos fonctions connexion, verif_sms, deconnexion

urlpatterns = [  # urlpatterns = liste que Django lit. Chaque ligne = 1 page
    path('connexion/', views.connexion_view, name='connexion'),  # path('connexion/') = URL http://127.0.0.1:8000/connexion/. views.connexion_view = fonction à appeler. name='connexion' = petit nom pour {% url 'connexion' %} dans le HTML
    path('verif-sms/', views.verif_sms_view, name='verif_sms'),  # /verif-sms/ -> page du code SMS 123456 pour Direction/Comptable
    path('deconnexion/', views.deconnexion_view, name='deconnexion'),  # /deconnexion/ -> déconnecte et renvoie à /connexion/
]