import streamlit as st

def render_kpi(store):
    c1, c2, c3, c4 = st.columns(4)

    # Traduction en français et alignement avec les variables globales
    c1.metric(label="👷 Personnel Détecté", value=int(store["personnel"]))
    c2.metric(label="🪖 Casques Conformes", value=int(store["helmet"]))
    c3.metric(label="🦺 Gilets Conformes", value=int(store["vest"]))
    
    # Formatage dynamique du risque avec son unité de pourcentage
    c4.metric(label="🚨 Niveau de Risque", value=f"{int(store['risk'])} %")