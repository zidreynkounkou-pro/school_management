# accounts/models.py - Les tables pour la connexion (Page 01)
from django.contrib.auth.models import AbstractUser  # AbstractUser = la classe mère de Django pour un utilisateur. On hérite d'elle pour garder tout ce qui marche déjà (mot de passe haché, is_active, etc.) et ajouter nos champs
from django.db import models  # models = boîte à outils pour créer des tables (CharField, BooleanField, etc.)

class User(AbstractUser):  # class User = 1 table qui s'appellera accounts_user. (AbstractUser) = "on part du User de Django et on le personnalise"
    class Role(models.TextChoices):  # class Role = liste de choix limités pour le rôle. TextChoices = Django te force à choisir parmi ces valeurs
        DIRECTION = 'DIRECTION', 'Direction'  # Valeur stockée = 'DIRECTION', affichée = 'Direction'. 1ère valeur = en base, 2ème = dans l'admin
        CENSEUR = 'CENSEUR', 'Censeur'  # 2ème rôle du cahier v2.1
        SURVEILLANT = 'SURVEILLANT', 'Surveillant Général'  # 3ème rôle
        SECRETARIAT = 'SECRETARIAT', 'Secrétariat'  # 4ème rôle
        COMPTABLE = 'COMPTABLE', 'Comptable'  # 5ème rôle, a besoin du 2FA SMS comme Direction
        ENSEIGNANT = 'ENSEIGNANT', 'Enseignant'  # 6ème rôle, ne voit pas Frais dans le menu
        PARENT = 'PARENT', 'Parent'  # 7ème rôle, par défaut
    # --- Nos champs en plus, par rapport au User de Django ---
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.PARENT)  # CharField = texte court. max_length=20 = max 20 lettres. choices=Role.choices = on ne peut choisir que parmi les 7 rôles ci-dessus. default=PARENT = si on ne met rien, c'est Parent
    telephone = models.CharField(max_length=20, unique=True, null=True, blank=True)  # telephone = pour se connecter avec le téléphone (cahier p.5). unique=True = pas 2 comptes avec même tel. null=True = en base, autorisé vide. blank=True = dans le formulaire, autorisé vide
    email = models.EmailField(unique=True)  # EmailField = texte qui doit ressembler à un email (avec @). unique=True = pas 2 comptes même email. C'est notre identifiant principal
    failed_attempts = models.PositiveSmallIntegerField(default=0)  # PositiveSmallIntegerField = petit nombre positif (0 à 32767). default=0 = au début, 0 échec. Pour bloquer après 5 échecs, cahier p.19
    last_failed_at = models.DateTimeField(null=True, blank=True)  # DateTimeField = date + heure. null=True + blank=True = peut être vide au début (pas encore d'échec). On y stocke l'heure du dernier échec pour le blocage 15 min
    USERNAME_FIELD = 'email'  # USERNAME_FIELD = "Django, pour te connecter, utilise l'email, pas le username". C'est la ligne la plus importante. Sans elle, Django demande username
    REQUIRED_FIELDS = ['username']  # REQUIRED_FIELDS = quand on fait createsuperuser, Django demande aussi username en plus de l'email, pour compatibilité
    def __str__(self):  # __str__ = comment Django affiche l'utilisateur dans /admin/. Sans ça : "User object (1)". Avec ça : "direction@ecole.cg (DIRECTION)"
        return f"{self.email} ({self.role})"  # f-string = on mélange texte et variables. self.email = l'email de CET utilisateur-ci. self.role = son rôle

class AuditLog(models.Model):  # class AuditLog = 2ème table, le journal. C'est celle qui manquait et qui faisait planter.
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # ForeignKey = lien "ce log appartient à un utilisateur". SET_NULL = si on supprime l'utilisateur, on garde le log mais user devient vide (null). On ne veut pas perdre l'historique
    action = models.CharField(max_length=50)  # action = ce qui s'est passé, ex: "CONNEXION_OK", "ECHEC", "BLOCAGE". Max 50 lettres
    details = models.CharField(max_length=200, blank=True)  # details = précision, ex: "Tentative 3". blank=True = peut être vide
    date = models.DateTimeField(auto_now_add=True)  # DateTimeField = date + heure. auto_now_add=True = Django met automatiquement la date de création, tu n'as rien à taper
    def __str__(self):  # Pour afficher "CONNEXION_OK - direction@ecole.cg" au lieu de "AuditLog object"
        return f"{self.action} - {self.user}"  # On affiche l'action et l'utilisateur