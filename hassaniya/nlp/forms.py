from django import forms
from .models import HassaniyaWord

class HassaniyaWordForm(forms.ModelForm):
    class Meta:
        model = HassaniyaWord
        fields = ['mot','traduction_arabe', 'traduction_francais', 'derives', 'grammaire']
        widgets = {
            'mot': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mot en Hassaniya'}),
            'traduction_arabe': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Traduction en Arabe'}),
            'traduction_francais': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Traduction en Français'}),
            'derives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Dérivés'}),
            'grammaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Grammaire'}),
        }
