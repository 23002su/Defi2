import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

def load_data(excel_path):
    df = pd.read_excel(excel_path, dtype=str)
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

def train_model(df, model_path):
    corpus = df.apply(lambda row: f"{row['mot_hassaniya']} {row['traduction_arabe']} {row['traduction_francais']} {' '.join(row['derivations'])}", axis=1).tolist()
    
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    
    knn = NearestNeighbors(n_neighbors=5, metric='cosine')
    knn.fit(X)
    
    joblib.dump((vectorizer, knn, df), model_path)

def process_word(query, model_path):
    vectorizer, knn, df = joblib.load(model_path)
    query_vector = vectorizer.transform([query])
    distances, indices = knn.kneighbors(query_vector)
    
    if len(indices[0]) > 0:
        suggested_row = df.iloc[indices[0][0]]
        result = {
            'mot_hassaniya': suggested_row['mot_hassaniya'],
            'traduction_arabe': suggested_row['traduction_arabe'],
            'traduction_francais': suggested_row['traduction_francais'],
            'derivations': suggested_row['derivations'],
            'grammar': suggested_row['grammar']
        }
        return result
    else:
        return None
