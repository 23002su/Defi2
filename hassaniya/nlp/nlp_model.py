import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import joblib


def load_data(excel_path):
    df = pd.read_excel(excel_path, dtype=str)
    print(df.head())  # Affiche les premières lignes pour vérifier
    expected_columns = ['mot_hassaniya', 'traduction_arabe', 'traduction_francais', 'derivations', 'grammar']
    
    for col in expected_columns:
        if col not in df.columns:
            raise ValueError(f"Colonne manquante dans le fichier Excel : {col}")
    
    def parse_derivations(value):
        if pd.notna(value) and isinstance(value, str):
            value = value.strip()
            if value.startswith("[") and value.endswith("]"):
                try:
                    return eval(value)
                except (SyntaxError, NameError):
                    return []
        return []

    df['derivations'] = df['derivations'].apply(parse_derivations)
    return df

# # Charger les données depuis le fichier Excel
# def load_data(excel_path):
#     df = pd.read_excel(excel_path, dtype=str)  # Charger tout en string pour éviter les erreurs
#     expected_columns = ['mot_hassaniya', 'traduction_arabe', 'traduction_francais', 'derivations', 'grammar']
    
#     for col in expected_columns:
#         if col not in df.columns:
#             raise ValueError(f"Colonne manquante dans le fichier Excel : {col}")
    
#     # Correction du chargement des dérivations
#     def parse_derivations(value):
#         if pd.notna(value) and isinstance(value, str):
#             value = value.strip()
#             if value.startswith("[") and value.endswith("]"):  # Vérifie si c'est une liste
#                 try:
#                     return eval(value)  # Utiliser eval pour interpréter comme liste Python
#                 except (SyntaxError, NameError):
#                     return []  # Si erreur, renvoyer une liste vide
#         return []

#     df['derivations'] = df['derivations'].apply(parse_derivations)
    
#     return df

# Entraîner un modèle NLP pour la recherche de mots similaires
def train_model(df, model_path):
    corpus = df.apply(lambda row: f"{row['mot_hassaniya']} {row['traduction_arabe']} {row['traduction_francais']} {' '.join(row['derivations'])}", axis=1).tolist()
    
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    
    knn = NearestNeighbors(n_neighbors=5, metric='cosine')
    knn.fit(X)
    
    joblib.dump((vectorizer, knn, df), model_path)
    print("Modèle NLP entraîné et sauvegardé avec succès !")

# Charger et utiliser le modèle NLP pour suggérer des mots similaires
# def suggest_words(query, model_path):
#     vectorizer, knn, df = joblib.load(model_path)
#     query_vector = vectorizer.transform([query])
#     distances, indices = knn.kneighbors(query_vector)

#     suggestions = df.iloc[indices[0]]['mot_hassaniya'].tolist()
#     return suggestions
def suggest_words(query, model_path):
    vectorizer, knn, df = joblib.load(model_path)
    print(df.head())  # Affiche les 5 premières lignes du DataFrame pour vérifier les données
    query_vector = vectorizer.transform([query])
    distances, indices = knn.kneighbors(query_vector)

    # Récupérer seulement le mot Hassaniya des suggestions
    suggestions = df.iloc[indices[0]]['mot_hassaniya'].tolist()
    return suggestions
# def process_word(query, model_path):
#     vectorizer, knn, df = joblib.load(model_path)
    
#     # Trouver les indices des mots similaires
#     query_vector = vectorizer.transform([query])
#     distances, indices = knn.kneighbors(query_vector)
    
#     # Obtenez les résultats pour le mot suggéré
#     suggested_row = df.iloc[indices[0][0]]  # On prend le mot le plus proche trouvé
    
#     # Renvoi des informations pour le mot suggéré
#     result = {
#         'mot_hassaniya': suggested_row['mot_hassaniya'],
#         'traduction_arabe': suggested_row['traduction_arabe'],
#         'traduction_francais': suggested_row['traduction_francais'],
#         'derivations': suggested_row['derivations'],
#         'grammar': suggested_row['grammar']
#     }
    
#     return result
def process_word(query, model_path):
    vectorizer, knn, df = joblib.load(model_path)
    
    print(f"Recherche pour le mot : {query}")  # Affiche le mot saisi
    query_vector = vectorizer.transform([query])
    distances, indices = knn.kneighbors(query_vector)
    
    # Vérifier si les indices retournés sont valides
    print(f"Indices retournés : {indices}")
    
    if len(indices[0]) > 0:
        suggested_row = df.iloc[indices[0][0]]  # Prendre le mot le plus proche
        print(f"Suggéré : {suggested_row['mot_hassaniya']}")  # Affiche le mot suggéré
        result = {
            'mot_hassaniya': suggested_row['mot_hassaniya'],
            'traduction_arabe': suggested_row['traduction_arabe'],
            'traduction_francais': suggested_row['traduction_francais'],
            'derivations': suggested_row['derivations'],
            'grammar': suggested_row['grammar']
        }
        return result
    else:
        print("Aucun mot similaire trouvé.")  # Affiche un message si aucun mot similaire n'est trouvé
        return None

if __name__ == "__main__":
    excel_path = "data/dictionnaire_hassaniya.xlsx"
    model_path = "data/nlp_model.pkl"
    
    df = load_data(excel_path)
    train_model(df, model_path)
    
    # Test de suggestion
    query = "يموت"
    suggestions = suggest_words(query, model_path)
    print("Suggestions de mots :", suggestions)

