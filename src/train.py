import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

def run_pipeline():
    print("=== 1. Lecture des données (via Facebook) ===")
    try:
        df = pd.read_csv('data/raw/donnees_facebook.csv')
    except FileNotFoundError:
        print("Erreur: Le fichier 'data/raw/donnees_facebook.csv' est introuvable.")
        print("Veuillez télécharger les données sur Facebook et les placer sous ce nom.")
        return
    
    print("\n=== 2. Exploration des données ===")
    print(f"Nombre de lignes : {df.shape[0]}, Nombre de colonnes : {df.shape[1]}")
    print("\nAperçu des colonnes :")
    print(df.columns.tolist())
    
    print("\n=== 3. Statistiques descriptives ===")
    print(df.describe())
    
    # Nettoyage
    print("\n=== 4. Nettoyage : Valeurs manquantes ===")
    print(df.isnull().sum())
    # Remplacer par la médiane
    df['distance_rn'] = df['distance_rn'].fillna(df['distance_rn'].median())
    df['distance_jirama'] = df['distance_jirama'].fillna(df['distance_jirama'].median())
    
    print("\n=== 5. Nettoyage : Suppression des valeurs aberrantes (Outliers) ===")
    # Utilisation de la méthode de l'intervalle interquartile (IQR) pour prix_m2
    Q1 = df['prix_m2'].quantile(0.25)
    Q3 = df['prix_m2'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    pre_outliers_count = len(df)
    df = df[(df['prix_m2'] >= lower_bound) & (df['prix_m2'] <= upper_bound)]
    print(f"Lignes supprimées (outliers) : {pre_outliers_count - len(df)}")
    
    # Enregistrer les données nettoyées
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/terrains_cleaned.csv', index=False)
    
    print("\n=== 6. Encodage des valeurs catégorielles ===")
    # Encodage Label (On pourrait utiliser OneHot, mais LabelEncoder est simple)
    le_dict = {}
    categorical_cols = ['type_acces', 'type_papier', 'commune']
    
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        le_dict[col] = le
        # Sauvegarde de l'encodeur
        joblib.dump(le, f'models/le_{col}.joblib')
        
    print("\nCorrélations avec le prix :")
    print(df.corr()['prix_m2'].sort_values(ascending=False))
    
    print("\n=== 7. Répartition Test / Entraînement ===")
    X = df.drop('prix_m2', axis=1)
    y = df['prix_m2']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"X_train shape: {X_train.shape}, X_test shape: {X_test.shape}")
    
    print("\n=== 8. Modélisation et Entraînement ===")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    print("\n=== 9. Test et Évaluation ===")
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"Root Mean Squared Error (RMSE): {np.sqrt(mse):.2f}")
    print(f"R2 Score: {r2:.2f}")
    
    print("\n=== 10. Sauvegarde du modèle ===")
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/model_prix_terrain.joblib')
    print("Modèle sauvegardé dans 'models/model_prix_terrain.joblib'")
    
if __name__ == "__main__":
    run_pipeline()
