from django.db import models

# Custom User model extending AbstractUser
class Utilisateur(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Modérateur', 'Modérateur'),
        ('Contributeur', 'Contributeur'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Contributeur')
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.username

# Model for Mot (Word)
class Mot(models.Model):
    mot_hassaniya = models.CharField(max_length=255)
    transliteration = models.CharField(max_length=255, blank=True, null=True)
    definition = models.TextField()

    def __str__(self):
        return self.mot_hassaniya

# Model for Contributions
class Contribution(models.Model):
    STATUT_CHOICES = [
        ('en attente', 'En attente'),
        ('valide', 'Valide'),
    ]
    id_contribiteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='contributions_contributor')
    id_moderateur = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True, related_name='contributions_moderator')
    mot = models.CharField(max_length=255)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en attente')

    def __str__(self):
        return f"Contribution by {self.id_contribiteur} - {self.mot}"

# Model for Commentaires (Comments)
class Commentaire(models.Model):
    id_moderateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='commentaires_moderator')
    id_contributeur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='commentaires_contributor')
    commentaire = models.TextField()
    date = models.DateField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.id_moderateur} on {self.date}"

# Model for Variante (Variants)
class Variante(models.Model):
    TYPE_CHOICES = [
        ('Pluriel', 'Pluriel'),
        ('Conjugaison', 'Conjugaison'),
        ('Dérivation', 'Dérivation'),
    ]
    mot = models.ForeignKey(Mot, on_delete=models.CASCADE, related_name='variantes')
    forme = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.forme} ({self.type})"

# Model for Document
class Document(models.Model):
    nom_fichier = models.CharField(max_length=255)
    chemin_fichier = models.CharField(max_length=255)
    ajoute_par = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='documents')

    def __str__(self):
        return self.nom_fichier

# Model for Mot_extrait (Extracted Words)
class MotExtrait(models.Model):
    STATUT_CHOICES = [
        ('À examiner', 'À examiner'),
        ('Confirmé', 'Confirmé'),
    ]
    mot = models.ForeignKey(Mot, on_delete=models.SET_NULL, null=True, blank=True, related_name='mots_extraits')
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='mots_extraits')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='À examiner')

    def __str__(self):
        return f"Extracted word from {self.document.nom_fichier}"