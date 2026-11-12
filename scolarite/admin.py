# scolarite/admin.py
# admin.py = on dit à Django "affiche ces modèles dans /admin/"
from django.contrib import admin
from .models import AnneeScolaire, Classe, Eleve

@admin.register(AnneeScolaire)
class AnneeAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'est_active') # Colonnes visibles dans l'admin

@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'annee', 'effectif') # effectif = notre @property

@admin.register(Eleve)
class EleveAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'nom', 'prenom', 'classe', 'statut')
    list_filter = ('statut', 'classe') # Filtre à droite dans l'admin
    search_fields = ('nom', 'prenom', 'matricule') # Barre de recherche