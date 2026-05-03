import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.linalg import eigvals
from utils import export_csv

# Constantes Plotly
_PLOTLY_BASE = dict(
    template="plotly_white",
    font=dict(family="Inter"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)
_GRID = dict(showgrid=True, gridcolor="#F1F5F9", zeroline=True, zerolinecolor="#E2E8F0")
_UNIT_CIRCLE_TRACE = go.Scatter(
    x=np.cos(np.linspace(0, 2 * np.pi, 300)),
    y=np.sin(np.linspace(0, 2 * np.pi, 300)),
    mode="lines",
    name="Cercle unité T",
    line=dict(color="#94A3B8", width=2, dash="dash"),
)

@st.cache_data
def companion_matrix(coeffs):
    """Construction d'une matrice compagnon selon (2.2)"""
    n = len(coeffs)
    C = np.zeros((n, n))
    C[0, :] = coeffs
    for i in range(1, n):
        C[i, i - 1] = 1
    return C

def show_bbr():
    # CSS pour les cartes métriques
    st.markdown("""
    <style>
        .metric-card {
            background: var(--st-color-background);
            border: 1px solid var(--st-color-border);
            border-radius: 12px;
            padding: 12px;
            text-align: center;
            transition: all 0.2s ease;
        }
        .metric-card:hover {
            transform: translateY(-2px);
            border-color: #10b981;
        }
        .metric-card .label {
            font-size: 0.7rem;
            text-transform: uppercase;
            color: var(--st-color-text-secondary);
            letter-spacing: 0.5px;
        }
        .metric-card .value {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--st-color-text-primary);
            margin: 6px 0;
        }
        .info-box {
            background: rgba(16,185,129,0.08);
            border-left: 3px solid #10b981;
            border-radius: 8px;
            padding: 12px 16px;
            margin: 12px 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # En-tête du module
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 0.25rem;">
            <div style="width: 4px; height: 28px; background: linear-gradient(135deg, #10b981, #059669); border-radius: 4px;"></div>
            <h1 style="font-size: 1.6rem; font-weight: 700; color: var(--st-color-text-primary); margin: 0;">
                Module 2
            </h1>
            <span style="font-size: 1.4rem; color: #64748b; margin: 0 4px;">|</span>
            <h2 style="font-size: 1.3rem; font-weight: 500; color: var(--st-color-text-secondary); margin: 0;">
                BBR
            </h2>
        </div>
        <div style="display: flex; align-items: baseline; gap: 8px; margin-left: 14px;">
            <span style="font-size: 0.9rem; font-weight: 500; color: #10b981;">Matrices Compagnons en Blocs</span>
            <span style="font-size: 0.7rem; color: #64748b;">·</span>
            <span style="font-size: 0.7rem; color: #64748b;">produit de matrices</span>
            <span style="font-size: 0.7rem; color: #64748b;">·</span>
            <span style="font-size: 0.7rem; color: #64748b;">monodromie</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Bloc de référence
    st.markdown("""
    <div class="info-box">
        <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
            <span style="font-weight: 600; color: #10b981;">Reference</span>
            <span style="color: var(--st-color-text-primary);">Benkhaldoun, Ben Taher &amp; Rachidi (2021)</span>
            <span style="color: #64748b;">—</span>
            <span style="font-size: 0.85rem; color: var(--st-color-text-secondary);">Periodic matrix difference equations and companion matrices in blocks</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Paramètres dans sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown("### Paramètres BBR")
        r = st.slider("Ordre r (taille des blocs)", 2, 5, 3)
        m = st.slider("Nombre de matrices dans le produit", 2, 5, 3)
        
        st.markdown("#### Matrice C(0)")
        coeffs0 = [st.number_input(f"a_{i+1}^{(0)}", value=1.0, key=f"bbr_c0_{i}", step=0.5) for i in range(r)]
        
        st.markdown("#### Matrice C(1)")
        coeffs1 = [st.number_input(f"a_{i+1}^{(1)}", value=0.8, key=f"bbr_c1_{i}", step=0.5) for i in range(r)]
        
        coeffs2, coeffs3 = [], []
        if m >= 3:
            st.markdown("#### Matrice C(2)")
            coeffs2 = [st.number_input(f"a_{i+1}^{(2)}", value=0.6, key=f"bbr_c2_{i}", step=0.5) for i in range(r)]
        if m >= 4:
            st.markdown("#### Matrice C(3)")
            coeffs3 = [st.number_input(f"a_{i+1}^{(3)}", value=0.4, key=f"bbr_c3_{i}", step=0.5) for i in range(r)]
    
    # Construction des matrices
    matrices = [companion_matrix(coeffs0), companion_matrix(coeffs1)]
    labels = ["C(0)", "C(1)"]
    if coeffs2:
        matrices.append(companion_matrix(coeffs2))
        labels.append("C(2)")
    if coeffs3:
        matrices.append(companion_matrix(coeffs3))
        labels.append("C(3)")
    
    # Lien avec la recurrence
    st.info(f"""
    **Interpretation structurelle (BBR)** :
    
    Chaque matrice compagnon C(k) correspond a une relation de recurrence lineaire d'ordre {r}.
    
    Le produit P = C({m-1}) x ... x C(0) decrit l'evolution du systeme sur {m} periodes.
    
    Le comportement asymptotique depend uniquement des valeurs propres de P.
    """)
    
    # Affichage des matrices
    st.markdown("### Matrices compagnons")
    cols = st.columns(min(len(matrices), 4))
    for i, (M, label) in enumerate(zip(matrices, labels)):
        with cols[i % 4]:
            st.markdown(f"**{label}**")
            st.code(f"{M}")
    
    # Produit (matrice monodromie)
    product = np.eye(r)
    for M in reversed(matrices):
        product = M @ product
    
    st.markdown("---")
    st.markdown("### Produit des matrices (Matrice de monodromie)")
    st.code(f"P = {labels[-1]} x ... x {labels[0]}\n\n{product}")
    
    # Metriques
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("det(P)", f"{np.linalg.det(product):.6f}")
    with col2:
        st.metric("tr(P)", f"{np.trace(product):.6f}")
    with col3:
        st.metric("Condition number", f"{np.linalg.cond(product):.2f}")
    
    # Dynamique du systeme
    st.markdown("### Dynamique du systeme : Y(n+1) = P x Y(n)")
    
    Y0_vec = np.ones(r)
    steps = 20
    trajectory = [Y0_vec.copy()]
    
    for _ in range(steps):
        Y_next = product @ trajectory[-1]
        trajectory.append(Y_next)
    
    trajectory = np.array(trajectory)
    
    fig_dyn = go.Figure()
    colors_d = ["#2563EB", "#EF4444", "#10B981", "#F59E0B", "#7C3AED"]
    for i in range(r):
        fig_dyn.add_trace(go.Scatter(
            y=trajectory[:, i],
            mode='lines+markers',
            name=f'Composante {i+1}',
            line=dict(width=2.5, color=colors_d[i % len(colors_d)]),
            marker=dict(size=4)
        ))
    
    fig_dyn.update_layout(
        height=400,
        title=f"Evolution du vecteur d'etat Y(n) — {steps} iterations",
        xaxis_title="Iteration n",
        yaxis_title="Valeur des composantes",
        **_PLOTLY_BASE
    )
    st.plotly_chart(fig_dyn, use_container_width=True)
    
    # Valeurs propres (multiplicateurs de Floquet)
    evals = eigvals(product)
    
    st.markdown("### Multiplicateurs de Floquet (valeurs propres)")
    
    # Analyse de stabilite
    n_stable = sum(1 for e in evals if abs(e) < 1 - 1e-10)
    n_unstable = sum(1 for e in evals if abs(e) > 1 + 1e-10)
    n_marginal = r - n_stable - n_unstable
    
    max_eval = max(abs(e) for e in evals)
    if max_eval < 1:
        stability_status = "STABLE"
        stability_color = "#10B981"
        stability_detail = "Tous les multiplicateurs sont a l'interieur du cercle unite"
    elif max_eval > 1:
        stability_status = "UNSTABLE"
        stability_color = "#EF4444"
        stability_detail = "Au moins un multiplicateur est a l'exterieur du cercle unite"
    else:
        stability_status = "MARGINAL"
        stability_color = "#F59E0B"
        stability_detail = "Multiplicateurs sur le cercle unite"
    
    st.markdown(f"""
    <div style="background:{stability_color}10; border-left:4px solid {stability_color}; border-radius:8px; padding:12px 16px; margin:12px 0;">
        <b style="color:{stability_color};">{stability_status}</b><br>
        {stability_detail}<br>
        <small>• {n_stable} multiplicateur(s) stable(s) | {n_unstable} instable(s) | {n_marginal} marginal(aux)</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Interpretation
    if max_eval < 1:
        interp = "Convergence vers zero (systeme contractant)"
    elif max_eval > 1:
        interp = "Divergence exponentielle (systeme dilatant)"
    else:
        interp = "Comportement cyclique ou stationnaire"
    
    st.info(f"**Interpretation** : max|λ| = {max_eval:.4f} → {interp}")
    
    # Oscillations complexes
    has_complex = any(abs(e.imag) > 1e-8 for e in evals)
    if has_complex:
        st.info("**Valeurs propres complexes** → oscillations dans les composantes du systeme")
    else:
        st.info("**Valeurs propres reelles** → comportement direct (sans oscillations)")
    
    # Cercle unite
    fig_eval = go.Figure()
    theta = np.linspace(0, 2 * np.pi, 300)
    fig_eval.add_trace(go.Scatter(
        x=np.cos(theta), y=np.sin(theta),
        mode='lines', name='Cercle unite T',
        line=dict(color='#64748b', width=2, dash='dash')
    ))
    
    for i, ev in enumerate(evals):
        if abs(ev) < 1:
            color = '#10b981'
            status = "stable"
        elif abs(ev) > 1:
            color = '#ef4444'
            status = "unstable"
        else:
            color = '#f59e0b'
            status = "marginal"
        
        fig_eval.add_trace(go.Scatter(
            x=[ev.real], y=[ev.imag],
            mode='markers+text',
            name=f'λ{i+1} ({status})',
            marker=dict(size=18, color=color, symbol='circle', line=dict(width=2, color='white')),
            text=[f' λ{i+1}'],
            textposition='top right',
            textfont=dict(size=12)
        ))
    
    fig_eval.update_layout(
        title="Multiplicateurs de Floquet dans le plan complexe",
        height=480,
        **_PLOTLY_BASE,
        xaxis_title="Partie reelle",
        yaxis_title="Partie imaginaire",
        xaxis=dict(range=[-1.8, 1.8], showgrid=True),
        yaxis=dict(range=[-1.8, 1.8], showgrid=True, scaleanchor="x", scaleratio=1)
    )
    st.plotly_chart(fig_eval, use_container_width=True)
    
    # Tableau des valeurs propres
    df_evals = pd.DataFrame([
        {"Multiplicateur": f"λ{i+1}", 
         "Partie reelle": f"{ev.real:.6f}", 
         "Partie imaginaire": f"{ev.imag:.6f}", 
         "Module": f"{abs(ev):.6f}",
         "Stabilite": "Stable" if abs(ev) < 1 else "Instable" if abs(ev) > 1 else "Marginal"}
        for i, ev in enumerate(evals)
    ])
    st.dataframe(df_evals, use_container_width=True, hide_index=True)
    
    # Export CSV
    export_csv(df_evals, "bbr_multipliers.csv", "Exporter multiplicateurs BBR")
    
    # Lien avec Floquet
    st.markdown("---")
    st.markdown("### Lien avec la theorie de Floquet")
    
    st.info(f"""
    **Matrice de monodromie** : N = {labels[-1]} x ... x {labels[0]}
    
    - Le determinant de N verifie : det(N) = {np.linalg.det(product):.6f}
    - La trace de N est : tr(N) = {np.trace(product):.6f}
    - Les valeurs propres de N sont les **multiplicateurs de Floquet**
    
    **Stabilite** :
    - **Stable** : tous les |λ| < 1 → systeme contractant
    - **Instable** : un |λ| > 1 → systeme dilatant
    - **Marginal** : des |λ| = 1 → cycles ou comportement periodique
    
    **Resultat** : {n_stable} stable(s), {n_unstable} instable(s), {n_marginal} marginal(aux)
    
    Ce module BBR montre que le produit de matrices compagnons construit exactement la **matrice monodromique** utilisee dans la theorie de Floquet.
    
    **Recurrence associee** : Chaque matrice compagnon C(k) code une recurrence lineaire d'ordre {r} :
    $$
     y_{{n+r}} = a_1^{{(k)}} y_{{n+r-1}} + a_2^{{(k)}} y_{{n+r-2}} + \\cdots + a_r^{{(k)}} y_n
    $$
    """)
    
    # Heatmap
    with st.expander("Heatmap de la matrice de monodromie", expanded=False):
        fig_heat = go.Figure(data=go.Heatmap(
            z=np.abs(product),
            colorscale='Blues',
            colorbar=dict(title='|P_ij|'),
            hovertemplate='Ligne %{y}<br>Colonne %{x}<br>|P|=%{z:.3f}<extra></extra>'
        ))
        fig_heat.update_layout(
            height=450,
            title="Valeurs absolues de la matrice de monodromie",
            xaxis_title="Colonnes",
            yaxis_title="Lignes",
            **_PLOTLY_BASE
        )
        st.plotly_chart(fig_heat, use_container_width=True)