# ============================================
# PROJET : Simulation des objets matriciels
# Membres du groupe :
# - [Prénom NOM 1]
# - [Prénom NOM 2]
# ============================================

import streamlit as st
from home import show_home
from floquet import show_floquet
from bbr import show_bbr
from rachidi import show_rachidi

# PAGE CONFIG
st.set_page_config(
    
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS simplifié
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main-title { text-align: center; font-size: 2rem; font-weight: 800; margin-bottom: 0.2rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title"></div>', unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("### Simulation Suite")
    sim_choice = st.radio(
        "Module",
        [" Accueil", "Floquet", " BBR", "⚡ Rachidi"]
    )
    st.markdown("---")
    st.caption("Heijman & von Mouche (2015) · BBR (2021) · Rachidi (2025)")

# ROUTING
if sim_choice == " Accueil":
    show_home()
elif "Floquet" in sim_choice:
    show_floquet()
elif "BBR" in sim_choice:
    show_bbr()
else:
    show_rachidi()

# Footer
st.markdown("---")
st.markdown("*Floquet Theory Suite — Heijman & von Mouche (2015) • BBR (2021) • Rachidi (2025)*")