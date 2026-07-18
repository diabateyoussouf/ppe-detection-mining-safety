import streamlit as st
import streamlit.components.v1 as components
import time

from data_store import init_store
from mqtt_client import start_mqtt
from styles import CSS
from config import VIDEO_URL

from components.kpi import render_kpi
from components.chart import render_chart
from components.video import render_video
from components.logs import render_logs

# Configuration de la page
st.set_page_config(
    page_title="Mining Safety Monitor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injection du CSS
st.markdown(CSS, unsafe_allow_html=True)

@st.cache_resource
def get_store():
    return init_store()

store = get_store()

@st.cache_resource
def start():
    return start_mqtt(store)

start()

# Sidebar stylisée
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>⛏️</h2>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-icon'>🏠</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-icon'>👷</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-icon'>🎥</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-icon'>📊</div>", unsafe_allow_html=True)

# Titre principal
st.markdown("<div class='main-title'>⛏️ Moniteur de sécurité minière</div>", unsafe_allow_html=True)

# Conteneurs de mise en page
kpi_container = st.empty()
st.markdown("<br>", unsafe_allow_html=True) 

left, right = st.columns([1, 1.8])

with left:
    st.markdown("<div class='section-title'>Performances & Alertes</div>", unsafe_allow_html=True)
    chart_container = st.empty()

with right:
    st.markdown("<div class='section-title'>Zone Nord - Cam 3</div>", unsafe_allow_html=True)
    render_video(VIDEO_URL)
    
    st.markdown("<div class='section-title' style='margin-top: 20px;'>📋 Journal des événements en temps réel</div>", unsafe_allow_html=True)
    logs_container = st.empty()

# Le conteneur audio doit être persistant en bas de page
audio_container = st.empty()

# --- GESTION DE LA SIRÈNE REVISITÉE (SANS IFRAME) ---
def trigger_audio_alert(store, container):
    if store.get("alert", False):
        # Si c'est le début d'une alerte ou si on change d'état de danger
        if not st.session_state.get("siren_active", False):
            st.session_state.siren_active = True
            
            # Utilisation d'un timestamp pour forcer le navigateur à recharger la balise
            id_unique = int(time.time())
            
            # Balise HTML5 native directe avec autoplay, cachée visuellement
            audio_html = f"""
                <audio autoplay key="{id_unique}" style="display:none;">
                    <source src="https://assets.mixkit.co/active_storage/sfx/995/995-preview.mp3" type="audio/mpeg">
                </audio>
            """
            # Rendu direct dans le conteneur sans passer par components.html
            container.markdown(audio_html, unsafe_allow_html=True)
    else:
        # Réinitialisation propre dès que l'environnement redevient SAFE
        st.session_state.siren_active = False
        container.empty()

# --- BOUCLE DE RAFRAÎCHISSEMENT FRACTIONNÉE ---
@st.fragment(run_every=1.5)
def refresh_dynamic_data():
    with kpi_container.container():
        render_kpi(store)
        
    with chart_container.container():
        render_chart(store)
        
    with logs_container.container():
        render_logs(store)
        
    # Exécution de l'alerte sonore
    trigger_audio_alert(store, audio_container)

# Lancement automatique
refresh_dynamic_data()