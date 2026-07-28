# Projet de Prédiction de Coût de Terrain au m²

Ce projet implémente l'ensemble du pipeline de science des données pour traiter, analyser et prédire le prix d'un terrain à Madagascar (centré sur Antananarivo).

## Structure du projet

Cette arborescence professionnelle garantit la bonne séparation des processus de test, traitement, et modèles :

```
vidina_tany/
│
├── data/
│   ├── raw/                 # Données brutes (ex: téléchargées via Facebook)
│   └── processed/           # Données nettoyées (valeurs nulles gérées, etc.)
│
├── models/                  # Modèles Machine Learning sauvegardés (joblib)
│
├── reports/                 # Rapports, figures et résultats du projet
│
├── src/                     # Code source
│   ├── generate_data.py     # Script pour générer un dataset factice semblable aux cas réels
│   ├── train.py             # Pipeline d'analyse, traitement et entraînement du modèle
│   └── app.py               # Interface interactive SIG avec Streamlit pour la prédiction
│
├── requirements.txt         # Dépendances du projet
└── README.md
```

## Technologies Utilisées

- **Python 3** : Langage de base principal.
- **Pandas & NumPy** : Exploration, nettoyage des données, statistiques descriptives (moyenne, quantiles, etc.).
- **Scikit-Learn** : Algorithme prédictif (RandomForestRegressor), séparation test/entrainement, encodage catégorique, RMSE/R2 score.
- **Joblib** : Sauvegarde des ressources entraînés (Modèle, encodeurs de variables texte comme les Communes).
- **Streamlit** : Interface utilisateur web intuitive en Python pour valider et insérer les données.
- **Folium & Streamlit-Folium** : Technologies web SIG (Systèmes d'Informations Géographiques) pour afficher la carte d'Antananarivo d'où on peut définir les coordonnées et la commune.

## Étape par Étape

### 1. Préparation de l'environnement
Activez votre environnement virtuel et installez les dépendances nécessaires.
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Générer (ou insérer) les données (.csv)
Puisque les données sont initialement collectées "via Facebook", un script est présent pour initier et représenter l'acquisition de ces données (7 colonnes).
```bash
python src/generate_data.py
```

### 3. Pipeline d'Analyse (Entrainement)
Ce script lance tout le cycle analytique :
- Lecture & Exploration structurelle
- Statistiques descriptives
- Nettoyage des valeurs manquantes et aberrantes
- Transformation des attributs text (Commune, etc.) en valeurs numériques
- Entraînement et sauvegarde du modèle via Joblib.

```bash
python src/train.py
```

### 4. Interface Interactive & SIG
Démarrez l'application logicielle où vous cliquerez sur la carte puis saisirez la distance JIRAMA, la parcelle, le type d'accès etc.. pour obtenir la prédiction.

```bash
streamlit run src/app.py
```
