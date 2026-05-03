# ============================================================
# APPLICATION STREAMLIT - Simulation des objets matriciels
# Version épurée - design clair, texte simple, impact visuel
# Compatible Dark Mode
# ============================================================

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from scipy import sparse
import base64

# ── Configuration de la page ─────────────────────────────────
st.set_page_config(
    page_title="Matrices - Projet Math",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS adaptatif pour Dark Mode ────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Dark mode detection */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --border: #334155;
            --card-bg: #1e293b;
            --card-hover: #334155;
            --metric-bg: #0f172a;
            --info-bg: #1e293b;
            --info-border: #3b82f6;
        }
    }
    
    /* Light mode */
    @media (prefers-color-scheme: light) {
        :root {
            --bg-primary: #f8fafc;
            --bg-secondary: #ffffff;
            --text-primary: #0f172a;
            --text-secondary: #64748b;
            --border: #e2e8f0;
            --card-bg: #ffffff;
            --card-hover: #f1f5f9;
            --metric-bg: #ffffff;
            --info-bg: #f1f5f9;
            --info-border: #3b82f6;
        }
    }
    
    .stApp {
        background: var(--bg-primary);
    }
    
    .card {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid var(--border);
        transition: all 0.2s ease;
        color: var(--text-primary);
    }
    
    .card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transform: translateY(-2px);
        background: var(--card-hover);
    }
    
    .metric {
        background: var(--metric-bg);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border: 1px solid var(--border);
        color: var(--text-primary);
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* BOUTONS CORRIGÉS - Toujours visibles (bleu avec texte blanc) */
    .stButton > button {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background-color: #2563eb !important;
        transform: translateY(-1px);
    }
    
    h1 {
        font-size: 2rem !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    h3, h4, h5, h6, p, label, .stMarkdown {
        color: var(--text-primary);
    }
    
    [data-testid="stSidebar"] {
        background: var(--bg-secondary);
        border-right: 1px solid var(--border);
    }
    
    [data-testid="stSidebar"] * {
        color: var(--text-primary);
    }
    
    .info-box {
        background: var(--info-bg);
        border-left: 3px solid var(--info-border);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: var(--text-primary);
    }
    
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 1px solid var(--border);
    }
    
    .stDataFrame, .dataframe {
        background: var(--card-bg) !important;
    }
    
    .stSelectSlider label, .stSlider label, .stCheckbox label {
        color: var(--text-primary) !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: var(--card-bg);
        border-radius: 8px;
        padding: 8px 16px;
        color: var(--text-primary);
        border: 1px solid var(--border);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--info-border) !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Fonctions utilitaires ───────────────────────────────────
@st.cache_data(ttl=3600)
def calcul_inversion(n, stabiliser):
    """Calcule l'inverse d'une matrice aléatoire"""
    A = np.random.rand(n, n)
    if stabiliser:
        A += n * np.eye(n)
    start = time.time()
    A_inv = np.linalg.inv(A)
    temps = time.time() - start
    erreur = np.linalg.norm(A @ A_inv - np.eye(n))
    return A, A_inv, temps, erreur

# Fonction pour adapter les couleurs Plotly selon le thème
def get_plotly_template():
    """Retourne un template Plotly adapté au thème"""
    # Détection du thème Streamlit
    try:
        theme = st.get_option("theme.base")
        if theme == "dark":
            return "plotly_dark"
    except:
        pass
    return "plotly_white"

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-size: 2rem;"></div>
            <div style="font-weight: 600; font-size: 1.2rem;">Matrices</div>
            <div style="font-size: 0.7rem;">projet mathématiques</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["Accueil", "Inversion", "Matrices creuses", "Integration", "Modele de Leslie"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.caption("simulation en temps reel")

# ============================================================
# PAGE ACCUEIL
# ============================================================
if page == "Accueil":
    st.markdown("<h1> Simulation des objets matriciels</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-secondary); margin-bottom: 2rem;'>Exploration interactive des structures matricielles</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
            <div class="card">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;"></div>
                <div style="font-weight: 600;">Objectif du projet</div>
                <div style="color: var(--text-secondary); margin-top: 0.5rem;">
                    Etudier et simuler differents types de matrices utilises en 
                    intelligence artificielle, systemes dynamiques et modelisation des populations.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric">
                <div class="metric-value">4</div>
                <div class="metric-label">taches interactives</div>
                <div style="font-size: 0.7rem; color: var(--text-secondary);">calcul en temps reel</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h2> Les 4 taches du projet</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="card" style="text-align: center;">
                <div style="font-size: 2rem;"></div>
                <div style="font-weight: 600;">Inversion</div>
                <div style="font-size: 0.7rem; color: var(--text-secondary);">complexite O(n³)</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="card" style="text-align: center;">
                <div style="font-size: 2rem;">🕸️</div>
                <div style="font-weight: 600;">Matrices creuses</div>
                <div style="font-size: 0.7rem; color: var(--text-secondary);">gain memoire x100</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="card" style="text-align: center;">
                <div style="font-size: 2rem;">∫</div>
                <div style="font-weight: 600;">Integration</div>
                <div style="font-size: 0.7rem; color: var(--text-secondary);">convergence O(1/N)</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="card" style="text-align: center;">
                <div style="font-size: 2rem;"></div>
                <div style="font-weight: 600;">Modele de Leslie</div>
                <div style="font-size: 0.7rem; color: var(--text-secondary);">valeur propre lambda</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
        <div class="info-box">
            <strong>Comment utiliser l'application</strong><br>
            Utilisez le menu de gauche pour naviguer entre les differentes taches.
            Chaque tache est interactive : modifiez les parametres et observez les resultats en temps reel.
            L'application s'adapte automatiquement à votre thème (clair/sombre).
        </div>
    """, unsafe_allow_html=True)

# ============================================================
# TACHE 1 : INVERSION
# ============================================================
elif page == "Inversion":
    st.markdown("<h1> Inversion de matrices</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-secondary);'>Analyse du temps de calcul et de la precision numerique</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        M = st.select_slider(
            "Taille de la matrice",
            options=[100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
            value=500
        )
    
    with col2:
        stabiliser = st.checkbox("Stabiliser la matrice", value=True)
    
    with col3:
        st.metric("Nombre d'elements", f"{M*M:,}")
    
    if st.button(" Calculer l'inverse", use_container_width=True):
        with st.spinner("Calcul en cours..."):
            A, A_inv, temps, erreur = calcul_inversion(M, stabiliser)
            memoire = A.nbytes / (1024**2)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="metric">
                    <div class="metric-value">{memoire:.2f}</div>
                    <div class="metric-label">memoire (Mo)</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric">
                    <div class="metric-value">{temps:.4f}</div>
                    <div class="metric-label">temps (secondes)</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric">
                    <div class="metric-value">{erreur:.2e}</div>
                    <div class="metric-label">erreur numerique</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            if erreur < 1e-8:
                st.markdown("""
                    <div class="metric">
                        <div class="metric-value">✓ valide</div>
                        <div class="metric-label">precision excellente</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="metric">
                        <div class="metric-value">⚠ limitee</div>
                        <div class="metric-label">verifier conditionnement</div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<h2> Visualisation</h2>", unsafe_allow_html=True)
        
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Matrice originale", "Matrice inverse"))
        
        fig.add_trace(go.Heatmap(z=A[:20, :20], colorscale='Blues', showscale=False), row=1, col=1)
        fig.add_trace(go.Heatmap(z=A_inv[:20, :20], colorscale='Reds', showscale=False), row=1, col=2)
        
        fig.update_layout(height=500, template=get_plotly_template())
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<h2>Extraits numeriques</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Matrice originale (3x3)**")
            st.dataframe(pd.DataFrame(np.round(A[:3, :3], 4)))
        with col2:
            st.markdown("**Matrice inverse (3x3)**")
            st.dataframe(pd.DataFrame(np.round(A_inv[:3, :3], 6)))
    
    st.markdown("---")
    st.markdown("<h2> Etude de complexite</h2>", unsafe_allow_html=True)
    
    if st.button(" Lancer l'etude", use_container_width=True):
        with st.spinner("Calcul en cours..."):
            tailles = [100, 200, 400, 600, 800, 1000]
            temps_list = []
            
            bar = st.progress(0)
            for i, n in enumerate(tailles):
                A = np.random.rand(n, n) + n * np.eye(n)
                start = time.time()
                np.linalg.inv(A)
                temps_list.append(time.time() - start)
                bar.progress((i + 1) / len(tailles))
            bar.empty()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=tailles, y=temps_list,
            mode='markers+lines',
            name='Mesure',
            line=dict(color='#3b82f6', width=2),
            marker=dict(size=8)
        ))
        
        n3 = np.array(tailles)**3
        n3 = n3 / n3[0] * temps_list[0]
        fig.add_trace(go.Scatter(
            x=tailles, y=n3,
            mode='lines',
            name='O(n³) theorique',
            line=dict(color='#f97316', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title="Complexite de l'inversion matricielle",
            xaxis_title="Taille n",
            yaxis_title="Temps (secondes)",
            xaxis_type="log",
            yaxis_type="log",
            template=get_plotly_template(),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
            <div class="info-box">
                <strong> Conclusion</strong><br>
                Le temps d'inversion suit une complexite en O(n³), conforme a la theorie.
                La memoire utilisee croit en O(n²). La precision reste bonne pour ces tailles.
            </div>
        """, unsafe_allow_html=True)

# ============================================================
# TÂCHE 2 : MATRICES CREUSES
# ============================================================
elif page == "Matrices creuses":
    st.markdown("<h1>🕸️ Matrices creuses</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-secondary);'>Optimisation mémoire, phénomène de fill-in et données manquantes</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    tab1, tab2 = st.tabs([" Matrices avec zéros", "❓ Valeurs manquantes (NaN)"])
    
    # ONGLET 1 : MATRICES AVEC ZÉROS
    with tab1:
        st.markdown("### Matrices avec beaucoup de zéros")
        
        col1, col2 = st.columns(2)
        with col1:
            n = st.slider("Taille de la matrice", 100, 2000, 1000, step=100, key="sparse_n")
        with col2:
            densite = st.slider("Densité (%)", 0.1, 5.0, 1.0, step=0.1, key="sparse_densite") / 100
        
        if st.button("🎲 Générer la matrice creuse", key="gen_sparse"):
            with st.spinner("Génération en cours..."):
                A_sparse = sparse.random(n, n, density=densite, format='csr')
                A_dense = A_sparse.toarray()
                
                mem_dense = A_dense.nbytes / (1024**2)
                mem_sparse = (A_sparse.data.nbytes + A_sparse.indices.nbytes + 
                             A_sparse.indptr.nbytes) / (1024**2)
                gain = mem_dense / mem_sparse
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                    <div class="metric">
                        <div class="metric-value">{n} x {n}</div>
                        <div class="metric-label">taille</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class="metric">
                        <div class="metric-value">{A_sparse.nnz:,}</div>
                        <div class="metric-label">éléments non nuls</div>
                        <div style="font-size:0.7rem; color: var(--text-secondary);">densité {densite*100:.2f}%</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div class="metric">
                        <div class="metric-value">x {gain:.0f}</div>
                        <div class="metric-label">gain mémoire</div>
                        <div style="font-size:0.7rem; color: var(--text-secondary);">{mem_sparse:.3f} Mo vs {mem_dense:.2f} Mo</div>
                    </div>
                """, unsafe_allow_html=True)
            
            rows, cols = A_sparse[:50, :50].nonzero()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=cols, y=rows,
                mode='markers',
                marker=dict(size=4, color='#3b82f6'),
                name='valeurs non nulles'
            ))
            
            fig.update_layout(
                title=f"Structure creuse - bloc 50×50 (densité {densite*100:.2f}%)",
                xaxis_title="colonnes",
                yaxis_title="lignes",
                yaxis_autorange="reversed",
                height=500,
                template=get_plotly_template()
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("###  Phénomène de fill-in")
        st.markdown("Lorsqu'on inverse une matrice creuse, elle peut devenir **dense** → perte du gain mémoire !")
        
        if st.button(" Calculer l'inverse et observer le fill-in", key="fillin"):
            with st.spinner("Calcul de l'inverse en cours..."):
                n_fill = 30
                A_fill = sparse.random(n_fill, n_fill, density=0.2, format='csc')
                A_fill = A_fill + sparse.eye(n_fill, format='csc')
                
                nnz_avant = A_fill.nnz
                densite_avant = nnz_avant / (n_fill * n_fill) * 100
                
                A_inv_dense = np.linalg.inv(A_fill.toarray())
                nnz_apres = np.count_nonzero(A_inv_dense)
                densite_apres = nnz_apres / (n_fill * n_fill) * 100
                ratio = densite_apres / densite_avant
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                    <div class="metric">
                        <div class="metric-value">{nnz_avant}</div>
                        <div class="metric-label">éléments non nuls AVANT inversion</div>
                        <div style="font-size:0.7rem; color: var(--text-secondary);">densité {densite_avant:.1f}%</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class="metric">
                        <div class="metric-value">{nnz_apres}</div>
                        <div class="metric-label">éléments non nuls APRÈS inversion</div>
                        <div style="font-size:0.7rem; color: var(--text-secondary);">densité {densite_apres:.1f}%</div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.warning(f"La matrice est devenue **{ratio:.1f}x plus dense** après inversion ! C'est le phénomène de **FILL-IN**.")
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # Adapter les couleurs des graphiques matplotlib
            bg_color = '#1e293b' if st.get_option("theme.base") == "dark" else '#ffffff'
            text_color = '#f1f5f9' if st.get_option("theme.base") == "dark" else '#0f172a'
            
            fig.patch.set_facecolor(bg_color)
            ax1.set_facecolor(bg_color)
            ax2.set_facecolor(bg_color)
            
            ax1.spy(A_fill, markersize=4, color='#3b82f6')
            ax1.set_title(f"Avant inversion\n{nnz_avant} éléments non nuls (densité {densite_avant:.1f}%)", color=text_color)
            ax1.set_xlabel("colonnes", color=text_color)
            ax1.set_ylabel("lignes", color=text_color)
            ax1.tick_params(colors=text_color)
            
            ax2.spy(A_inv_dense, markersize=4, color='#ef4444')
            ax2.set_title(f"Après inversion\n{nnz_apres} éléments non nuls (densité {densite_apres:.1f}%)", color=text_color)
            ax2.set_xlabel("colonnes", color=text_color)
            ax2.set_ylabel("lignes", color=text_color)
            ax2.tick_params(colors=text_color)
            
            plt.suptitle("Phénomène de fill-in : l'inverse devient dense", fontsize=14, fontweight='bold', color=text_color)
            plt.tight_layout()
            st.pyplot(fig)
            
            st.info(" **Conclusion** : L'inverse d'une matrice creuse peut devenir dense. C'est pourquoi on utilise des **solveurs itératifs** (Gradient Conjugué) au lieu de calculer l'inverse directement.")
    
    # ONGLET 2 : VALEURS MANQUANTES
    with tab2:
        st.markdown("### Matrices avec valeurs manquantes (NaN)")
        st.markdown("Exemple : système de recommandation utilisateurs × films")
        
        col1, col2 = st.columns(2)
        with col1:
            n_users = st.slider("Nombre d'utilisateurs", 3, 15, 8, key="users")
        with col2:
            n_films = st.slider("Nombre de films", 3, 12, 10, key="films")
        
        pct_nan = st.slider("Pourcentage de notes manquantes (%)", 20, 90, 65, key="nan_pct")
        
        if st.button(" Générer la matrice de notes", key="gen_notes"):
            np.random.seed(42)
            notes = np.random.randint(1, 6, size=(n_users, n_films)).astype(float)
            mask = np.random.rand(n_users, n_films) < pct_nan / 100
            notes[mask] = np.nan
            
            observes = np.sum(~np.isnan(notes))
            manquants = np.sum(np.isnan(notes))
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                    <div class="metric">
                        <div class="metric-value">{observes}</div>
                        <div class="metric-label">notes observées</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class="metric">
                        <div class="metric-value">{manquants}</div>
                        <div class="metric-label">notes manquantes</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div class="metric">
                        <div class="metric-value">{observes/(n_users*n_films)*100:.1f}%</div>
                        <div class="metric-label">densité</div>
                    </div>
                """, unsafe_allow_html=True)
            
            notes_display = np.where(np.isnan(notes), 0, notes)
            
            fig = go.Figure()
            fig.add_trace(go.Heatmap(
                z=notes_display,
                text=np.where(np.isnan(notes), "NaN", notes.astype(int)),
                texttemplate="%{text}",
                colorscale='Viridis',
                showscale=True,
                hoverongaps=False
            ))
            
            fig.update_layout(
                title="Matrice utilisateurs × films (rouge = note manquante)",
                xaxis_title="films",
                yaxis_title="utilisateurs",
                height=500,
                template=get_plotly_template()
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.session_state['notes'] = notes
            st.session_state['notes_original'] = notes.copy()
        
        st.markdown("---")
        st.markdown("###  Imputation des valeurs manquantes")
        st.markdown("On remplace les NaN par la **moyenne de chaque film**.")
        
        if st.button(" Remplacer les NaN par la moyenne", key="impute"):
            if 'notes' not in st.session_state:
                st.warning("Veuillez d'abord générer une matrice de notes.")
            else:
                with st.spinner("Imputation en cours..."):
                    notes_impute = st.session_state['notes'].copy()
                    for j in range(n_films):
                        col = notes_impute[:, j]
                        moyenne = np.nanmean(col)
                        notes_impute[np.isnan(col), j] = round(moyenne, 1)
                
                fig2 = go.Figure()
                fig2.add_trace(go.Heatmap(
                    z=notes_impute,
                    text=np.round(notes_impute, 1),
                    texttemplate="%{text}",
                    colorscale='YlGn',
                    zmin=1, zmax=5,
                    showscale=True
                ))
                
                fig2.update_layout(
                    title="Matrice après imputation (moyenne par film)",
                    xaxis_title="films",
                    yaxis_title="utilisateurs",
                    height=500,
                    template=get_plotly_template()
                )
                
                st.plotly_chart(fig2, use_container_width=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Avant imputation**")
                    df_before = pd.DataFrame(st.session_state['notes_original'])
                    st.dataframe(df_before.style.highlight_null(color='#ffcccc'))
                
                with col2:
                    st.markdown("**Après imputation**")
                    df_after = pd.DataFrame(np.round(notes_impute, 1))
                    st.dataframe(df_after)
                
                st.info(" **Application pratique** : Cette technique est utilisée dans les systèmes de recommandation (Netflix, Spotify, Amazon) pour traiter les données manquantes avant d'appliquer des algorithmes de factorisation matricielle comme la SVD.")

# ============================================================
# TACHE 3 : INTEGRATION
# ============================================================
elif page == "Integration":
    st.markdown("<h1>∫ Integration de matrices de fonctions</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-secondary);'>Calcul element par element d'une matrice dependant du temps</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.latex(r"A(t) = \begin{pmatrix} t & t^2 \\ 1 & e^t \end{pmatrix} \quad \Rightarrow \quad \int_0^1 A(t)\,dt = \begin{pmatrix} 0.5 & 1/3 \\ 1 & e-1 \end{pmatrix}")
    
    A_anal = np.array([[0.5, 1/3], [1.0, np.e - 1]])
    
    st.markdown("""
        <div class="info-box">
            <strong> Resultat analytique</strong><br>
            ∫₀¹ t dt = 0.5<br>
            ∫₀¹ t² dt = 1/3 ≈ 0.333333<br>
            ∫₀¹ 1 dt = 1.0<br>
            ∫₀¹ eᵗ dt = e-1 ≈ 1.718282
        </div>
    """, unsafe_allow_html=True)
    
    N = st.slider("Nombre de points", 100, 100000, 5000, step=100)
    
    with st.spinner("Calcul en cours..."):
        t = np.linspace(0, 1, N)
        dt = t[1] - t[0]
        
        A_t = np.array([
            [t, t**2],
            [np.ones_like(t), np.exp(t)]
        ])
        A_num = np.sum(A_t, axis=2) * dt
        erreur = np.max(np.abs(A_anal - A_num))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div class="metric">
                <div class="metric-value">{N:,}</div>
                <div class="metric-label">points</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric">
                <div class="metric-value">{erreur:.2e}</div>
                <div class="metric-label">erreur maximale</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h2> Resultats</h2>", unsafe_allow_html=True)
    
    df_compare = pd.DataFrame({
        "Element": ["A(1,1)", "A(1,2)", "A(2,1)", "A(2,2)"],
        "Analytique": [0.5, 1/3, 1.0, np.e-1],
        "Numerique": [A_num[0,0], A_num[0,1], A_num[1,0], A_num[1,1]]
    })
    
    df_compare["Difference"] = np.abs(df_compare["Analytique"] - df_compare["Numerique"])
    
    st.dataframe(df_compare.style.format({
        "Analytique": "{:.8f}",
        "Numerique": "{:.8f}",
        "Difference": "{:.2e}"
    }), use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("<h2>Convergence de la methode</h2>", unsafe_allow_html=True)
    
    if st.button(" Afficher la convergence", use_container_width=True):
        with st.spinner("Calcul en cours..."):
            N_vals = [10, 50, 100, 500, 1000, 5000, 10000, 50000]
            erreurs = []
            
            for n in N_vals:
                t = np.linspace(0, 1, n)
                dt = t[1] - t[0]
                A_t = np.array([[t, t**2], [np.ones_like(t), np.exp(t)]])
                A_res = np.sum(A_t, axis=2) * dt
                erreurs.append(np.max(np.abs(A_anal - A_res)))
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=N_vals, y=erreurs,
            mode='markers+lines',
            name='Erreur mesuree',
            line=dict(color='#3b82f6', width=2),
            marker=dict(size=6)
        ))
        
        err_theo = erreurs[0] * (N_vals[0] / np.array(N_vals))
        fig.add_trace(go.Scatter(
            x=N_vals, y=err_theo,
            mode='lines',
            name='O(1/N) theorique',
            line=dict(color='#f97316', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title="Convergence de la methode des rectangles",
            xaxis_title="N",
            yaxis_title="Erreur",
            xaxis_type="log",
            yaxis_type="log",
            template=get_plotly_template(),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
            <div class="info-box">
                <strong> Conclusion</strong><br>
                La methode des rectangles converge en O(1/N), conforme a la theorie.
                Avec N=10000 points, l'erreur est inferieure a 10⁻⁵.
            </div>
        """, unsafe_allow_html=True)

# ============================================================
# TACHE 4 : MODELE DE LESLIE
# ============================================================
elif page == "Modele de Leslie":
    st.markdown("<h1> Modèle de Leslie</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-secondary);'>Simulation de l'évolution d'une population structurée par âge</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Paramètres (toujours visibles)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        taux_jeunes = st.slider("Fécondité (jeunes)", 0.0, 5.0, 2.5, step=0.1)
    with col2:
        taux_adultes = st.slider("Fécondité (adultes)", 0.0, 5.0, 3.0, step=0.1)
    with col3:
        taux_ages = st.slider("Fécondité (âgés)", 0.0, 3.0, 0.5, step=0.1)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        survie_jeunes = st.slider("Survie jeunes → adultes", 0.0, 1.0, 0.6, step=0.05)
    with col2:
        survie_adultes = st.slider("Survie adultes → âgés", 0.0, 1.0, 0.4, step=0.05)
    with col3:
        survie_ages = st.slider("Survie âgés", 0.0, 1.0, 0.0, step=0.05)
    
    generations = st.slider("Nombre de générations", 10, 100, 50)
    
    # Population initiale
    col1, col2, col3 = st.columns(3)
    with col1:
        pop_jeunes = st.number_input("Jeunes initiaux", 0, 500, 100)
    with col2:
        pop_adultes = st.number_input("Adultes initiaux", 0, 500, 50)
    with col3:
        pop_ages = st.number_input("Âgés initiaux", 0, 500, 20)
    
    # ============================================================
    # BOUTON 1 : SIMULATION PRINCIPALE
    # ============================================================
    if st.button(" Lancer la simulation", use_container_width=True):
        # Construction de la matrice de Leslie
        L = np.array([
            [taux_jeunes, taux_adultes, taux_ages],
            [survie_jeunes, 0, 0],
            [0, survie_adultes, survie_ages]
        ])
        
        X0 = np.array([pop_jeunes, pop_adultes, pop_ages])
        
        # Simulation
        population = [X0.copy()]
        X = X0.copy()
        for _ in range(generations - 1):
            X = L @ X
            population.append(X.copy())
        population = np.array(population)
        
        total = population.sum(axis=1)
        proportions = population / total.reshape(-1, 1)
        
        # Calcul de la valeur propre dominante et de la distribution stable
        valeurs_propres, vecteurs_propres = np.linalg.eig(L)
        lam = np.max(np.abs(valeurs_propres))
        
        # Distribution stable : vecteur propre associé à λ (normalisé)
        idx = np.argmax(np.abs(valeurs_propres))
        distribution_stable = np.abs(vecteurs_propres[:, idx])
        distribution_stable = distribution_stable / distribution_stable.sum()
        
        # Stocker dans session_state pour le bouton des 3 cas
        st.session_state['L_principal'] = L
        st.session_state['X0_principal'] = X0
        st.session_state['generations_principal'] = generations
        
        # ============================================================
        # MÉTRIQUES PRINCIPALES
        # ============================================================
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="metric">
                    <div class="metric-value">{lam:.4f}</div>
                    <div class="metric-label">λ dominant</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if lam > 1.01:
                st.markdown("""
                    <div class="metric">
                        <div class="metric-value"> croissance</div>
                        <div class="metric-label">λ > 1</div>
                    </div>
                """, unsafe_allow_html=True)
            elif lam < 0.99:
                st.markdown("""
                    <div class="metric">
                        <div class="metric-value"> déclin</div>
                        <div class="metric-label">λ < 1</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="metric">
                        <div class="metric-value"> stable</div>
                        <div class="metric-label">λ = 1</div>
                    </div>
                """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric">
                    <div class="metric-value">{int(total[-1]):,}</div>
                    <div class="metric-label">population finale</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            ratio = total[-1] / total[0]
            st.markdown(f"""
                <div class="metric">
                    <div class="metric-value">{(ratio-1)*100:+.1f}%</div>
                    <div class="metric-label">évolution</div>
                </div>
            """, unsafe_allow_html=True)
        
        # ============================================================
        # DISTRIBUTION STABLE THÉORIQUE
        # ============================================================
        
        st.markdown("---")
        st.markdown("<h2> Distribution stable théorique</h2>", unsafe_allow_html=True)
        
        st.markdown(f"""
        La **distribution stable** est le vecteur propre associé à λ = {lam:.4f} :
        
        | Classe | Proportion théorique |
        |--------|---------------------|
        | Jeunes | **{distribution_stable[0]:.2%}** |
        | Adultes | **{distribution_stable[1]:.2%}** |
        | Âgés | **{distribution_stable[2]:.2%}** |
        
        Après un grand nombre de générations, la population tend vers cette répartition,
        **quelle que soit la population initiale** (théorème de Perron-Frobenius).
        """)
        
        # ============================================================
        # GRAPHIQUES ÉVOLUTION
        # ============================================================
        
        st.markdown("<h2>Évolution de la population</h2>", unsafe_allow_html=True)
        
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Population totale", "Distribution des âges"))
        
        # Graphique 1 : Population totale
        fig.add_trace(go.Scatter(x=list(range(generations)), y=total, 
                                mode='lines+markers', name='Population',
                                line=dict(color='#3b82f6', width=2),
                                marker=dict(size=3)), row=1, col=1)
        
        # Graphique 2 : Distribution des âges avec lignes théoriques
        labels = ['Jeunes', 'Adultes', 'Âgés']
        couleurs = ['#3b82f6', '#f97316', '#ef4444']
        
        for k, (label, couleur) in enumerate(zip(labels, couleurs)):
            # Courbe réelle
            fig.add_trace(go.Scatter(x=list(range(generations)), y=proportions[:, k],
                                    mode='lines', name=label,
                                    line=dict(color=couleur, width=2)), row=1, col=2)
            # Ligne théorique (distribution stable)
            fig.add_trace(go.Scatter(x=list(range(generations)), y=[distribution_stable[k]]*generations,
                                    mode='lines', name=f"{label} (théorique)",
                                    line=dict(color=couleur, width=1.5, dash='dash'),
                                    showlegend=False), row=1, col=2)
        
        fig.update_layout(height=500, template=get_plotly_template())
        fig.update_yaxes(title_text="Population", row=1, col=1)
        fig.update_yaxes(title_text="Proportion", row=1, col=2)
        fig.update_xaxes(title_text="Génération", row=1, col=1)
        fig.update_xaxes(title_text="Génération", row=1, col=2)
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        *Les lignes pointillées représentent la **distribution stable théorique**.  
        On observe que les proportions réelles convergent vers ces valeurs.*
        """)
        
        # ============================================================
        # MATRICE DE LESLIE
        # ============================================================
        
        st.markdown("<h2> Matrice de Leslie</h2>", unsafe_allow_html=True)
        
        df_L = pd.DataFrame(L, index=["Jeunes", "Adultes", "Âgés"], columns=["Jeunes", "Adultes", "Âgés"])
        st.dataframe(df_L.style.background_gradient(cmap='Blues', axis=None))
    
    # ============================================================
    # LES 3 CAS CLASSIQUES (EN DEHORS DU PREMIER BOUTON)
    # ============================================================
    
    st.markdown("---")
    st.markdown("<h2> Les 3 cas classiques</h2>", unsafe_allow_html=True)
    
    if st.button(" Afficher croissance / déclin / stable", key="show_cases"):
        with st.spinner("Simulation en cours..."):
            L_croiss = np.array([[0, 3, 1], [0.6, 0, 0], [0, 0.5, 0]])
            L_declin = np.array([[0, 1, 0], [0.4, 0, 0], [0, 0.3, 0]])
            L_stable = np.array([[0, 2, 0], [0.5, 0, 0], [0, 0.4, 0]])
            
            X0_c = np.array([80, 40, 10])
            X0_d = np.array([100, 60, 30])
            X0_s = np.array([100, 50, 20])
            
            def sim(L, X0, n=30):
                pop = [X0.copy()]
                X = X0.copy()
                for _ in range(n-1):
                    X = L @ X
                    pop.append(X.copy())
                return np.array(pop)
            
            pop_c = sim(L_croiss, X0_c)
            pop_d = sim(L_declin, X0_d)
            pop_s = sim(L_stable, X0_s)
            
            lam_c = np.max(np.abs(np.linalg.eigvals(L_croiss)))
            lam_d = np.max(np.abs(np.linalg.eigvals(L_declin)))
            lam_s = np.max(np.abs(np.linalg.eigvals(L_stable)))
        
        fig2 = make_subplots(rows=1, cols=3, subplot_titles=(f"Croissance (λ={lam_c:.3f})", 
                                                             f"Déclin (λ={lam_d:.3f})", 
                                                             f"Stable (λ={lam_s:.3f})"))
        
        couleurs2 = ['#10b981', '#ef4444', '#3b82f6']
        
        for idx, (pop, couleur, titre) in enumerate(zip([pop_c, pop_d, pop_s], couleurs2, ["Croissance", "Déclin", "Stable"])):
            fig2.add_trace(go.Scatter(x=list(range(30)), y=pop.sum(axis=1),
                                    mode='lines', name=titre,
                                    line=dict(color=couleur, width=2.5),
                                    fill='tozeroy', opacity=0.5), row=1, col=idx+1)
        
        fig2.update_layout(height=500, template=get_plotly_template(), showlegend=False)
        fig2.update_xaxes(title_text="Génération")
        fig2.update_yaxes(title_text="Population")
        
        st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("""
            <div class="info-box">
                <strong> Interprétation</strong><br>
                • <strong>λ > 1</strong> → croissance exponentielle (la population explose)<br>
                • <strong>λ < 1</strong> → déclin vers l'extinction<br>
                • <strong>λ = 1</strong> → population stable (équilibre démographique)<br><br>
                La distribution des âges converge vers le vecteur propre associé à λ,
                quelle que soit la condition initiale — c'est la <strong>distribution stable</strong>.
            </div>
        """, unsafe_allow_html=True)
    
    st.success("**Modèle de Leslie terminé** — illustration du lien entre l'algèbre linéaire (valeurs propres, vecteurs propres) et une application concrète en démographie et écologie.")