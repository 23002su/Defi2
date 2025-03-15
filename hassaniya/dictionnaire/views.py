from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from .models import Utilisateur


def home(request):
    if 'user_id' not in request.session:
        return redirect('login')  # Redirect to login if user is not logged in
    user = Utilisateur.objects.get(id=request.session['user_id'])
    return render(request, 'authentification/home.html', {'user': user})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after registration
    else:
        form = RegistrationForm()
    return render(request, 'authentification/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            mot_de_passe = form.cleaned_data['mot_de_passe']
            try:
                user = Utilisateur.objects.get(email=email)
                if user.mot_de_passe == mot_de_passe:  # Directly compare passwords
                    request.session['user_id'] = user.id  # Store user ID in session
                    return redirect('home')  # Redirect to the home page after login
                else:
                    form.add_error(None, "Email ou mot de passe incorrect.")
            except Utilisateur.DoesNotExist:
                form.add_error(None, "Email ou mot de passe incorrect.")
    else:
        form = LoginForm()
    return render(request, 'authentification/login.html', {'form': form})

def user_logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']  # Remove user ID from session
    return redirect('login')  # Redirect to the login page after logout