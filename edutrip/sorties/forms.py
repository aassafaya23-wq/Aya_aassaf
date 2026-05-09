from django import forms
from .models import Sortie, Classe, Enseignant


class SortieForm(forms.ModelForm):
    class Meta:
        model = Sortie
        fields = ['ville', 'date_sortie', 'classe', 'nb_eleves', 'responsable']
        widgets = {
            'date_sortie': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'ville': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Paris'}),
            'classe': forms.Select(attrs={'class': 'form-select'}),
            'nb_eleves': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'responsable': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'ville': 'Destination (Ville)',
            'date_sortie': 'Date de la sortie',
            'classe': 'Classe participante',
            'nb_eleves': "Nombre d'élèves",
            'responsable': 'Enseignant responsable',
        }


class ClasseForm(forms.ModelForm):
    class Meta:
        model = Classe
        fields = ['nom_classe', 'niveau']
        widgets = {
            'nom_classe': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 2nde A'}),
            'niveau': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'nom_classe': 'Nom de la classe',
            'niveau': 'Niveau scolaire',
        }


class EnseignantForm(forms.ModelForm):
    class Meta:
        model = Enseignant
        fields = ['nom', 'prenom', 'matiere']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'matiere': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Mathématiques'}),
        }
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'matiere': 'Matière enseignée',
        }


class RechercheForm(forms.Form):
    ville = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rechercher par ville...'}),
        label='Ville'
    )
    classe = forms.ModelChoiceField(
        queryset=Classe.objects.all(),
        required=False,
        empty_label='-- Toutes les classes --',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Classe'
    )
    responsable = forms.ModelChoiceField(
        queryset=Enseignant.objects.all(),
        required=False,
        empty_label='-- Tous les responsables --',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Responsable'
    )
    date_debut = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Du'
    )
    date_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Au'
    )
