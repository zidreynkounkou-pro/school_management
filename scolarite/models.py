# scolarite/models.py - Les tables de la base de données
from django.db import models  # On importe la boîte à outils Django pour créer des tables

# TABLE 1 : Année scolaire
class AnneeScolaire(models.Model):  # class = 1 table. AnneeScolaire = nom de la table
    libelle = models.CharField(max_length=20, default="2026-2027")  # Colonne texte court, max 20 lettres, par défaut 2026-2027
    est_active = models.BooleanField(default=True)  # Colonne Vrai/Faux, case à cocher
    def __str__(self):  # __str__ = comment Django affiche l'objet dans /admin/. Sans ça : "AnneeScolaire object (1)"
        return self.libelle  # self = cette année-ci. On affiche son libellé, ex: "2026-2027"

# TABLE 2 : Classe
class Classe(models.Model):
    nom = models.CharField(max_length=20)  # Ex: 3ème A
    annee = models.ForeignKey(AnneeScolaire, on_delete=models.CASCADE, related_name='classes')  # ForeignKey = lien "cette classe appartient à une année". CASCADE = si on supprime l'année, on supprime ses classes. related_name = surnom pour faire annee.classes.all()
    capacite = models.PositiveSmallIntegerField(default=45)  # Nombre positif, 45 par défaut
    @property  # @property = transforme une méthode en attribut, on écrit classe.effectif sans parenthèses
    def effectif(self):  # Méthode qui calcule l'effectif en direct, pas en dur
        return self.eleves.filter(statut='Actif').count()  # self.eleves = élèves de cette classe. filter(Actif) = règle cahier p.8 : pas les Transférés. count() = compte
    def __str__(self):  # Pour afficher "3ème A" dans l'admin au lieu de "Classe object"
        return self.nom

# TABLE 3 : Élève - COMPLET pour la Page 04

class Eleve(models.Model):
    class Statut(models.TextChoices):
        ACTIF = 'Actif', 'Actif'
        TRANSFERE = 'Transfere', 'Transféré'

    class Genre(models.TextChoices):
        FILLE = 'F', 'Fille'
        GARCON = 'M', 'Garçon'

    matricule = models.CharField(max_length=20, unique=True, editable=False)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    genre = models.CharField(max_length=1, choices=Genre.choices, default='F')
    date_naissance = models.DateField()
    classe = models.ForeignKey('Classe', on_delete=models.SET_NULL, null=True, related_name='eleves')
    annee = models.ForeignKey('AnneeScolaire', on_delete=models.SET_NULL, null=True, related_name='eleves')
    statut = models.CharField(max_length=20, choices=Statut.choices, default='Actif')
    acte_naissance = models.CharField(max_length=100, blank=True, verbose_name="N° Acte de naissance")
    contact_urgence = models.CharField(max_length=20, blank=True)
    ecole_precedente = models.CharField(max_length=100, blank=True, verbose_name="École précédente")
    groupe_sanguin = models.CharField(max_length=5, blank=True)

    def save(self, *args, **kwargs):
        if not self.matricule:
            last = Eleve.objects.order_by('-id').first()
            num = (last.id + 1) if last else 1
            self.matricule = f"EC-2026-{num:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

""""
class Eleve(models.Model):
    class Statut(models.TextChoices):  # Choix limités pour le statut
        ACTIF = 'Actif', 'Actif'  # Valeur stockée = 'Actif', affichée = 'Actif'
        TRANSFERE = 'Transfere', 'Transféré'  # Transféré = caché dans la liste
    matricule = models.CharField(max_length=20, unique=True, editable=False)  # unique = pas 2 mêmes matricules. editable=False = on ne le modifie pas à la main, généré auto
    nom = models.CharField(max_length=100)  # Nom de famille
    prenom = models.CharField(max_length=100)  # Prénom
    genre = models.CharField(max_length=1, choices=[('M','M'),('F','F')])  # M ou F seulement
    date_naissance = models.DateField()  # Date, avec calendrier
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.ACTIF)  # Statut, par défaut Actif
    classe = models.ForeignKey(Classe, on_delete=models.SET_NULL, null=True, blank=True, related_name='eleves')  # Lien vers Classe. SET_NULL = si on supprime la classe, l'élève reste mais sans classe. null=True = autorisé vide
    annee = models.ForeignKey(AnneeScolaire, on_delete=models.CASCADE)  # Lien vers Année
    # --- NOUVEAUX CHAMPS PAGE 04 ---
    numero_acte_naissance = models.CharField(max_length=50, blank=True)  # N° acte de naissance, cahier p.9. blank=True = peut être vide au début
    contact_urgence = models.CharField(max_length=20, blank=True)  # Téléphone d'urgence, ex: +242 06 123 45 67
    groupe_sanguin = models.CharField(max_length=5, blank=True, choices=[('A+','A+'),('A-','A-'),('B+','B+'),('O+','O+'),('O-','O-'),('AB+','AB+')])  # Groupe sanguin = donnée santé mineur. Visible Direction/Infirmerie seulement, avec cadenas (on le gérera dans le template)
    def save(self, *args, **kwargs):  # save() = méthode appelée quand on clique Enregistrer. On la surcharge pour générer le matricule
        if not self.matricule:  # Si l'élève n'a pas encore de matricule (nouvel élève)
            self.matricule = f"EC-{self.annee.libelle[:4]}-{Eleve.objects.count()+1:04d}"  # f-string : EC- + 4 premiers chiffres de l'année (2026) + - + nombre d'élèves+1 sur 4 chiffres (0001)
        super().save(*args, **kwargs)  # super().save = appelle le vrai save de Django pour enregistrer en base. Sans ça, rien n'est enregistré.
    def __str__(self):  # Pour afficher "OKEMBA Sarah" au lieu de "Eleve object"
        return f"{self.nom} {self.prenom}" 

    """

# TABLE 4 : Tuteur - NOUVEAU PAGE 04, multi-tuteurs
class Tuteur(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name='tuteurs')  # Un tuteur appartient à un élève. Un élève peut avoir plusieurs tuteurs (Père + Mère). related_name = eleve.tuteurs.all()
    nom = models.CharField(max_length=100)  # Nom du tuteur
    prenom = models.CharField(max_length=100)  # Prénom du tuteur
    telephone = models.CharField(max_length=20)  # Téléphone du tuteur, pour SMS
    lien = models.CharField(max_length=20, choices=[('Pere','Père'),('Mere','Mère'),('Tuteur','Tuteur légal')])  # Lien de parenté
    def __str__(self):  # Affiche "Père - ITOUA Jean"
        return f"{self.lien} - {self.nom} {self.prenom}"

# TABLE 5 : Pièce jointe - Drag & Drop PAGE 04
class PieceJointe(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name='pieces')  # Pièce appartient à un élève
    fichier = models.FileField(upload_to='pieces/')  # FileField = colonne pour fichier. upload_to = dossier où Django stocke le fichier : media/pieces/
    type_piece = models.CharField(max_length=30, choices=[('Acte','Acte de naissance'),('Photo','Photo'),('Bulletin','Bulletin')])  # Type de pièce
    def __str__(self):  # Affiche "Acte - OKEMBA Sarah"
        return f"{self.type_piece} - {self.eleve}"