# core/views.py - La logique de la Page 02 Dashboard
from django.shortcuts import render  # render = afficher un template HTML avec des données
from django.contrib.auth.decorators import login_required  # @login_required = vigile : si pas connecté, on va à /connexion/
from django.db.models import Sum  # Sum = fonction pour faire la somme en base, ex: somme de tous les montants
from scolarite.models import Eleve, Classe  # On importe Eleve et Classe pour compter les élèves et les classes
from finance.models import Paiement  # On importe Paiement. C'est cette ligne qui plantait avant, parce que Paiement n'existait pas dans finance/models.py

@login_required  # Vigile : page privée
def dashboard(request):  # def dashboard = vue du dashboard. request = ce que le navigateur envoie
    nb_eleves = Eleve.objects.filter(statut='Actif').count()  # Eleve.objects = gestionnaire pour parler à la table Eleve. filter(Actif) = garde seulement les Actifs. count() = compte. Au début : 0. Quand tu ajoutes Sarah : 1. C'est dynamique, pas en dur.
    nb_classes = Classe.objects.count()  # Compte le nombre de classes. Au début : 0
    total_encaisse = Paiement.objects.aggregate(s=Sum('montant'))['s'] or 0  # Paiement.objects.aggregate = calcule la somme. Sum('montant') = somme de la colonne montant. ['s'] = on récupère le résultat qui s'appelle 's'. or 0 = si pas de paiement, la somme vaut None, on met 0 à la place
    total_attendu = 45200000  # 45.2M = attendu fixe du cahier, pour calculer le %. C'est une estimation du cahier, on la garde pour le calcul
    taux = round((total_encaisse / total_attendu * 100), 1) if total_attendu else 0  # taux = encaissé / attendu * 100, arrondi à 1 décimale. Ex: 35100000 / 45200000 * 100 = 77.7%. Au début : 0 / 45200000 = 0%
    is_empty = (nb_eleves == 0)  # is_empty = True si 0 élève, False sinon. Pour afficher le message jaune "Base vide - C'est normal" dans le template
    return render(request, 'core/dashboard.html', {  # render = affiche le template dashboard.html avec les données
        'nb_eleves': nb_eleves,  # On envoie nb_eleves au HTML, on l'affichera avec {{ nb_eleves }}
        'nb_classes': nb_classes,  # On envoie nb_classes
        'total_encaisse': total_encaisse,  # On envoie total_encaisse
        'total_attendu': total_attendu,  # On envoie total_attendu
        'taux': taux,  # On envoie taux
        'is_empty': is_empty,  # On envoie is_empty pour le message vide
    })