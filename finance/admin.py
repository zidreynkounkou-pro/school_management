# finance/admin.py - Pour afficher Paiement dans /admin/
from django.contrib import admin  # admin = interface d'administration
from .models import Paiement  # .models = models.py du même dossier. On importe Paiement

admin.site.register(Paiement)  # register = "Affiche Paiement dans /admin/"