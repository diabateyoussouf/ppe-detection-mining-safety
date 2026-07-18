CSS = """
<style>

/* Fond principal très sombre, typique des salles de contrôle */
.stApp {
    background-color: #0d1117;
    color: #c9d1d9;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Nettoyage de l'interface par défaut de Streamlit */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Rapproche le contenu du haut de l'écran */
.block-container {
    padding-top: 2rem !important;
}

/* Sidebar noire avec bordure subtile */
[data-testid="stSidebar"] {
    background-color: #010409 !important;
    border-right: 1px solid #30363d;
}

/* Style des icônes du menu latéral */
.sidebar-icon {
    text-align: center;
    font-size: 24px;
    margin-top: 35px;
    color: #8b949e;
    transition: 0.2s;
    cursor: default;
}
.sidebar-icon:hover {
    color: #ffffff;
    transform: scale(1.1);
}

/* Titre principal : ajout d'une ligne de séparation en dessous */
.main-title {
    font-size: 26px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 25px;
    padding-bottom: 15px;
    border-bottom: 1px solid #30363d;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* Titres au-dessus du graphique, de la vidéo et des logs */
.section-title {
    font-size: 14px;
    color: #8b949e;
    font-weight: bold;
    margin-bottom: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Amélioration de la bannière d'alerte */
.alert-banner {
    background-color: #2b1414;
    border-top: 2px solid #ff4b4b;
    border-left: 1px solid #ff4b4b;
    border-right: 1px solid #ff4b4b;
    border-bottom: 1px solid #ff4b4b;
    color: #ff4b4b;
    padding: 12px;
    border-radius: 4px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0px 4px 10px rgba(255, 75, 75, 0.05);
}

/* Personnalisation de la scrollbar pour les logs */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: #0d1117;
}
::-webkit-scrollbar-thumb {
    background: #30363d;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #8b949e;
}

</style>
"""