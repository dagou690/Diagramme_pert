from django import forms
from .models import Projet, Tache


class ProjetForm(forms.ModelForm):
    class Meta:
        model = Projet
        fields = ['nom', 'description', 't0']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'placeholder': 'Nom du projet',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'rows': 3,
                'placeholder': 'Description (optionnel)',
            }),
            't0': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'min': 0,
            }),
        }
        labels = {
            'nom': 'Nom du projet',
            'description': 'Description',
            't0': 'Jour de début (T₀)',
        }


class TacheForm(forms.ModelForm):
    class Meta:
        model = Tache
        fields = ['id_tache', 'nom', 'duree']
        widgets = {
            'id_tache': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg uppercase',
                'placeholder': 'A, B, C...',
                'maxlength': 10,
            }),
            'nom': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'placeholder': 'Nom de la tâche',
            }),
            'duree': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'min': 1,
                'placeholder': '5',
            }),
        }
        labels = {
            'id_tache': 'ID Tâche',
            'nom': 'Nom',
            'duree': 'Durée (jours)',
        }

    def __init__(self, *args, projet=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.projet = projet
