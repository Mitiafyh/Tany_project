import streamlit as st
import pandas as pd
import joblib
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

st.set_page_config(page_title="Prédiction Prix Terrain", layout="wide")

st.title("Prédiction du Coût du Terrain au m²")

# Load models and encoders
try:
    model = joblib.load('models/model_prix_terrain.joblib')
    le_acces = joblib.load('models/le_type_acces.joblib')
    le_papier = joblib.load('models/le_type_papier.joblib')
    le_commune = joblib.load('models/le_commune.joblib')
except FileNotFoundError:
    st.error("Modèle non trouvé. Veuillez d'abord exécuter `python src/train.py`.")
    st.stop()

col1, col2 = st.columns([1, 1])

# Initialiser le geocoder
geolocator = Nominatim(user_agent="terrain_app")

# Interactive map in column 1
with col1:
    st.subheader("1. Localisation (SIG)")
    
    # Centre of Antananarivo
    m = folium.Map(location=[-18.8792, 47.5079], zoom_start=12)
    m.add_child(folium.LatLngPopup())
    
    map_data = st_folium(m, width=700, height=400)
    
    commune_detectee = "Non détectée (Veuillez cliquer sur la carte)"
    
    if map_data and map_data.get("last_clicked"):
        lat = map_data["last_clicked"]["lat"]
        lng = map_data["last_clicked"]["lng"]
        try:
            location = geolocator.reverse((lat, lng), exactly_one=True)
            if location and location.raw.get("address"):
                address = location.raw["address"]
                # Chercher ville/commune/suburb
                commune_detectee = address.get("city", address.get("town", address.get("village", address.get("suburb", "Analakely"))))
            else:
                commune_detectee = "Analakely" # default if not found
        except:
            commune_detectee = "Analakely" # fallback
            
    # S'assurer que la commune est dans la liste connue, sinon prendre une par défaut
    if commune_detectee not in le_commune.classes_:
        # Just a small trick to have a valid commune for the model
        valid_commune = "Analakely" # fallback
    else:
        valid_commune = commune_detectee

# Input form in column 2
with col2:
    st.subheader("2. Caractéristiques du terrain")
    
    st.text_input("Commune détectée automatiqument :", value=commune_detectee, disabled=True)
    
    type_acces = st.selectbox("Type d'accès :", le_acces.classes_)
    distance_rn = st.number_input("Distance / Route Nationale (en mètres) :", min_value=0.0, value=500.0)
    batissable = st.radio("Le terrain est-il bâtissable ?", ["Oui", "Non"])
    distance_jirama = st.number_input("Distance / Poteau JIRAMA (en mètres) :", min_value=0.0, value=100.0)
    type_papier = st.selectbox("Type de papier :", le_papier.classes_)
    
    if st.button("Prédire le prix au m²", type="primary"):
        # Formatting inputs for prediction
        input_data = pd.DataFrame({
            'type_acces': [le_acces.transform([type_acces])[0]],
            'distance_rn': [distance_rn],
            'batissable': [1 if batissable == "Oui" else 0],
            'distance_jirama': [distance_jirama],
            'type_papier': [le_papier.transform([type_papier])[0]],
            'commune': [le_commune.transform([valid_commune])[0]]
        })
        
        # Prediction
        prediction = model.predict(input_data)[0]
        
        st.success(f"### Estimation : **{prediction:,.2f} Ariary / m²**")
        
st.divider()
