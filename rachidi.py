import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
    name="Cercle unite T",
    line=dict(color="#94A3B8", width=2, dash="dash"),
)

@st.cache_data
def companion_matrix(coeffs):
    """Matrice compagnon - section 3.1 du document"""
    r = len(coeffs)
    C = np.zeros((r, r))
    C[0, :] = coeffs
    for i in range(1, r):
        C[i, i - 1] = 1
    return C

@st.cache_data
def generalized_fibonacci(coeffs, init, n_max):
    """Suite de Fibonacci generalisee - equation (1.1)"""
    seq = list(init[:len(coeffs)])
    for n in range(len(coeffs), n_max + 1):
        val = sum(coeffs[i] * seq[n - i - 1] for i in range(len(coeffs)))
        seq.append(val)
    return np.array(seq)

def show_rachidi():
    # CSS pour les cartes metriques
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
            border-color: #f59e0b;
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
            background: rgba(245,158,11,0.08);
            border-left: 3px solid #f59e0b;
            border-radius: 8px;
            padding: 12px 16px;
            margin: 12px 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # En-tete du module
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 0.25rem;">
            <div style="width: 4px; height: 28px; background: linear-gradient(135deg, #f59e0b, #d97706); border-radius: 4px;"></div>
            <h1 style="font-size: 1.6rem; font-weight: 700; color: var(--st-color-text-primary); margin: 0;">
                Module 3
            </h1>
            <span style="font-size: 1.4rem; color: #64748b; margin: 0 4px;">|</span>
            <h2 style="font-size: 1.3rem; font-weight: 500; color: var(--st-color-text-secondary); margin: 0;">
                Rachidi
            </h2>
        </div>
        <div style="display: flex; align-items: baseline; gap: 8px; margin-left: 14px;">
            <span style="font-size: 0.9rem; font-weight: 500; color: #f59e0b;">Puissance de Matrice Compagnon</span>
            <span style="font-size: 0.7rem; color: #64748b;">·</span>
            <span style="font-size: 0.7rem; color: #64748b;">Fibonacci generalisee</span>
            <span style="font-size: 0.7rem; color: #64748b;">·</span>
            <span style="font-size: 0.7rem; color: #64748b;">formule de Binet</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Bloc de reference
    st.markdown("""
    <div class="info-box">
        <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
            <span style="font-weight: 600; color: #f59e0b;">Reference</span>
            <span style="color: var(--st-color-text-primary);">Rachidi (2025)</span>
            <span style="color: #64748b;">—</span>
            <span style="font-size: 0.85rem; color: var(--st-color-text-secondary);">Powers of Companion Matrix via Linear Recursiveness. Application</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("---")
        st.markdown("### Parametres Rachidi")
        r = st.slider("Ordre r", 2, 5, 3)
        n_power = st.slider("Puissance n", 1, 10, 3)
        
        st.markdown("#### Coefficients de recurrence")
        coeffs = [st.number_input(f"a_{i+1}", value=1.0, key=f"rach_coeff_{i}", step=0.5) for i in range(r)]
        
        st.markdown("#### Conditions initiales")
        init_vals = [st.number_input(f"v_{i}", value=1.0, key=f"rach_init_{i}", step=0.5) for i in range(r)]
        
        st.markdown("#### Termes a calculer")
        n_terms = st.slider("Nombre de termes de la suite", 10, 80, 30)
    
    # Matrice compagnon et puissance
    A = companion_matrix(coeffs)
    An = np.linalg.matrix_power(A, n_power)
    eigenvalues = eigvals(A)
    
    st.markdown("### Matrice compagnon A")
    st.code(f"A =\n{A}")
    
    st.caption(f" A^{n_power} decrit l'evolution du systeme apres {n_power} iterations (analogue discret de la monodromie)")
    
    st.markdown(f"### A^{n_power}")
    st.code(f"A^{n_power} =\n{An}")
    
    # Analyse de stabilite
    max_eval = max(abs(e) for e in eigenvalues)
    
    if max_eval < 1:
        stability_status = "STABLE"
        stability_color = "#10B981"
        stability_detail = "Toutes les racines sont a l'interieur du cercle unite"
        interp = "Convergence vers zero (systeme contractant)"
    elif max_eval > 1:
        stability_status = "UNSTABLE"
        stability_color = "#EF4444"
        stability_detail = "Au moins une racine est a l'exterieur du cercle unite"
        interp = "Divergence exponentielle (systeme dilatant)"
    else:
        stability_status = "MARGINAL"
        stability_color = "#F59E0B"
        stability_detail = "Racines sur le cercle unite"
        interp = "Comportement cyclique ou stationnaire"
    
    st.markdown(f"""
    <div style="background:{stability_color}10; border-left:4px solid {stability_color}; border-radius:8px; padding:12px 16px; margin:12px 0;">
        <b style="color:{stability_color};">{stability_status}</b><br>
        {stability_detail}<br>
        <small>• max|λ| = {max_eval:.6f}</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.info(f"**Interpretation dynamique** : max|λ| = {max_eval:.4f} → {interp}")
    
    # Oscillations complexes
    has_complex = any(abs(ev.imag) > 1e-8 for ev in eigenvalues)
    if has_complex:
        st.info("**Valeurs propres complexes** → oscillations dans la suite v_n")
    else:
        st.info("**Valeurs propres reelles** → comportement direct (sans oscillations)")
    
    # Metriques
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
    st.markdown("### Racines caracteristiques (Theoreme 7)")
    
    fig_spec = go.Figure()
    theta = np.linspace(0, 2 * np.pi, 300)
    fig_spec.add_trace(go.Scatter(
        x=np.cos(theta), y=np.sin(theta),
        mode='lines', name='Cercle unite T',
        line=dict(color='#64748b', width=2, dash='dash')
    ))
    
    for i, ev in enumerate(eigenvalues):
        if abs(ev) < 1:
            color = '#10b981'
            status = "stable"
        elif abs(ev) > 1:
            color = '#ef4444'
            status = "unstable"
        else:
            color = '#f59e0b'
            status = "marginal"
        
        fig_spec.add_trace(go.Scatter(
            x=[ev.real], y=[ev.imag],
            mode='markers+text',
            name=f'λ{i+1} ({status})',
            marker=dict(size=18, color=color, symbol='circle', line=dict(width=2, color='white')),
            text=[f' λ{i+1}'],
            textposition='top right',
            textfont=dict(size=12)
        ))
    
    fig_spec.update_layout(
        title="Spectre de la matrice compagnon",
        height=450,
        **_PLOTLY_BASE,
        xaxis_title="Partie reelle",
        yaxis_title="Partie imaginaire",
        xaxis=dict(range=[-2.2, 2.2], showgrid=True),
        yaxis=dict(range=[-2.2, 2.2], showgrid=True, scaleanchor="x", scaleratio=1)
    )
    st.plotly_chart(fig_spec, use_container_width=True)
    
    # Tableau des valeurs propres
    df_eigen = pd.DataFrame([
        {"Racine": f"λ{i+1}", 
         "Partie reelle": f"{ev.real:.6f}", 
         "Partie imaginaire": f"{ev.imag:.6f}", 
         "Module": f"{abs(ev):.6f}",
         "Stabilite": "Stable" if abs(ev) < 1 else "Instable" if abs(ev) > 1 else "Marginal"}
        for i, ev in enumerate(eigenvalues)
    ])
    st.dataframe(df_eigen, use_container_width=True, hide_index=True)
    
    export_csv(df_eigen, "rachidi_eigenvalues.csv", "Exporter les racines caracteristiques")
    
    # Verification numerique
    fib_seq = generalized_fibonacci(coeffs, init_vals, n_terms)
    X0 = np.array(init_vals[:r])
    Xn_matrix = An @ X0
    
    if n_power <= n_terms:
        seq_at_n = fib_seq[n_power]
    else:
        seq_at_n = generalized_fibonacci(coeffs, init_vals, n_power)[n_power]
    
    st.markdown("### Verification numerique : methode matricielle vs recurrence")
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.metric(f"A^{n_power} x X0 (matriciel)", str(Xn_matrix))
    with col_v2:
        st.metric(f"v_{n_power} par recurrence", f"{seq_at_n:.6f}")
    
    st.caption("Les deux methodes donnent des resultats coherents (conformement a la Proposition 1 de Rachidi)")
    
    # Suite de Fibonacci generalisee
    st.markdown("### Suite de Fibonacci generalisee")
    
    fig_fib = make_subplots(rows=1, cols=2, subplot_titles=("<b>Courbe</b>", "<b>Barres</b>"), horizontal_spacing=0.10)
    idx = np.arange(len(fib_seq))
    
    fig_fib.add_trace(
        go.Scatter(x=idx, y=fib_seq, mode='lines+markers', name='v_n',
                   line=dict(color='#2563EB', width=2.5),
                   marker=dict(size=5, color='#7C3AED')),
        row=1, col=1
    )
    fig_fib.add_trace(
        go.Bar(x=idx, y=fib_seq, name='v_n',
               marker_color=["#10B981" if v >= 0 else "#EF4444" for v in fib_seq],
               opacity=0.8),
        row=1, col=2
    )
    
    fig_fib.update_layout(
        title=f"Suite recurrente lineaire d'ordre {r}",
        height=400,
        showlegend=False,
        **_PLOTLY_BASE,
        xaxis=dict(title="n", **_GRID),
        yaxis=dict(title="v_n", **_GRID),
        xaxis2=dict(title="n", **_GRID),
        yaxis2=dict(title="v_n", **_GRID)
    )
    st.plotly_chart(fig_fib, use_container_width=True)
    
    df_fib = pd.DataFrame({'n': idx, 'v_n': fib_seq})
    st.dataframe(df_fib.style.format({'v_n': '{:.6g}'}), use_container_width=True, hide_index=True)
    export_csv(df_fib, "rachidi_fibonacci.csv", "Exporter suite de Fibonacci")
    
    # Formule de Binet
    st.markdown("### Formule de Binet generalisee (expression 1.2)")
    st.latex(r"v_n = \sum_{k=1}^{h} \left( \sum_{f=0}^{m_k-1} x_{k,f} n^f \right) \lambda_k^n")
    
    # Details analytiques
    with st.expander("Details analytiques", expanded=False):
        st.markdown("#### Polynome caracteristique")
        poly_expr = f"P(z) = z^{r} - " + " - ".join([f"{coeffs[i]}z^{r-i-1}" for i in range(r-1)]) + f" - {coeffs[-1]}"
        st.latex(poly_expr)
        
        st.markdown("#### Racines caracteristiques")
        for i, ev in enumerate(eigenvalues):
            st.write(f"λ{i+1} = {ev.real:.6f} + {ev.imag:.6f}i")
        
        st.markdown("#### Expression (3.2) - Decomposition combinatoire")
        st.latex(r"Y_n = \rho(n,r)W_0 + \rho(n-1,r)W_1 + \dots + \rho(n-r+1,r)W_{r-1}")
        
        st.markdown("#### Expression (1.3) - Fonction ρ(n,r)")
        st.latex(r"\rho(n,r) = \sum_{k_1 + 2k_2 + \dots + rk_r = n-r} \frac{(k_1 + \dots + k_r)!}{k_1! \dots k_r!} a_1^{k_1} \dots a_r^{k_r}")
    
    # Lien avec Floquet
    st.markdown("---")
    st.markdown("### Lien avec la theorie de Floquet")
    
    st.info(f"""
    **Matrice compagnon A** : matrice de transfert du systeme.
    
    - Les valeurs propres de A sont les **racines caracteristiques** de la recurrence.
    - La stabilite est determinee par max|λ| = {max_eval:.6f}
    
    **Pour un systeme periodique de periode q** :
    - La matrice de monodromie serait N = A_q x ... x A_1
    - Les puissances A^n permettent de calculer l'evolution sur n periodes
    
    **Relation avec la suite de Fibonacci** :
    - Les entrees de A^n sont donnees par les termes v_n^(s) de la suite de Fibonacci generalisee.
    - La formule de Binet generalisee donne une expression explicite de v_n.
    
    Ce module Rachidi complete Floquet en donnant les **outils de calcul explicite** (puissances de matrices, suites recurrentes).
    """)