from django import forms
from .models import Utilisateur


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