from django import forms
from .models import Suggestion
from .models import Probleme
from .models import publicites


class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['suggestion']
        widgets = {
            'suggestion': forms.Textarea(attrs={
                'class': 'suggestion-input',
                'placeholder': 'Votre suggestion pour cette voie...',
                'rows': 4
            })
        }
   
   

class ProblemeForm(forms.ModelForm):
    class Meta:
        model = Probleme
        fields = ['nom_complet', 'telephone', 'probleme', 'description']
        widgets = {
            'nom_complet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom complet'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro de téléphone'}),
            'probleme': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quel est le problème ?'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description (facultative)', 'rows': 4}),
        }


class PublicitesForm(forms.ModelForm):
    class Meta:
        model = publicites
        fields = ['titre', 'description', 'image', 'video', 'type_media']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'type_media': forms.Select(attrs={'class': 'form-select'}),
        }