import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
import warnings
import sympy as sp
from scipy.linalg import eigvals, expm, logm
from scipy.special import comb
import time
import math

warnings.filterwarnings('ignore')

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG - ULTRA PREMIUM
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Floquet Theory Suite | Economic Dynamics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────────────────────────
# CSS DESIGN WAW - INTERFACE DE LUXE
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main title avec gradient animé */
    .main-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s ease infinite;
        margin-bottom: 0.5rem;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .subtitle {
        text-align: center;
        color: #888;
        margin-bottom: 2rem;
        font-size: 1rem;
    }
    
    /* Cartes premium */
    .premium-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(248,250,252,0.98) 100%);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        border: 1px solid rgba(102,126,234,0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.12);
    }
    
    /* Info box */
    .info-box {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border-radius: 15px;
        padding: 16px 20px;
        border-left: 4px solid #667eea;
        margin: 15px 0;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 25px 0 15px 0;
        display: inline-block;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 16px;
        text-align: center;
        color: white;
        box-shadow: 0 5px 20px rgba(102,126,234,0.3);
    }
    
    .metric-card .label {
        font-size: 0.85rem;
        opacity: 0.9;
        letter-spacing: 1px;
    }
    
    .metric-card .value {
        font-size: 1.8rem;
        font-weight: 800;
        margin: 8px 0;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stSlider label {
        color: rgba(255,255,255,0.7) !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 20px;
        background: #f0f2f6;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown('<div class="main-title"> Floquet Theory & Economic Dynamics </div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Complete Mathematical Suite | Heijman & von Mouche (2015) • BBR (2021) • Rachidi</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR PREMIUM AVEC LOGO
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <div style="font-size: 3rem;"></div>
        <div style="font-weight: 800; font-size: 1.3rem;">Simulation Suite</div>
        <div style="font-size: 0.8rem; opacity: 0.7;">Floquet • BBR • Rachidi</div>
    </div>
    """, unsafe_allow_html=True)
    
    sim_choice = st.radio(
        "🎛️ **Sélectionnez le module**",
        [
            "📈 1. Floquet - Samuelson-Hicks Périodique",
            "🔢 2. BBR - Matrices Compagnons en Blocs", 
            "⚡ 3. Rachidi - Puissance & Fibonacci"
        ],
        format_func=lambda x: x.split(".")[1] if "." in x else x
    )
    
    st.markdown("---")
    st.caption("📖 **Références**\n\nHeijman & von Mouche (2015)\nBenkhaldoun, Ben Taher & Rachidi (2021)\nRachidi (2025)")

# ==============================================================================================
# MODULE 1 : FLOQUET - SAMUELSON-HICKS PÉRIODIQUE (COMPLET)
# ==============================================================================================
if "Floquet" in sim_choice:
    st.markdown('<div class="section-header">📈 Module 1 | Floquet Theory & Samuelson-Hicks Model</div>', unsafe_allow_html=True)
    
    # Paramètres dans sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🎛️ Paramètres Floquet")
        
        mode = st.radio("Mode du modèle", ["Constant (SH)", "Periodic (PSH)"], index=1)
        T = st.slider("Horizon temporel T", 20, 200, 80)
        
        if "Periodic" in mode:
            q = st.slider("Période q", 2, 8, 3)
        else:
            q = 1
        
        st.markdown("#### Coefficients de base")
        gamma0 = st.slider("γ₀ (propension à consommer)", 0.1, 0.95, 0.6, 0.05)
        alpha0 = st.slider("α₀ (accélérateur)", 0.1, 3.5, 1.2, 0.05)
        
        if "Periodic" in mode and q > 1:
            st.markdown("#### 🔄 Variations périodiques")
            col1, col2 = st.columns(2)
            with col1:
                gamma_amp = st.slider("Amplitude γ", 0.0, 0.5, 0.15, 0.05)
                gamma_phase = st.slider("Phase γ", 0, 360, 0, 30)
            with col2:
                alpha_amp = st.slider("Amplitude α", 0.0, 1.2, 0.4, 0.1)
                alpha_phase = st.slider("Phase α", 0, 360, 45, 30)
        else:
            gamma_amp = alpha_amp = 0.0
            gamma_phase = alpha_phase = 0
        
        st.markdown("####  Composantes exogènes")
        col1, col2, col3 = st.columns(3)
        with col1:
            G_val = st.number_input("G(t)", 0.0, 50.0, 10.0, step=1.0)
        with col2:
            C_auto = st.number_input("C̄", 0.0, 30.0, 5.0, step=1.0)
        with col3:
            I_auto = st.number_input("Ī", 0.0, 30.0, 5.0, step=1.0)
        
        st.markdown("####  Conditions initiales")
        col1, col2 = st.columns(2)
        with col1:
            Y0 = st.number_input("Y(0)", -50.0, 150.0, 20.0, step=5.0)
        with col2:
            Y1 = st.number_input("Y(1)", -50.0, 150.0, 22.0, step=5.0)
    
    # Fonctions mathématiques complètes
    def build_periodic_params(q, g0, a0, g_amp, a_amp, g_phase, a_phase):
        """Construction des paramètres périodiques selon la proposition 38"""
        t = np.arange(q)
        gamma_seq = g0 + g_amp * np.sin(2 * np.pi * t / q + np.radians(g_phase))
        alpha_seq = a0 + a_amp * np.sin(2 * np.pi * t / q + np.radians(a_phase))
        return np.clip(gamma_seq, 0.01, 0.99), np.clip(alpha_seq, 0.05, None)
    
    def simulate_psh(T, q, gamma_seq, alpha_seq, G, C_bar, I_bar, Y0, Y1):
        """Simulation de l'équation (PSH) - équation (3) du document"""
        Y = np.zeros(T + 2)
        Y[0], Y[1] = Y0, Y1
        for t in range(T):
            idx = (t + 1) % q
            g = gamma_seq[idx]
            a = alpha_seq[idx]
            exogenous = C_bar + I_bar + G
            Y[t + 2] = (g + a) * Y[t + 1] - a * Y[t] + exogenous
        return Y
    
    def monodromy_matrix(gamma_seq, alpha_seq, q):
        """Matrice de monodromie - équation (4) du document"""
        M = np.eye(2)
        for m in range(q - 1, -1, -1):
            C_m = np.array([[0, 1], [-alpha_seq[m], gamma_seq[m] + alpha_seq[m]]])
            M = C_m @ M
        return M
    
    def floquet_multipliers(gamma_seq, alpha_seq, q):
        """Calcul des multiplicateurs de Floquet - équation (5)"""
        M = monodromy_matrix(gamma_seq, alpha_seq, q)
        multipliers = eigvals(M)
        return multipliers, M
    
    def stability_analysis(multipliers):
        """Analyse de stabilité selon théorème 2 et corollaire 13"""
        inside = [m for m in multipliers if abs(m) < 1 - 1e-10]
        on = [m for m in multipliers if abs(abs(m) - 1) < 1e-8]
        outside = [m for m in multipliers if abs(m) > 1 + 1e-10]
        
        dim_bounded = len(inside) + len(on)
        dim_c0 = len(inside)
        
        if len(inside) == 2:
            status = " ASYMPTOTIQUEMENT STABLE"
            color = "green"
            detail = "Toutes les solutions tendent vers 0 (Théorème 2)"
        elif len(inside) == 1 and len(outside) == 1:
            status = " POINT SELLE"
            color = "orange"
            detail = "Une solution bornée, une explosive (point selle)"
        elif len(on) == 2:
            status = " STABLE MARGINAL"
            color = "blue"
            detail = "Cycles possibles (cas α=1 dans le modèle constant)"
        elif len(outside) == 2:
            status = " INSTABLE"
            color = "red"
            detail = "Solutions explosives"
        else:
            status = "❓ CAS MIXTE"
            color = "gray"
            detail = "Analyse supplémentaire nécessaire"
        
        return {
            "inside": inside, "on": on, "outside": outside,
            "dim_bounded": dim_bounded, "dim_c0": dim_c0,
            "status": status, "color": color, "detail": detail
        }
    
    # Construction et simulation
    gamma_seq, alpha_seq = build_periodic_params(q, gamma0, alpha0, gamma_amp, alpha_amp, gamma_phase, alpha_phase)
    Y = simulate_psh(T, q, gamma_seq, alpha_seq, G_val, C_auto, I_auto, Y0, Y1)
    multipliers, M = floquet_multipliers(gamma_seq, alpha_seq, q)
    stability = stability_analysis(multipliers)
    
    # Proposition 78: déterminant
    det_alpha_product = np.prod(alpha_seq)
    det_monodromy = np.linalg.det(M)
    
    # Métriques premium
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">REVENU FINAL</div>
            <div class="value">{Y[-1]:.1f}</div>
            <div class="label">Y({T})</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">|λ₁|</div>
            <div class="value">{abs(multipliers[0]):.4f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">|λ₂|</div>
            <div class="value">{abs(multipliers[1]):.4f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="label">det(N)</div>
            <div class="value">{det_monodromy:.4f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        color_map = {"green": "#28a745", "orange": "#fd7e14", "red": "#dc3545", "blue": "#007bff", "gray": "#6c757d"}
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, {color_map[stability['color']]}, {color_map[stability['color']]}dd);">
            <div class="label">STABILITÉ</div>
            <div class="value" style="font-size: 1rem;">{stability['status'].split()[1] if len(stability['status'].split())>1 else stability['status']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Info box sur la stabilité
    st.markdown(f"""
    <div class="info-box">
        <strong> {stability['status']}</strong><br>
        {stability['detail']}<br>
        <small>• dim(SOL⁽⁰⁾ ∩ l^∞) = {stability['dim_bounded']} (solutions bornées)<br>
        • dim(SOL⁽⁰⁾ ∩ c₀) = {stability['dim_c0']} (solutions → 0)</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Graphique principal avec Plotly
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            '<b>📈 Revenu National Y(t)</b>',
            '<b>🌀 Portrait de phase (Y(t), Y(t+1))</b>',
            '<b>📊 Coefficients périodiques γ(t) et α(t)</b>',
            '<b>📈 Taux de croissance instantané</b>'
        ),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]],
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    t_arr = np.arange(T + 2)
    
    # Y(t)
    fig.add_trace(
        go.Scatter(x=t_arr, y=Y, mode='lines', name='Y(t)',
                   line=dict(color='#667eea', width=2.5),
                   fill='tozeroy', fillcolor='rgba(102,126,234,0.1)'),
        row=1, col=1
    )
    fig.add_hline(y=0, line_dash="dash", line_color="gray", row=1, col=1)
    
    # Portrait de phase
    fig.add_trace(
        go.Scatter(x=Y[:-1], y=Y[1:], mode='lines', name='Trajectoire',
                   line=dict(color='#764ba2', width=2),
                   hovertemplate='Y(t)=%{x:.1f}<br>Y(t+1)=%{y:.1f}<extra></extra>'),
        row=1, col=2
    )
    
    # Coefficients périodiques
    gamma_plot = [gamma_seq[t % q] for t in t_arr]
    alpha_plot = [alpha_seq[t % q] for t in t_arr]
    
    fig.add_trace(
        go.Scatter(x=t_arr, y=gamma_plot, mode='lines', name='γ(t)',
                   line=dict(color='#e74c3c', width=2.5, dash='solid')),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=t_arr, y=alpha_plot, mode='lines', name='α(t)',
                   line=dict(color='#2ecc71', width=2.5, dash='solid')),
        row=2, col=1
    )
    
    # Taux de croissance
    growth = np.diff(Y) / (np.abs(Y[:-1]) + 1e-8) * 100
    colors_growth = ['#e74c3c' if g < 0 else '#2ecc71' for g in growth]
    fig.add_trace(
        go.Bar(x=t_arr[1:], y=growth, name='Croissance %',
               marker_color=colors_growth, opacity=0.7),
        row=2, col=2
    )
    fig.add_hline(y=0, line_dash="dash", line_color="gray", row=2, col=2)
    
    fig.update_layout(
        height=600,
        template='plotly_white',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_xaxes(title_text="Temps t", row=2, col=1)
    fig.update_xaxes(title_text="Y(t)", row=1, col=2)
    fig.update_yaxes(title_text="Y(t)", row=1, col=1)
    fig.update_yaxes(title_text="Y(t+1)", row=1, col=2)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Cercle unité avec multiplicateurs
    fig2 = go.Figure()
    
    theta = np.linspace(0, 2 * np.pi, 200)
    fig2.add_trace(go.Scatter(
        x=np.cos(theta), y=np.sin(theta),
        mode='lines', name='Cercle unité (𝕋)',
        line=dict(color='black', width=2, dash='dash')
    ))
    
    colors_mul = ['#2ecc71' if abs(m) < 1 else '#e74c3c' if abs(m) > 1 else '#f39c12' for m in multipliers]
    for i, (lam, color) in enumerate(zip(multipliers, colors_mul)):
        fig2.add_trace(go.Scatter(
            x=[lam.real], y=[lam.imag],
            mode='markers+text',
            name=f'λ{i+1}',
            marker=dict(size=20, color=color, symbol='circle', line=dict(width=2, color='white')),
            text=[f' λ{i+1}'],
            textposition='top right',
            textfont=dict(size=14, weight='bold')
        ))
    
    fig2.add_annotation(x=0.5, y=1.1, text="Zone stable (|z| < 1)", showarrow=False, font=dict(color="#2ecc71", size=12))
    fig2.add_annotation(x=1.2, y=0.2, text="Zone instable (|z| > 1)", showarrow=False, font=dict(color="#e74c3c", size=12))
    
    fig2.update_layout(
        title="<b> Multiplicateurs de Floquet & Cercle Unité</b>",
        height=500,
        template='plotly_white',
        xaxis_title="Partie réelle",
        yaxis_title="Partie imaginaire",
        xaxis=dict(range=[-1.8, 1.8], showgrid=True),
        yaxis=dict(range=[-1.8, 1.8], showgrid=True, scaleanchor="x", scaleratio=1)
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Section des résultats théoriques
    with st.expander("🔬 **Analyse théorique détaillée**", expanded=False):
        st.markdown("""
        ###  Théorèmes clés du document Heijman & von Mouche (2015)
        
        **Proposition 55 (Floquet, 1883)** : Le système (PSH)⁽⁰⁾ a une solution non nulle de type Floquetien (q, z) 
        **si et seulement si** z est un multiplicateur de Floquet.
        
        **Théorème 2** : Pour (PSH)⁽⁰⁾ :
        - dim(SOL⁽⁰⁾ ∩ l^∞) = somme des multiplicités algébriques des multiplicateurs **dans** 𝕋 + somme des multiplicités géométriques **sur** 𝕋
        - dim(SOL⁽⁰⁾ ∩ c₀) = somme des multiplicités algébriques des multiplicateurs **dans** 𝕋
        
        **Proposition 78** : Le produit des multiplicateurs de Floquet vérifie :
        $$\\lambda_1 \\lambda_2 \\cdots \\lambda_k = (-1)^{Mq} \\frac{v_0^{(0)} \\cdots v_{q-1}^{(0)}}{v_0^{(M)} \\cdots v_{q-1}^{(M)}}$$
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.latex(r"\mathcal{N} = \prod_{m=0}^{q-1} \begin{pmatrix} 0 & 1 \\ -\alpha_{q-m} & \gamma_{q-m} + \alpha_{q-m} \end{pmatrix}")
        with col2:
            st.latex(f"\\text{{det}}(\\mathcal{{N}}) = {det_monodromy:.6f}")
            st.latex(f"\\prod \\alpha = {det_alpha_product:.6f}")
            if abs(det_monodromy - det_alpha_product) < 1e-6:
                st.success(" Vérification proposition 78: det(N) = ∏α")
            else:
                st.warning(f" Écart: {abs(det_monodromy - det_alpha_product):.2e}")
        
        st.markdown("#### Séquences périodiques utilisées")
        df_params = pd.DataFrame({
            't': list(range(q)),
            'γ(t)': [f"{g:.4f}" for g in gamma_seq],
            'α(t)': [f"{a:.4f}" for a in alpha_seq]
        })
        st.dataframe(df_params, use_container_width=True)
        
        st.markdown("#### Matrice de monodromie")
        st.code(f"N =\n{M}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================================
# MODULE 2 : BBR - PRODUIT DE MATRICES COMPAGNONS EN BLOCS
# ==============================================================================================
elif "BBR" in sim_choice:
    st.markdown('<div class="section-header">🔢 Module 2 | BBR - Matrices Compagnons en Blocs</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">📖 <strong>Benkhaldoun, Ben Taher & Rachidi (2021)</strong> - Periodic matrix difference equations and companion matrices in blocks</div>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🎛️ Paramètres BBR")
        r = st.slider("Ordre r (taille des blocs)", 2, 5, 3)
        m = st.slider("Nombre de matrices dans le produit", 2, 5, 3)
        
        st.markdown("#### Matrice C(0)")
        coeffs0 = [st.number_input(f"a_{i+1}^{(0)}", value=1.0, key=f"bbr_c0_{i}", step=0.5) for i in range(r)]
        
        st.markdown("#### Matrice C(1)")
        coeffs1 = [st.number_input(f"a_{i+1}^{(1)}", value=0.8, key=f"bbr_c1_{i}", step=0.5) for i in range(r)]
        
        coeffs2, coeffs3, coeffs4 = [], [], []
        if m >= 3:
            st.markdown("#### Matrice C(2)")
            coeffs2 = [st.number_input(f"a_{i+1}^{(2)}", value=0.6, key=f"bbr_c2_{i}", step=0.5) for i in range(r)]
        if m >= 4:
            st.markdown("#### Matrice C(3)")
            coeffs3 = [st.number_input(f"a_{i+1}^{(3)}", value=0.4, key=f"bbr_c3_{i}", step=0.5) for i in range(r)]
        if m >= 5:
            st.markdown("#### Matrice C(4)")
            coeffs4 = [st.number_input(f"a_{i+1}^{(4)}", value=0.2, key=f"bbr_c4_{i}", step=0.5) for i in range(r)]
    
    def companion_matrix(coeffs):
        """Construction d'une matrice compagnon selon (2.2)"""
        r = len(coeffs)
        C = np.zeros((r, r))
        C[0, :] = coeffs
        for i in range(1, r):
            C[i, i - 1] = 1
        return C
    
    # Construction des matrices
    matrices = [companion_matrix(coeffs0), companion_matrix(coeffs1)]
    labels = ["C(0)", "C(1)"]
    if coeffs2:
        matrices.append(companion_matrix(coeffs2))
        labels.append("C(2)")
    if coeffs3:
        matrices.append(companion_matrix(coeffs3))
        labels.append("C(3)")
    if coeffs4:
        matrices.append(companion_matrix(coeffs4))
        labels.append("C(4)")
    
    # Affichage des matrices
    cols = st.columns(min(len(matrices), 3))
    for i, (M, label) in enumerate(zip(matrices, labels)):
        with cols[i % 3]:
            st.markdown(f"**{label}**")
            st.code(f"{M}")
    
    # Calcul du produit (ordre important!)
    product = np.eye(r)
    for M in reversed(matrices):
        product = M @ product
    
    st.markdown("---")
    st.markdown("### 📦 Produit des matrices (Matrice de monodromie)")
    st.code(f"P = {labels[-1]} × ... × {labels[0]} =\n{product}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("det(P)", f"{np.linalg.det(product):.6f}")
    with col2:
        st.metric("tr(P)", f"{np.trace(product):.6f}")
    with col3:
        st.metric("Condition number", f"{np.linalg.cond(product):.2f}")
    
    # Valeurs propres
    evals = eigvals(product)
    
    st.markdown("### ⭕ Multiplicateurs de Floquet (valeurs propres)")
    
    fig_eval = go.Figure()
    theta = np.linspace(0, 2 * np.pi, 200)
    fig_eval.add_trace(go.Scatter(
        x=np.cos(theta), y=np.sin(theta),
        mode='lines', name='Cercle unité',
        line=dict(color='black', width=2, dash='dash')
    ))
    
    for i, ev in enumerate(evals):
        color = '#2ecc71' if abs(ev) < 1 else '#e74c3c' if abs(ev) > 1 else '#f39c12'
        fig_eval.add_trace(go.Scatter(
            x=[ev.real], y=[ev.imag],
            mode='markers+text',
            name=f'λ{i+1}',
            marker=dict(size=18, color=color),
            text=[f' λ{i+1}'],
            textposition='top right'
        ))
    
    fig_eval.update_layout(
        title="Multiplicateurs de Floquet",
        height=450,
        xaxis_title="Partie réelle",
        yaxis_title="Partie imaginaire",
        xaxis=dict(range=[-1.5, 1.5]),
        yaxis=dict(range=[-1.5, 1.5], scaleanchor="x", scaleratio=1)
    )
    st.plotly_chart(fig_eval, use_container_width=True)
    
    # Tableau des valeurs propres
    df_evals = pd.DataFrame([
        {"Multiplicateur": f"λ{i+1}", "Partie réelle": f"{ev.real:.6f}", 
         "Partie imaginaire": f"{ev.imag:.6f}", "Module": f"{abs(ev):.6f}",
         "Stabilité": "Stable" if abs(ev) < 1 else " Instable" if abs(ev) > 1 else "🔄 Marginal"}
        for i, ev in enumerate(evals)
    ])
    st.dataframe(df_evals, use_container_width=True, hide_index=True)
    
    # Lien avec Floquet
    st.info(f"""
    🔗 **Lien avec la théorie de Floquet** : 
    
    Ce produit de matrices compagnons est exactement la **matrice de monodromie** N = C({m-1}) × ... × C(0).
    
    Ses valeurs propres sont les **multiplicateurs de Floquet**. La stabilité du système est déterminée par leur position par rapport au cercle unité 𝕋.
    
    Dans ce cas : {sum(1 for ev in evals if abs(ev) < 1)} multiplicateur(s) stable(s), 
    {sum(1 for ev in evals if abs(ev) > 1)} instable(s).
    """)

# ==============================================================================================
# MODULE 3 : RACHIDI - PUISSANCE DE MATRICE COMPAGNON
# ==============================================================================================
else:
    st.markdown('<div class="section-header">⚡ Module 3 | Rachidi - Puissance de Matrice Compagnon</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">📖 <strong>Rachidi (2025)</strong> - Powers of Companion Matrix via Linear Recursiveness. Application</div>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🎛️ Paramètres Rachidi")
        r = st.slider("Ordre r", 2, 5, 3)
        n_power = st.slider("Puissance n", 1, 10, 3)
        
        st.markdown("#### Coefficients de récurrence")
        coeffs = [st.number_input(f"a_{i+1}", value=1.0, key=f"rach_coeff_{i}", step=0.5) for i in range(r)]
        
        st.markdown("#### Conditions initiales")
        init_vals = [st.number_input(f"v_{i}", value=1.0, key=f"rach_init_{i}", step=0.5) for i in range(r)]
        
        st.markdown("#### Termes à calculer")
        n_terms = st.slider("Nombre de termes de la suite", 10, 50, 25)
    
    def companion_matrix_rachidi(coeffs):
        """Matrice compagnon - section 3.1 du document"""
        r = len(coeffs)
        C = np.zeros((r, r))
        C[0, :] = coeffs
        for i in range(1, r):
            C[i, i - 1] = 1
        return C
    
    def generalized_fibonacci(coeffs, init, n_max):
        """Suite de Fibonacci généralisée - équation (1.1)"""
        seq = list(init[:len(coeffs)])
        for n in range(len(coeffs), n_max + 1):
            val = sum(coeffs[i] * seq[n - i - 1] for i in range(len(coeffs)))
            seq.append(val)
        return np.array(seq)
    
    def rho_n_r(n, r, coeffs):
        """Fonction ρ(n,r) - expression (1.3) du document"""
        if n < r:
            return 0
        if n == r:
            return 1
        
        # Version simplifiée pour l'affichage
        from sympy import symbols, factorial, summation
        k = symbols('k0:%d' % r)
        # Pour une démonstration, on retourne une approximation
        return 1.0
    
    # Matrice compagnon
    A = companion_matrix_rachidi(coeffs)
    
    st.markdown("### Matrice compagnon A")
    st.code(f"A =\n{A}")
    
    # Puissance
    An = np.linalg.matrix_power(A, n_power)
    st.markdown(f"### A^{n_power}")
    st.code(f"A^{n_power} =\n{An}")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("det(A)", f"{np.linalg.det(A):.6f}")
    with col2:
        st.metric(f"det(A^{n_power})", f"{np.linalg.det(An):.6f}")
    with col3:
        st.metric("tr(A)", f"{np.trace(A):.6f}")
    with col4:
        st.metric(f"tr(A^{n_power})", f"{np.trace(An):.6f}")
    
    # Spectre
    eigenvalues = eigvals(A)
    
    st.markdown("###  Racines caractéristiques (Théorème 7)")
    
    fig_spec = go.Figure()
    
    # Cercle unité
    theta = np.linspace(0, 2 * np.pi, 200)
    fig_spec.add_trace(go.Scatter(
        x=np.cos(theta), y=np.sin(theta),
        mode='lines', name='Cercle unité',
        line=dict(color='black', width=2, dash='dash')
    ))
    
    for i, ev in enumerate(eigenvalues):
        fig_spec.add_trace(go.Scatter(
            x=[ev.real], y=[ev.imag],
            mode='markers+text',
            name=f'λ{i+1}',
            marker=dict(size=18, color='#667eea'),
            text=[f' λ{i+1}'],
            textposition='top right'
        ))
    
    fig_spec.update_layout(
        title="Spectre de la matrice compagnon",
        height=450,
        xaxis_title="Partie réelle",
        yaxis_title="Partie imaginaire",
        xaxis=dict(range=[-2, 2]),
        yaxis=dict(range=[-2, 2], scaleanchor="x", scaleratio=1)
    )
    st.plotly_chart(fig_spec, use_container_width=True)
    
    # Suite de Fibonacci généralisée
    st.markdown("### 📈 Suite de Fibonacci généralisée")
    
    fib_seq = generalized_fibonacci(coeffs, init_vals, n_terms)
    
    fig_fib = go.Figure()
    fig_fib.add_trace(go.Scatter(
        x=list(range(len(fib_seq))),
        y=fib_seq,
        mode='lines+markers',
        name='v_n',
        line=dict(color='#667eea', width=2.5),
        marker=dict(size=6, color='#764ba2')
    ))
    fig_fib.update_layout(
        title="Suite récurrente linéaire d'ordre r",
        xaxis_title="n",
        yaxis_title="v_n",
        height=400,
        template='plotly_white'
    )
    st.plotly_chart(fig_fib, use_container_width=True)
    
    # Formule de Binet généralisée
    st.markdown("### 📜 Formule de Binet généralisée (expression 1.2)")
    
    st.latex(r"v_n = \sum_{k=1}^{h} \left( \sum_{f=0}^{m_k-1} x_{k,f} n^f \right) \lambda_k^n")
    
    # Détails des racines
    with st.expander("🔬 Détails analytiques", expanded=False):
        st.markdown("#### Polynôme caractéristique")
        poly_expr = f"P(z) = z^{r} - " + " - ".join([f"{coeffs[i]}z^{r-i-1}" for i in range(r-1)]) + f" - {coeffs[-1]}"
        st.latex(poly_expr)
        
        st.markdown("#### Racines caractéristiques")
        for i, ev in enumerate(eigenvalues):
            st.write(f"λ{i+1} = {ev.real:.6f} + {ev.imag:.6f}i")
        
        st.markdown("#### Expression (3.2) - Décomposition combinatoire")
        st.latex(r"Y_n = \rho(n,r)W_0 + \rho(n-1,r)W_1 + \dots + \rho(n-r+1,r)W_{r-1}")
        
        st.markdown("#### Expression (1.3) - Fonction ρ(n,r)")
        st.latex(r"\rho(n,r) = \sum_{k_1 + 2k_2 + \dots + rk_r = n-r} \frac{(k_1 + \dots + k_r)!}{k_1! \dots k_r!} a_1^{k_1} \dots a_r^{k_r}")
    
    # Matrice de monodromie pour le lien avec Floquet
    st.info(f"""
    🔗 **Lien avec la théorie de Floquet** : 
    
    La matrice compagnon A est la **matrice de transfert** du système. Pour un système périodique de période q, 
    la matrice de monodromie serait le produit A_q × ... × A_1. Les puissances A^n permettent de calculer 
    l'évolution sur n périodes.
    
    **Relation avec la suite de Fibonacci** : Les entrées de A^n sont données par les termes v_n^{{s}}  de la suite 
    de Fibonacci généralisée (Proposition 1 du document).
    """)

# Footer premium
st.markdown("---")
st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0;">
    <div>
        <span style="font-weight: 600;"> Floquet Theory Suite</span><br>
        <span style="font-size: 0.8rem; color: #888;">Heijman & von Mouche (2015) • BBR (2021) • Rachidi (2025)</span>
    </div>
    <div style="text-align: right;">
        <span style="font-size: 0.8rem; color: #888;">Interactive simulation • Real-time Floquet analysis</span><br>
        <span style="font-size: 0.7rem; color: #aaa;">Powered by Streamlit • Plotly • NumPy</span>
    </div>
</div>
""", unsafe_allow_html=True)