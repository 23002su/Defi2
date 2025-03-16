from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, LoginForm, UtilisateurForm
from .models import Utilisateur, Mot, Variante, Contribution, Commentaire


def profile(request):
    if 'user_id' not in request.session:
        return redirect('login')  # Redirect to login if user is not logged in
    user = Utilisateur.objects.get(id=request.session['user_id'])
    return render(request, 'authentification/profile.html', {'user': user})

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
                    return redirect('profile')  # Redirect to the home page after login
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


def users_list(request):
    if 'user_id' in request.session: 
        user = Utilisateur.objects.get(id=request.session['user_id'])
        if user.role == 'Admin':
            if request.method == 'POST':
                form = UtilisateurForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('users_list')
            else:
                form = UtilisateurForm()
            
            users = Utilisateur.objects.all()
            return render(request, 'admin/users_list.html', {'users': users, 'form': form, 'user': user})
        else:
            return redirect('profile')
    else:
        return redirect('login')

# Update User
def update_user(request, id):
    if 'user_id' in request.session: 
        user1 = Utilisateur.objects.get(id=request.session['user_id'])
        if user1.role == 'Admin':
            user = get_object_or_404(Utilisateur, id=id)
            if request.method == 'POST':
                form = UtilisateurForm(request.POST, instance=user)
                if form.is_valid():
                    form.save()
                    return redirect('users_list')
            else:
                form = UtilisateurForm(instance=user)
            return render(request, 'admin/users_list.html', {'form': form, 'user': user})
        else:
            return redirect('profile')
    else:
        return redirect('login')

# Delete User
def delete_user(request, id):
    if 'user_id' in request.session: 
        user1 = Utilisateur.objects.get(id=request.session['user_id'])
        if user1.role == 'Admin':
            user = get_object_or_404(Utilisateur, id=id)
            if request.method == 'POST':
                user.delete()
                return redirect('users_list')
            return render(request, 'admin/users_list.html', {'user': user})
        else:
            return redirect('profile')
    else:
        return redirect('login')