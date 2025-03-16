from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, LoginForm, UtilisateurForm, CommentaireForm, ContributionForm, MotForm, ReplyForm
from .models import Utilisateur, Mot, Variante, Contribution, Commentaire
from django.http import JsonResponse
from django.core.paginator import Paginator


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
    
    
    
# List Contributions
def contributions_list(request):
    user = Utilisateur.objects.get(id=request.session['user_id'])
    contributions = Contribution.objects.filter(statut='en attente')  # Only show pending contributions
    return render(request, 'admin/contributions_list.html', {'contributions': contributions, 'user': user})

# Validate or Reject Contribution
def validate_contribution(request, id):
    contribution = get_object_or_404(Contribution, id=id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'validate':
            # Update the contribution status
            contribution.statut = 'valide'

            # Add the word to the Mot model
            Mot.objects.create(
                mot_hassaniya=contribution.mot,
                transliteration=contribution.transliteration,
                definition=contribution.definition
            )

            # Add 2 points to the contributor's score
            contributor = contribution.id_contribiteur
            contributor.score += 2
            contributor.save()

        elif action == 'reject':
            contribution.statut = 'rejeté'  # Add 'rejeté' to STATUT_CHOICES if not already present

        # Assign the moderator (current user)
        user = Utilisateur.objects.get(id=request.session['user_id'])
        contribution.id_moderateur = user

        # Save the updated contribution
        contribution.save()

        return redirect('contributions_list')
    return redirect('contributions_list')

# Add Comment to Contribution
def add_comment(request, id):
    contribution = get_object_or_404(Contribution, id=id)
    if request.method == 'POST':
        form = CommentaireForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            user = Utilisateur.objects.get(id=request.session['user_id'])
            comment.id_moderateur = user
            comment.id_contributeur = contribution.id_contribiteur
            comment.contribution = contribution  # Set the contribution field
            comment.save()
            return redirect('contributions_list')
    else:
        form = CommentaireForm()
    return render(request, 'admin/contributions_list.html', {'form': form, 'contribution': contribution, 'user': user})


# Suggest a Word
def suggest_word(request):
    if request.method == 'POST':
        form = ContributionForm(request.POST)
        if form.is_valid():
            contribution = form.save(commit=False)
            user = Utilisateur.objects.get(id=request.session['user_id'])
            contribution.id_contribiteur = user
            contribution.statut = 'en attente'  # Set status to 'pending'
            contribution.save()
            if user.role == 'Admin' or user.role == 'Modérateur':
                return redirect('contributions_list')
            else:
                return render(request, 'dictionnaire/search_results.html', {'user': user})
    else:
        form = ContributionForm()
    return render(request, 'contributions_list.html', {'form': form, 'user':user})   

def search_word(request):
    if 'user_id' in request.session:
        user = Utilisateur.objects.get(id=request.session['user_id'])
        if request.method == 'GET':
            search_term = request.GET.get('search_term', '').strip()
            
            # Check if the word exists in the dictionary
            try:
                mot = Mot.objects.get(mot_hassaniya__iexact=search_term)
                variants = Variante.objects.filter(mot=mot)
                return render(request, 'dictionnaire/search_results.html', {
                    'mot': mot,
                    'variants': variants,
                    'exists': True,
                })
            except Mot.DoesNotExist:
                # Word doesn't exist, show the suggestion popup
                return render(request, 'dictionnaire/search_results.html', {
                    'exists': False,
                    'search_term': search_term,
                    'user': user,
                })

        return render(request, 'dictionnaire/search_results.html', {'user': user})
    
    
    
def list_words(request):
    if 'user_id' in request.session: 
        user = Utilisateur.objects.get(id=request.session['user_id'])
        mots_list = Mot.objects.all().order_by('mot_hassaniya')
        paginator = Paginator(mots_list, 6)  # Show 10 words per page
        page = request.GET.get('page')
        mots = paginator.get_page(page)
        return render(request, 'dictionnaire/dictionnaire.html', {'mots': mots, 'user': user})
    else:
        return redirect('login')   


def add_word(request):
    if request.method == 'POST':
        form = MotForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('list_words')


def update_word(request, id):
    mot = get_object_or_404(Mot, id=id)
    if request.method == 'POST':
        form = MotForm(request.POST, instance=mot)
        if form.is_valid():
            form.save()
    return redirect('list_words')



def delete_word(request, id):
    mot = get_object_or_404(Mot, id=id)
    if request.method == 'POST':
        mot.delete()
    return redirect('list_words')


def user_contributions(request):
    if 'user_id' not in request.session:
        return redirect('login')  # Redirect to login if user is not logged in

    user = Utilisateur.objects.get(id=request.session['user_id'])
    contributions = Contribution.objects.filter(id_contribiteur=user).order_by('-id')

    # Fetch commenters for each contribution
    for contribution in contributions:
        # Get unique commenters for this contribution
        commenters = Utilisateur.objects.filter(
            commentaires_moderator__contribution=contribution
        ).distinct()
        print(f"Contribution: {contribution.mot}, Commenters: {commenters}")  # Debugging
        contribution.commenters = commenters  # Add commenters to the contribution object

    return render(request, 'commentaire/user_contributions.html', {'contributions': contributions, 'user': user})


def view_comments(request, contribution_id, commenter_id=None):
    if 'user_id' not in request.session:
        return redirect('login')  # Redirect to login if user is not logged in

    user = Utilisateur.objects.get(id=request.session['user_id'])
    contribution = get_object_or_404(Contribution, id=contribution_id)

    # Get all commenters for this contribution
    commenters = Utilisateur.objects.filter(
        commentaires_moderator__contribution=contribution
    ).distinct()

    # If a specific commenter is selected, get their comments
    comments = []
    selected_commenter = None
    if commenter_id:
        selected_commenter = get_object_or_404(Utilisateur, id=commenter_id)
        comments = Commentaire.objects.filter(
            id_moderateur=selected_commenter,
            id_contributeur=user,
            contribution=contribution
        )

    return render(request, 'commentaire/view_comments.html', {
        'contribution': contribution,
        'commenters': commenters,
        'comments': comments,
        'selected_commenter': selected_commenter,  # Pass the selected commenter
        'user': user,
    })
    
    
def reply_to_comment(request, contribution_id, commenter_id):
    if 'user_id' not in request.session:
        return redirect('login')  # Redirect to login if user is not logged in

    user = Utilisateur.objects.get(id=request.session['user_id'])
    contribution = get_object_or_404(Contribution, id=contribution_id)
    commenter = get_object_or_404(Utilisateur, id=commenter_id)

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            # Create a new Commentaire object
            reply = Commentaire(
                id_moderateur=user,  # The current user is the moderator
                id_contributeur=commenter,  # The commenter is the contributor
                contribution=contribution,  # Link to the contribution
                commentaire=form.cleaned_data['commentaire'],  # The reply text
                is_seen=False  # Mark the reply as unseen
            )
            reply.save()
            return redirect('view_comments', contribution_id=contribution_id, commenter_id=commenter_id)
    else:
        form = ReplyForm()

    return render(request, 'commentaire/reply_to_comment.html', {
        'form': form,
        'contribution': contribution,
        'commenter': commenter,
        'user': user,
    })    