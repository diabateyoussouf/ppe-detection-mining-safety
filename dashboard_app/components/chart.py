import plotly.graph_objects as go
import streamlit as st

def render_chart(store):
    # Préparation des données en français
    categories = ["Personnel", "Casques", "Gilets", "Risque (%)"]
    valeurs = [
        store["personnel"],
        store["helmet"],
        store["vest"],
        store["risk"]
    ]
    
    fig = go.Figure()

    fig.add_bar(
        x=categories,
        y=valeurs,
        marker_color=[
            "#29B6F6",  # Bleu clair - Personnel
            "#66BB6A",  # Vert - Casques
            "#FFA726",  # Orange - Gilets
            "#EF5350"   # Rouge - Risque
        ],
        text=valeurs,            # Affiche la valeur directement sur/au-dessus de la barre
        textposition='auto',
        textfont=dict(color='white', weight='bold')
    )

    fig.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False,
        paper_bgcolor="#161b22",
        plot_bgcolor="#161b22",
        font_color="white",
        xaxis=dict(
            gridcolor="rgba(0,0,0,0)", # Pas de grille verticale
            tickfont=dict(size=13, weight='bold')
        ),
        yaxis=dict(
            gridcolor="#2d333b",       # Grille horizontale assortie au thème sombre
            zerolinecolor="#2d333b"
        )
    )

    # st.plotly_chart avec suppression de la barre d'outils flottante parasite
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={'displayModeBar': False}
    )