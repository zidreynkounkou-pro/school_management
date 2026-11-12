# scolarite/forms.py - On sépare le formulaire du modèle, c'est la norme industrie. forms.py = "à quoi ressemble le formulaire"
""" from django import forms  # On importe les formulaires Django
from .models import Eleve  # On importe le modèle Eleve

class EleveForm(forms.ModelForm):  # ModelForm = formulaire généré automatiquement à partir du modèle Eleve
    class Meta:  # Meta = configuration du formulaire
        model = Eleve  # On se base sur le modèle Eleve
        fields = ['nom', 'prenom', 'genre', 'date_naissance', 'classe', 'annee', 'numero_acte_naissance', 'contact_urgence', 'groupe_sanguin']  # Champs affichés dans le formulaire, dans cet ordre
        widgets = {  # widgets = comment chaque champ s'affiche en HTML
            'date_naissance': forms.DateInput(attrs={'type': 'date', 'class': 'input'}),  # type=date = calendrier dans le navigateur. class=input = notre CSS
            'nom': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Ex: OKEMBA'}),  # TextInput = <input type="text">
            'prenom': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Ex: Sarah'}),
        }

        """

from django import forms
from .models import Eleve

class EleveForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = ['nom', 'prenom', 'genre', 'date_naissance', 'classe', 'annee', 'acte_naissance', 'contact_urgence', 'ecole_precedente', 'groupe_sanguin']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Ex : OKEMBA', 'class': 'w-full border rounded-lg p-2 text-sm'}),
            'prenom': forms.TextInput(attrs={'placeholder': 'Ex : Sarah', 'class': 'w-full border rounded-lg p-2 text-sm'}),
            'genre': forms.Select(attrs={'class': 'w-full border rounded-lg p-2 text-sm'}),
            'date_naissance': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border rounded-lg p-2 text-sm'}),
            'classe': forms.Select(attrs={'class': 'w-full border rounded-lg p-2 text-sm'}),
            'annee': forms.Select(attrs={'class': 'w-full border rounded-lg p-2 text-sm'}),
            'acte_naissance': forms.TextInput(attrs={'placeholder': 'Ex : 1234 / Brazzaville', 'class': 'w-full border rounded-lg p-2 text-sm'}),
            'contact_urgence': forms.TextInput(attrs={'placeholder': '+242 06...', 'class': 'w-full border rounded-lg p-2 text-sm'}),
            'ecole_precedente': forms.TextInput(attrs={'placeholder': 'Ex : EP Sainte-Marie', 'class': 'w-full border rounded-lg p-2 text-sm'}),
            'groupe_sanguin': forms.Select(attrs={'class': 'border rounded-lg p-2 text-sm bg-white'}),
        }