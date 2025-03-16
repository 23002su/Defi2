from django import forms
from .models import Utilisateur, Commentaire, Contribution, Mot


class UtilisateurForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['email', 'role', 'score', 'mot_de_passe']
        widgets = {
            'mot_de_passe': forms.PasswordInput(),
        }



class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Utilisateur
        fields = ['email', 'role', 'mot_de_passe']
        widgets = {
            'mot_de_passe': forms.PasswordInput,
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("mot_de_passe")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")

class LoginForm(forms.Form):
    email = forms.EmailField()
    mot_de_passe = forms.CharField(widget=forms.PasswordInput)
    
    
class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['commentaire']    

class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ['mot', 'transliteration', 'definition']  # Include all necessary fields
        widgets = {
            'mot': forms.TextInput(attrs={'class': 'form-control'}),
            'transliteration': forms.TextInput(attrs={'class': 'form-control'}),
            'definition': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }  
        
        
        
        
class MotForm(forms.ModelForm):
    class Meta:
        model = Mot
        fields = ['mot_hassaniya', 'transliteration', 'definition']   
        
        
        
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['commentaire']
        widgets = {
            'commentaire': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }                  