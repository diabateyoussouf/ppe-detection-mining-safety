import streamlit as st

def render_logs(store):
    logs_html = ""

    for log in store["logs"]:
        # Couleurs fluides adaptées au thème sombre
        color = "#3fb950" if log["status"] == "SAFE" else "#f85149"
        icon = "✅" if log["status"] == "SAFE" else "⚠️"
        bg_color = "rgba(63, 185, 80, 0.05)" if log["status"] == "SAFE" else "rgba(248, 81, 73, 0.05)"

        logs_html += f"""
<div style="background:{bg_color}; border-left:4px solid {color}; margin-bottom:8px; padding:12px; border-radius:6px; border-top: 1px solid rgba(255,255,255,0.02);">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="color:#8b949e; font-family:monospace; font-size:12px;">⏰ {log['time']}</span>
        <span style="color:{color}; font-weight:bold; font-size:13px; letter-spacing:0.5px;">{icon} {log['status']}</span>
    </div>
    <div style="color:#c9d1d9; margin-top:6px; font-size:14px; font-weight:500;">{log['message']}</div>
</div>
"""

    # Rendu du conteneur parent avec barres de défilement stylisées (overflow-y)
    st.markdown(
        f"""
<div style="background:#161b22; border:1px solid #2d333b; border-radius:8px; padding:15px; max-height:335px; overflow-y:auto; box-shadow: inset 0 0 10px rgba(0,0,0,0.5);">
    {logs_html if logs_html else '<div style="color:#8b949e; text-align:center; padding:20px;">Aucun événement enregistré</div>'}
</div>
        """,
        unsafe_allow_html=True
    )