from django.shortcuts import render
from .nlp_model import process_word
import os

# Définir le chemin du modèle NLP sauvegardé
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'data', 'nlp_model.pkl')

def transform_word(request):
    query = request.GET.get('mot', '')  # Récupère le mot saisi dans le formulaire
    print(f"Mot saisi : {query}")  # Vérifiez que le mot est bien récupéré
    
    result = None  # Initialisation de la variable result
    
    if query:  # Si un mot est saisi
        result = process_word(query, MODEL_PATH)  # Traiter le mot pour obtenir les informations
    
    return render(request, 'traduction.html', {'result': result, 'query': query, 'model_path': MODEL_PATH})
