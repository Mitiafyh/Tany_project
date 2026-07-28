import pandas as pd
import numpy as np
import os

def generate_data(num_records=500):
    np.random.seed(42)
    
    types_acces = ['sans acces', 'acces moto', 'acces voiture']
    papiers = ['titre et borne', 'cadastre', 'fifanolorana']
    communes = ['Analakely', 'Ambohidratrimo', 'Ilafy', 'Alasora', 'Ivato', 'Tanjombato']
    
    data = {
        'type_acces': np.random.choice(types_acces, num_records, p=[0.2, 0.3, 0.5]),
        'distance_rn': np.abs(np.random.normal(5000, 3000, num_records)), # en metres
        'batissable': np.random.choice([0, 1], num_records, p=[0.1, 0.9]),
        'distance_jirama': np.abs(np.random.normal(1000, 800, num_records)), # en metres
        'type_papier': np.random.choice(papiers, num_records, p=[0.5, 0.3, 0.2]),
        'commune': np.random.choice(communes, num_records),
    }
    
    df = pd.DataFrame(data)
    
    # mitady anle valeur manquante amin'ny distance_rn sy distance_jirama
    df.loc[np.random.choice(df.index, 10), 'distance_rn'] = np.nan
    df.loc[np.random.choice(df.index, 10), 'distance_jirama'] = np.nan
    
    # Base price calculation based on features
    base_price = 50000 # 50,000 Ariary base
    
    # Pricing logic
    df['prix_m2'] = base_price
    df.loc[df['type_acces'] == 'acces voiture', 'prix_m2'] += 100000
    df.loc[df['type_acces'] == 'acces moto', 'prix_m2'] += 40000
    df.loc[df['type_papier'] == 'titre et borne', 'prix_m2'] += 150000
    df.loc[df['type_papier'] == 'cadastre', 'prix_m2'] += 50000
    df.loc[df['batissable'] == 1, 'prix_m2'] += 80000
    
    # Proximity premium
    df['prix_m2'] -= (df['distance_rn'] * 5)
    df['prix_m2'] -= (df['distance_jirama'] * 10)
    
    # Add noise & outliers
    df['prix_m2'] += np.random.normal(0, 15000, num_records)
    df.loc[np.random.choice(df.index, 5), 'prix_m2'] = df['prix_m2'] * 5 # Outliers
    
    df['prix_m2'] = np.abs(df['prix_m2']).round(2)
    
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv('data/raw/terrains_antananarivo.csv', index=False)
    print("Données brutes générées dans data/raw/terrains_antananarivo.csv")

if __name__ == "__main__":
    generate_data()
