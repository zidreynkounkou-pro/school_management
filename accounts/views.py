# accounts/views.py - Les vues = la logique de la Page 01 Connexion
from django.shortcuts import render, redirect  # render = afficher un template HTML. redirect = renvoyer vers une autre page (ex: après login, va au dashboard)
from django.contrib.auth import authenticate, login, logout  # authenticate = vérifier email + mot de passe. login = connecter vraiment l'utilisateur (crée la session). logout = déconnecter
from django.contrib import messages  # messages = afficher un petit message vert/rouge en haut de la page ("Mot de passe faux", "Code SMS envoyé")
from django.utils import timezone  # timezone = pour avoir l'heure actuelle à Brazzaville, pour le blocage 15 min
from datetime import timedelta  # timedelta = pour calculer une durée, ex: 15 minutes
from .models import User, AuditLog  # .models = models.py du même dossier. User = notre User custom. AuditLog = journal qui a fait quoi

def connexion_view(request):  # def = on définit une fonction. connexion_view = nom de la vue, c'est celui que urls.py cherche. request = tout ce que le navigateur envoie (qui, quoi)
    if request.user.is_authenticated:  # request.user = l'utilisateur actuel. is_authenticated = est-il déjà connecté ? Si oui,
        return redirect('dashboard')  # redirect('dashboard') = renvoie directement au dashboard, pas besoin de se reconnecter
    if request.method == 'POST':  # request.method = GET ou POST. GET = on ouvre juste la page. POST = on a cliqué sur SE CONNECTER et envoyé le formulaire
        identifiant = request.POST.get('identifiant')  # request.POST = dictionnaire des données envoyées. .get('identifiant') = valeur du champ qui s'appelle "identifiant" dans le HTML (email ou téléphone)
        password = request.POST.get('password')  # .get('password') = valeur du champ mot de passe
        try:  # try = "essaie ça, si ça plante, va dans except"
            if '@' in identifiant:  # Si l'identifiant contient @, c'est un email
                user_obj = User.objects.get(email=identifiant)  # User.objects.get = cherche UN utilisateur avec cet email. objects = gestionnaire pour parler à la table
            else:  # Sinon, c'est un téléphone
                user_obj = User.objects.get(telephone=identifiant)  # Cherche avec le téléphone
        except User.DoesNotExist:  # except = si User.objects.get n'a rien trouvé, il lève l'exception DoesNotExist
            messages.error(request, "Identifiant introuvable. Vérifie email/téléphone.")  # messages.error = message rouge
            return render(request, 'accounts/connexion.html')  # render = réaffiche la page de connexion avec le message
        # --- Sécurité : blocage après 5 échecs, cahier p.19 ---
        if user_obj.failed_attempts >= 5 and user_obj.last_failed_at:  # Si déjà 5 échecs ET on a une date de dernier échec
            if timezone.now() - user_obj.last_failed_at < timedelta(minutes=15):  # timezone.now() = maintenant. - last_failed_at = temps écoulé. < 15 min = encore bloqué
                messages.error(request, "Compte bloqué 15 minutes après 5 échecs. Attends.")  # Message rouge
                return render(request, 'accounts/connexion.html')  # On réaffiche la page, on ne laisse pas essayer
            else:  # Sinon, 15 min passées, on débloque
                user_obj.failed_attempts = 0  # On remet le compteur à 0
                user_obj.save()  # save() = enregistre en base
        # --- Vérification du mot de passe ---
        user = authenticate(request, email=user_obj.email, password=password)  # authenticate = Django vérifie le mot de passe haché. Si bon, renvoie l'utilisateur. Si faux, renvoie None
        if user:  # if user = si authenticate a renvoyé un utilisateur, donc mot de passe OK
            user_obj.failed_attempts = 0  # On remet le compteur à 0, il a réussi
            user_obj.save()  # On enregistre
            AuditLog.objects.create(user=user_obj, action="CONNEXION_OK", details="Login réussi")  # AuditLog = journal. On écrit "CONNEXION_OK" pour tracer, exigence sécurité
            # --- 2FA pour Direction / Comptable, cahier p.5 ---
            if user.role in ['DIRECTION', 'COMPTABLE']:  # Si le rôle est Direction ou Comptable, on demande un 2e code
                request.session['2fa_user_id'] = user.id  # request.session = petit casier temporaire du navigateur. On y stocke l'id pour la page suivante
                print("=== CODE SMS pour apprendre : 123456 ===")  # print = affiche dans le terminal VS Code. En vrai, on enverrait un SMS MTN. Pour apprendre, on affiche 123456
                messages.info(request, "Code SMS envoyé. Pour apprendre, tape 123456")  # Message bleu
                return redirect('verif_sms')  # On renvoie vers la page du code SMS
            login(request, user)  # login = connecte vraiment, crée la session. Sans ça, l'utilisateur n'est pas connecté
            return redirect('dashboard')  # On renvoie au dashboard
        else:  # else = mot de passe faux, authenticate a renvoyé None
            user_obj.failed_attempts += 1  # +=1 = on ajoute 1 au compteur d'échecs. 0 -> 1, 1 -> 2...
            user_obj.last_failed_at = timezone.now()  # On enregistre l'heure de cet échec
            user_obj.save()  # On enregistre en base
            AuditLog.objects.create(user=user_obj, action="ECHEC", details=f"Tentative {user_obj.failed_attempts}")  # On écrit l'échec dans le journal
            messages.error(request, f"Mot de passe faux. Il te reste {5 - user_obj.failed_attempts} essais.")  # f-string = on mélange texte et calcul. Ex: 5-1 = 4 essais restants
    return render(request, 'accounts/connexion.html')  # Si GET (on ouvre juste la page) ou si on arrive ici, on affiche la page de connexion

def verif_sms_view(request):  # Vue de la page du code SMS, 2ème étape pour Direction
    user_id = request.session.get('2fa_user_id')  # On récupère l'id stocké dans la session à l'étape précédente
    if not user_id:  # Si pas d'id, c'est qu'on a essayé d'aller direct sur /verif-sms/ sans passer par connexion
        return redirect('connexion')  # On renvoie à la connexion
    if request.method == 'POST':  # Si on a envoyé le code
        if request.POST.get('code') == '123456':  # Si le code tapé est 123456 (pour apprendre)
            user = User.objects.get(id=user_id)  # On retrouve l'utilisateur
            login(request, user)  # On le connecte vraiment
            del request.session['2fa_user_id']  # del = on supprime l'id de la session, on n'en a plus besoin
            return redirect('dashboard')  # On va au dashboard
        messages.error(request, "Code faux")  # Sinon, message rouge
    return render(request, 'accounts/verif_sms.html')  # On affiche la page du code

def deconnexion_view(request):  # Vue pour se déconnecter
    logout(request)  # logout = détruit la session, déconnecte
    return redirect('connexion')  # On renvoie à la page de connexion