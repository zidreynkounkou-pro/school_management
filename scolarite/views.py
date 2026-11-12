"""

# scolarite/views.py - On ajoute en bas du fichier, après liste_eleves
from .forms import EleveForm  # On importe le formulaire qu'on vient de créer
from .models import Tuteur  # On importe Tuteur pour créer les tuteurs
# scolarite/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # Norme : page privée, pas pour les anonymes
from django.db.models import Q # Q = pour chercher dans plusieurs colonnes en même temps (OU)
from django.core.paginator import Paginator # Pagination = 20 par page, pas 1248 d'un coup
from django.contrib import messages
from .models import Eleve, Classe, AnneeScolaire
import openpyxl # Pour lire Excel

@login_required
def liste_eleves(request):

    PAGE 03 - Liste des élèves
    Règle métier cahier p.8 : on n'affiche que les Actifs.
    Un Transféré comme LOUBAKI Nina ne doit PAS apparaître.

    # 1. On part de tous les élèves Actifs, triés par nom
    # select_related = optimise la requête, évite 1000 requêtes SQL (norme industrie)
    eleves = Eleve.objects.filter(statut='Actif').select_related('classe', 'annee').order_by('nom')

    # 2. Recherche : si l'utilisateur a tapé dans la barre ?q=OKEMBA
    q = request.GET.get('q', '').strip()
    if q:
        # Q(nom__icontains) = nom contient, insensible à la casse
        eleves = eleves.filter(
            Q(nom__icontains=q) | Q(prenom__icontains=q) | Q(matricule__icontains=q)
        )

    # 3. Filtre par classe : ?classe=1
    classe_id = request.GET.get('classe')
    if classe_id:
        eleves = eleves.filter(classe_id=classe_id)

    # 4. Pagination : on coupe en pages de 20
    paginator = Paginator(eleves, 20)
    page_obj = paginator.get_page(request.GET.get('page'))

    # 5. On envoie tout au template
    return render(request, 'scolarite/liste_eleves.html', {
        'eleves': page_obj,      # Page actuelle
        'classes': Classe.objects.all(), # Pour le <select>
        'q': q,
        'total': paginator.count, # Ce chiffre fera passer le dashboard de 0 à 1, 2...
        'is_empty': paginator.count == 0,
    })

@login_required
def importer_excel_eleves(request):
Bouton Importer Excel de la Page 03
    from urllib import request


if request.method == 'POST' and request.FILES.get('fichier'):
        fichier = request.FILES['fichier']
        try:
            wb = openpyxl.load_workbook(fichier)
            ws = wb.active # 1ère feuille
            annee, _ = AnneeScolaire.objects.get_or_create(libelle="2026-2027", defaults={'est_active': True})
            count = 0
            # Ligne 1 = en-têtes, on commence à ligne 2
            # Colonnes attendues : Nom | Prenom | Genre | DateNaissance | Classe
            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row or not row[0]:
                    continue
                nom, prenom, genre, date_naiss, classe_nom = row[0], row[1], row[2] or 'M', row[3], row[4]
                classe = None
                if classe_nom:
                    classe, _ = Classe.objects.get_or_create(nom=classe_nom, annee=annee)
                Eleve.objects.create(
                    nom=str(nom).strip(),
                    prenom=str(prenom).strip() if prenom else '',
                    genre=genre[0].upper(),
                    date_naissance=date_naiss or '2010-01-01',
                    classe=classe,
                    annee=annee,
                )
                count += 1
            messages.success(request, f"{count} élèves importés. Le dashboard n'est plus à 0 !")
        except Exception as e:
            messages.error(request, f"Erreur Excel : {e}")
    return redirect('liste_eleves')




@login_required  # @login_required = vigile : si pas connecté, on va à /connexion/
def inscription_view(request):  # def = on définit la vue. request = tout ce que le navigateur envoie
    if request.method == 'POST':  # POST = l'utilisateur a cliqué sur "ENREGISTRER" et a envoyé le formulaire
        form = EleveForm(request.POST)  # On remplit le formulaire avec les données envoyées
        if form.is_valid():  # is_valid() = Django vérifie : nom pas vide ? date correcte ? etc.
            eleve = form.save()  # save() = enregistre l'élève en base, et renvoie l'objet élève créé
            # --- On crée le Tuteur 1 (obligatoire) ---
            Tuteur.objects.create(  # create() = crée et enregistre en 1 ligne
                eleve=eleve,  # On rattache au nouvel élève
                nom=request.POST.get('tuteur1_nom'),  # request.POST.get = récupère la valeur du champ tuteur1_nom dans le formulaire
                prenom=request.POST.get('tuteur1_prenom'),
                telephone=request.POST.get('tuteur1_tel'),
                lien=request.POST.get('tuteur1_lien', 'Pere'),  # Par défaut Père si rien
            )
            # --- Tuteur 2 (optionnel, bouton + 2e tuteur) ---
            if request.POST.get('tuteur2_nom'):  # if = seulement si l'utilisateur a rempli le 2e tuteur
                Tuteur.objects.create(
                    eleve=eleve,
                    nom=request.POST.get('tuteur2_nom'),
                    prenom=request.POST.get('tuteur2_prenom'),
                    telephone=request.POST.get('tuteur2_tel'),
                    lien=request.POST.get('tuteur2_lien', 'Mere'),
                )
            messages.success(request, f"Élève {eleve} inscrit ! Matricule {eleve.matricule}")  # Message vert de succès
            return redirect('liste_eleves')  # redirect = on renvoie vers la liste des élèves, on y verra le nouvel élève
    else:  # GET = l'utilisateur vient juste d'ouvrir la page, il n'a rien envoyé
        form = EleveForm()  # On crée un formulaire vide
    return render(request, 'scolarite/inscription.html', {'form': form})  # render = affiche le template avec le formulaire vide


"""



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Eleve, Classe, AnneeScolaire, Tuteur
from .forms import EleveForm
import openpyxl

@login_required
def liste_eleves(request):
    eleves = Eleve.objects.filter(statut='Actif').select_related('classe', 'annee').order_by('nom')
    q = request.GET.get('q', '').strip()
    if q:
        eleves = eleves.filter(Q(nom__icontains=q) | Q(prenom__icontains=q) | Q(matricule__icontains=q))
    classe_id = request.GET.get('classe')
    if classe_id:
        eleves = eleves.filter(classe_id=classe_id)
    paginator = Paginator(eleves, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'scolarite/liste_eleves.html', {
        'eleves': page_obj,
        'classes': Classe.objects.all(),
        'q': q,
        'total': paginator.count,
        'is_empty': paginator.count == 0,
    })

@login_required
def importer_excel_eleves(request):
    if request.method == 'POST' and request.FILES.get('fichier'):
        fichier = request.FILES['fichier']
        try:
            wb = openpyxl.load_workbook(fichier)
            ws = wb.active
            annee, _ = AnneeScolaire.objects.get_or_create(libelle="2026-2027", defaults={'est_active': True})
            count = 0
            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row or not row[0]:
                    continue
                nom, prenom, genre, date_naiss, classe_nom = row[0], row[1], row[2] or 'M', row[3], row[4]
                classe = None
                if classe_nom:
                    classe, _ = Classe.objects.get_or_create(nom=classe_nom, annee=annee)
                Eleve.objects.create(
                    nom=str(nom).strip(),
                    prenom=str(prenom).strip() if prenom else '',
                    genre=genre[0].upper(),
                    date_naissance=date_naiss or '2010-01-01',
                    classe=classe,
                    annee=annee,
                )
                count += 1
            messages.success(request, f"{count} élèves importés. Le dashboard n'est plus à 0 !")
        except Exception as e:
            messages.error(request, f"Erreur Excel : {e}")
    return redirect('liste_eleves')

@login_required
def inscription_view(request):
    if request.method == 'POST':
        form = EleveForm(request.POST)
        if form.is_valid():
            eleve = form.save()
            Tuteur.objects.create(
                eleve=eleve,
                nom=request.POST.get('tuteur1_nom'),
                prenom=request.POST.get('tuteur1_prenom'),
                telephone=request.POST.get('tuteur1_tel'),
                lien=request.POST.get('tuteur1_lien', 'Père'),
            )
            if request.POST.get('tuteur2_nom'):
                Tuteur.objects.create(
                    eleve=eleve,
                    nom=request.POST.get('tuteur2_nom'),
                    prenom=request.POST.get('tuteur2_prenom'),
                    telephone=request.POST.get('tuteur2_tel'),
                    lien=request.POST.get('tuteur2_lien', 'Mère'),
                )
            messages.success(request, f"Élève {eleve} inscrit ! Matricule {eleve.matricule}")
            return redirect('liste_eleves')
    else:
        form = EleveForm()
    return render(request, 'scolarite/inscription.html', {'form': form})