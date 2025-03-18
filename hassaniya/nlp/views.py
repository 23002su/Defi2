import pickle
import os
from django.shortcuts import render
from .nlp_model import process_word  # Assurez-vous d'importer la fonction pour traiter les mots

# Définition du chemin du fichier nlp_model.pkl
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'data/nlp_model.pkl')
def transform_word(request):
    query = request.GET.get('mot', '').strip()  # Récupérer le mot entré dans l'input

    result = None  # Initialisation du résultat
    
    if query:  # Si un mot a été saisi
        result = process_word(query, MODEL_PATH)  # Appeler la fonction pour obtenir les résultats à partir du modèle NLP
        
        # Ajout de logging pour déboguer
        print(f"Query: {query}")
        print(f"Result: {result}")

    # Envoyer les données au template
    return render(request, 'traduction.html', {'query': query, 'result': result})

