from django.db import models

class SuggestionMot(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('accepté', 'Accepté'),
        ('rejeté', 'Rejeté'),
    ]

    mot = models.CharField(max_length=255)
    variation_generee = models.CharField(max_length=255, verbose_name='Variation générée')
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente',
        verbose_name='Statut'
    )
    cree_le = models.DateTimeField(auto_now_add=True, verbose_name='Créé le')

    def __str__(self):
        return f"Suggestion pour {self.mot.mot_hassaniya} - {self.variation_generee}"

    class Meta:
        verbose_name = 'Suggestion de mot'
        verbose_name_plural = 'Suggestions de mots'