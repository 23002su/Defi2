import pandas as pd
import json

# Liste des mots en Hassaniya avec leurs traductions, dérivations et grammaire
hassaniya_words = [
    ("تفو", "كلمة تعبر عن الكره", "Expression de dégoût", ["تفوت", "متفو"], "اسم"),
    ("ازمد", "يموت", "Mourir", ["مات", "يموت", "وفاة"], "فعل"),
    ("غمظ", "يركد", "Se calmer", ["ركد", "يغمض", "هدأ"], "فعل"),
    ("اطرح", "اترك", "Laisser", ["ترك", "يترك", "اترك"], "فعل"),
    ("اتاي", "الشاي", "Thé", ["شاي", "أتاي", "مشروب ساخن"], "اسم"),
    ("يحركبوك", "التوبيخ", "Réprimander", ["وبخ", "لوم", "انتقاد"], "فعل"),
    ("يخزيك", "للعن", "Maudire", ["لعنة", "سب", "شتم"], "فعل"),
    ("امالك", "كيف / ماذا أشعر", "Comment / Que ressens-tu", ["كيف", "حالة", "شعور"], "أداة استفهام"),
    ("تتختير", "ماذا أريد", "Que veux-tu", ["اختيار", "رغبة", "قرار"], "أداة استفهام"),
    ("إزريك", "شيء يشرب", "Quelque chose à boire", ["شراب", "مشروب", "سائل"], "اسم"),
    ("البكرة", "البقرة", "Vache", ["بقر", "عجل", "ماشية"], "اسم"),
    ("المغرج", "البوش", "Bétail", ["إبل", "جمل", "بوش"], "اسم"),
    ("خيرت", "أهلاً / مرحباً", "Bienvenue", ["تحية", "استقبال", "مرحبًا"], "اسم"),
    ("ورخست", "كلمة تعبر عن الكره", "Expression de mépris", ["كره", "احتقار", "ازدراء"], "اسم"),
    ("يلالكيان", "التعاطف", "Empathie", ["تعاطف", "مواساة", "تفهم"], "اسم"),
    ("ماسخ", "غير لذيذ", "Pas bon", ["غير شهي", "ليس لذيذًا", "طعم سيء"], "صفة"),
    ("اكند", "كثير الحلاوة", "Très sucré", ["سكر", "حلو", "لذيذ"], "صفة"),
]

# Sauvegarde les mots dans un fichier Excel
def save_to_excel(words, excel_path):
    df = pd.DataFrame(words, columns=["mot_hassaniya", "traduction_arabe", "traduction_francais", "derivations", "grammar"])
    df.to_excel(excel_path, index=False)

# Charger le fichier Excel
def load_data(excel_path):
    df = pd.read_excel(excel_path)
    
    # Vérifier que les colonnes attendues existent
    expected_columns = ['mot_hassaniya', 'traduction_arabe', 'traduction_francais', 'derivations', 'grammar']
    for col in expected_columns:
        if col not in df.columns:
            raise ValueError(f"Colonne manquante dans le fichier Excel : {col}")
    
    # Transformer les données en dictionnaire
    data = []
    for _, row in df.iterrows():
        derivations = row["derivations"]
        
        # Vérifier si la colonne "derivations" contient une valeur valide
        if pd.notna(derivations):
            try:
                derivations = json.loads(derivations)  # Tentative de décodage JSON
            except json.JSONDecodeError:
                derivations = []  # En cas d'erreur, on attribue une liste vide
        else:
            derivations = []  # Si la cellule est vide, on utilise une liste vide
        
        entry = {
            "mot_hassaniya": row["mot_hassaniya"],
            "traduction_arabe": row["traduction_arabe"],
            "traduction_francais": row["traduction_francais"],
            "derivations": derivations,
            "grammar": row["grammar"] if pd.notna(row["grammar"]) else "",
        }
        data.append(entry)
    
    return data

# Sauvegarde les données sous forme de JSON
def save_json(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    excel_path = "data/dictionnaire_hassaniya.xlsx"
    output_path = "data/hassaniya_data.json"
    
    # Sauvegarder la liste des mots dans un fichier Excel
    save_to_excel(hassaniya_words, excel_path)
    
    # Charger et sauvegarder en JSON
    data = load_data(excel_path)
    save_json(data, output_path)
    print("Données extraites et sauvegardées avec succès !")
