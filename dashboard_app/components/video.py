import streamlit as st

def render_video(video_url):
    html = f"""
    <div style="
        border:1px solid #2d333b;
        border-radius:8px;
        overflow:hidden;
        background:#000000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    ">
        <img src="{video_url}"
             style="
                width:100%;
                max-height:420px;
                display:block;
                object-fit:contain;
             "
             alt="Flux vidéo indisponible (Vérifiez la connexion de l'iPhone)">
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)