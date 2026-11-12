# accounts/admin.py - Pour voir User et AuditLog dans /admin/
from django.contrib import admin  # admin = interface d'administration
from django.contrib.auth.admin import UserAdmin  # UserAdmin = l'admin spécial pour les utilisateurs, avec gestion du mot de passe
from .models import User, AuditLog  # .models = models.py du même dossier. On importe User et AuditLog

@admin.register(User)  # @admin.register = "Affiche User dans /admin/"
class MyUserAdmin(UserAdmin):  # MyUserAdmin = notre admin pour User, on hérite de UserAdmin pour garder le hachage du mot de passe
    list_display = ('email', 'role', 'telephone', 'failed_attempts')  # list_display = colonnes visibles dans la liste /admin/
    fieldsets = UserAdmin.fieldsets + (('EduCongo', {'fields': ('role', 'telephone', 'failed_attempts', 'last_failed_at')}),)  # fieldsets = groupes de champs dans le formulaire. On ajoute un groupe "EduCongo" avec nos champs

admin.site.register(AuditLog)  # On affiche aussi AuditLog dans /admin/, sans personnalisation