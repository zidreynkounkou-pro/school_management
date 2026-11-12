# finance/models.py - Les tables pour l'argent (Page 09 Frais, mais on la prépare dès maintenant)
from django.db import models  # models = boîte à outils pour créer des tables (CharField, IntegerField, etc.)
from scolarite.models import Eleve  # On importe Eleve depuis l'app scolarite. On en a besoin pour dire "ce paiement appartient à quel élève ?"

class Paiement(models.Model):  # class Paiement = 1 table qui s'appellera finance_paiement. C'est la table des paiements
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name='paiements')  # ForeignKey = lien "ce paiement appartient à un élève". CASCADE = si on supprime l'élève, on supprime aussi ses paiements. related_name='paiements' = pour faire eleve.paiements.all() : tous les paiements de cet élève
    montant = models.PositiveIntegerField()  # PositiveIntegerField = nombre entier positif, pas de négatif, pas de virgule. Ex: 45000 FCFA. On ne met pas de décimale pour le FCFA
    mode = models.CharField(max_length=30, choices=[('MTN','MTN'),('Airtel','Airtel'),('Especes','Espèces')], default='Especes')  # CharField = texte court. choices = on ne peut choisir que MTN, Airtel ou Espèces. default='Especes' = si on ne met rien, c'est Espèces
    reference = models.CharField(max_length=50, blank=True)  # reference = numéro de transaction, ex: R-8502 pour rapprochement MTN (cahier p.14). blank=True = peut être vide si paiement en espèces
    date = models.DateField(auto_now_add=True)  # DateField = date. auto_now_add=True = Django met automatiquement la date du jour quand on crée le paiement, tu n'as rien à taper
    def __str__(self):  # __str__ = comment Django affiche le paiement dans /admin/. Sans ça : "Paiement object (1)". Avec ça : "OKEMBA Sarah - 45000 FCFA"
        return f"{self.eleve} - {self.montant} FCFA"  # f-string = on mélange texte et variables. self.eleve = l'élève de CE paiement-ci (grâce à __str__ de Eleve, ça affiche "OKEMBA Sarah"). self.montant = le montant