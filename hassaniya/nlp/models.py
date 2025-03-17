from django.db import models

class HassaniyaWord(models.Model):
    mot = models.CharField(max_length=255, unique=True, verbose_name="Mot Hassaniya")
    traduction_arabe = models.TextField(blank=True, null=True, verbose_name="Traduction en Arabe")
    traduction_francais = models.TextField(blank=True, null=True, verbose_name="Traduction en Français")
    derives = models.TextField(blank=True, null=True, verbose_name="Dérivés")
    grammaire = models.TextField(blank=True, null=True, verbose_name="Grammaire")
    
    def __str__(self):
        return self.mot
