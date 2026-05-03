import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.linalg import eigvals
from utils import export_csv

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
        border-color: #3b82f6;
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
</style>
""", unsafe_allow_html=True)
def show_floquet():
    st.markdown("""
<div style="margin-bottom: 1.5rem;">
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 0.25rem;">
        <div style="width: 4px; height: 28px; background: linear-gradient(135deg, #2563eb, #1d4ed8); border-radius: 4px;"></div>
        <h1 style="font-size: 1.6rem; font-weight: 700; color: var(--st-color-text-primary); margin: 0;">
            Module 1
        </h1>
        <span style="font-size: 1.4rem; color: #64748b; margin: 0 4px;">|</span>
        <h2 style="font-size: 1.3rem; font-weight: 500; color: var(--st-color-text-secondary); margin: 0;">
            Floquet Theory
        </h2>
    </div>
    <div style="display: flex; align-items: baseline; gap: 8px; margin-left: 14px;">
        <span style="font-size: 0.9rem; font-weight: 500; color: #3b82f6;">Samuelson-Hicks Model</span>
        <span style="font-size: 0.7rem; color: #64748b;">·</span>
        <span style="font-size: 0.7rem; color: #64748b;">periodic coefficients</span>
        <span style="font-size: 0.7rem; color: #64748b;">·</span>
        <span style="font-size: 0.7rem; color: #64748b;">Floquet multipliers</span>
    </div>
</div>
""", unsafe_allow_html=True)    
    # Paramètres dans sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown("###  Paramètres Floquet")
        
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
    
    # Fonctions mathématiques
    def build_periodic_params(q, g0, a0, g_amp, a_amp, g_phase, a_phase):
        t = np.arange(q)
        gamma_seq = g0 + g_amp * np.sin(2 * np.pi * t / q + np.radians(g_phase))
        alpha_seq = a0 + a_amp * np.sin(2 * np.pi * t / q + np.radians(a_phase))
        return np.clip(gamma_seq, 0.01, 0.99), np.clip(alpha_seq, 0.05, None)
    
    def simulate_psh(T, q, gamma_seq, alpha_seq, G, C_bar, I_bar, Y0, Y1):
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
        M = np.eye(2)
        for t in range(q):
            g = gamma_seq[t]
            a = alpha_seq[t]
            A_t = np.array([[g + a, -a], [1, 0]])
            M = A_t @ M
        return M
    
    def floquet_multipliers(gamma_seq, alpha_seq, q):
        M = monodromy_matrix(gamma_seq, alpha_seq, q)
        multipliers = eigvals(M)
        return multipliers, M
    
    def stability_analysis(multipliers):
        inside = [m for m in multipliers if abs(m) < 1 - 1e-10]
        on = [m for m in multipliers if abs(abs(m) - 1) < 1e-8]
        outside = [m for m in multipliers if abs(m) > 1 + 1e-10]
        
        dim_bounded = len(inside) + len(on)
        dim_c0 = len(inside)
        
        if len(inside) == 2:
            status = "ASYMPTOTIQUEMENT STABLE"
            color = "green"
            detail = "Toutes les solutions tendent vers 0 (Théorème 2)"
            short = "STABLE"
        elif len(inside) == 1 and len(outside) == 1:
            status = " POINT SELLE"
            color = "orange"
            detail = "Une solution bornée, une explosive (point selle)"
            short = "SELLE"
        elif len(on) == 2:
            status = " STABLE MARGINAL"
            color = "blue"
            detail = "Cycles possibles (cas α=1 dans le modèle constant)"
            short = "CYCLE"
        elif len(outside) == 2:
            status = " INSTABLE"
            color = "red"
            detail = "Solutions explosives"
            short = "INSTABLE"
        else:
            status = " CAS MIXTE"
            color = "gray"
            detail = "Analyse supplémentaire nécessaire"
            short = "MIXTE"
        
        return {
            "inside": inside, "on": on, "outside": outside,
            "dim_bounded": dim_bounded, "dim_c0": dim_c0,
            "status": status, "color": color, "detail": detail,
            "short": short
        }
    
    def shock_dependency_analysis(mode, alpha0, lambdas):
        if "Constant" in mode:
            if abs(alpha0 - 1.0) < 1e-6:
                return " SHOCK-INDEPENDENT", "α = 1 → cycles endogènes sans chocs (Résultat XVII)", "#10B981"
            elif alpha0 < 1:
                return " SHOCK-DEPENDENT", f"α = {alpha0:.3f} < 1 → convergence vers équilibre, besoin de chocs", "#EF4444"
            else:
                return " SHOCK-DEPENDENT", f"α = {alpha0:.3f} > 1 → explosion, besoin de chocs", "#EF4444"
        else:
            one_is_multiplier = any(abs(l - 1) < 1e-6 for l in lambdas)
            if not one_is_multiplier:
                return " SHOCK-INDEPENDENT", "1 n'est PAS multiplicateur de Floquet → PSH génère des cycles sans chocs (Résultat XVIII, numériquement vérifié)", "#10B981"
            else:
                return " CAS LIMITE", "Conjecture 1 non vérifiée pour ces paramètres", "#F59E0B"
    
    # Construction et simulation
    gamma_seq, alpha_seq = build_periodic_params(q, gamma0, alpha0, gamma_amp, alpha_amp, gamma_phase, alpha_phase)
    Y = simulate_psh(T, q, gamma_seq, alpha_seq, G_val, C_auto, I_auto, Y0, Y1)
    multipliers, M = floquet_multipliers(gamma_seq, alpha_seq, q)
    stability = stability_analysis(multipliers)
    shock_label, shock_msg, shock_color = shock_dependency_analysis(mode, alpha0, multipliers)
    
    det_alpha_product = np.prod(alpha_seq)
    det_monodromy = np.linalg.det(M)
    one_is_multiplier = any(abs(l - 1) < 1e-6 for l in multipliers)
    
    # Métriques
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
            <div class="value" style="font-size: 1rem;">{stability['short']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Info box
    st.markdown(f"""
    <div class="info-box">
        <strong> {stability['status']}</strong><br>
        {stability['detail']}<br>
        <small>• dim(SOL⁽⁰⁾ ∩ l^∞) = {stability['dim_bounded']} (solutions bornées)<br>
        • dim(SOL⁽⁰⁾ ∩ c₀) = {stability['dim_c0']} (solutions → 0)</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Interprétation
    max_lambda = max(abs(m) for m in multipliers)
    if max_lambda < 1:
        interp = "Convergence vers un équilibre (stabilité asymptotique)"
        interp_color = "#10B981"
    elif max_lambda > 1:
        interp = "Divergence du système (instabilité économique)"
        interp_color = "#EF4444"
    else:
        interp = " Cycles ou comportement quasi-périodique"
        interp_color = "#F59E0B"
    
    st.markdown(f"""
    <div style="background:{interp_color}10; border-radius:8px; padding:10px 14px; margin:10px 0;">
        <span style="color:{interp_color}; font-weight:600;"> Interprétation économique :</span><br>
        <span style="font-size:0.9rem;">max|λ| = {max_lambda:.4f} → {interp}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Oscillations complexes
    has_complex = any(abs(m.imag) > 1e-8 for m in multipliers)
    if has_complex:
        st.info("**Présence de valeurs propres complexes** → oscillations dans Y(t) (comportement cyclique)")
    else:
        st.info(" **Valeurs propres réelles** → comportement direct (sans oscillations internes)")
    
    # Shock-dependency banner
    st.markdown(f"""
    <div style="background:{shock_color}15; border-left:4px solid {shock_color}; border-radius:8px; padding:12px 16px; margin:12px 0;">
        <b style="color:{shock_color};"> {shock_label}</b><br>
        <span style="font-size:0.85rem;">{shock_msg}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Conjecture 1
    if "Periodic" in mode and q > 1:
        if not one_is_multiplier:
            st.success("**Conjecture 1** : 1 n'est PAS multiplicateur de Floquet → vérifiée pour ces paramètres.")
        else:
            st.warning(" **Conjecture 1** : 1 EST multiplicateur de Floquet → cas limite, à surveiller.")
    
    # Graphique principal
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            '<b> Revenu National Y(t)</b>',
            '<b> Portrait de phase (Y(t), Y(t+1))</b>',
            '<b> Coefficients périodiques γ(t) et α(t)</b>',
            '<b> Taux de croissance instantané</b>'
        ),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]],
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    t_arr = np.arange(T + 2)
    fig.add_trace(go.Scatter(x=t_arr, y=Y, mode='lines', name='Y(t)', line=dict(color='#667eea', width=2.5), fill='tozeroy', fillcolor='rgba(102,126,234,0.1)'), row=1, col=1)
    fig.add_hline(y=0, line_dash="dash", line_color="gray", row=1, col=1)
    fig.add_trace(go.Scatter(x=Y[:-1], y=Y[1:], mode='lines', name='Trajectoire', line=dict(color='#764ba2', width=2)), row=1, col=2)
    
    gamma_plot = [gamma_seq[t % q] for t in t_arr]
    alpha_plot = [alpha_seq[t % q] for t in t_arr]
    fig.add_trace(go.Scatter(x=t_arr, y=gamma_plot, mode='lines', name='γ(t)', line=dict(color='#e74c3c', width=2.5)), row=2, col=1)
    fig.add_trace(go.Scatter(x=t_arr, y=alpha_plot, mode='lines', name='α(t)', line=dict(color='#2ecc71', width=2.5)), row=2, col=1)
    
    growth = np.diff(Y) / (np.abs(Y[:-1]) + 1e-8) * 100
    colors_growth = ['#e74c3c' if g < 0 else '#2ecc71' for g in growth]
    fig.add_trace(go.Bar(x=t_arr[1:], y=growth, name='Croissance %', marker_color=colors_growth, opacity=0.7), row=2, col=2)
    fig.add_hline(y=0, line_dash="dash", line_color="gray", row=2, col=2)
    
    fig.update_layout(height=600, template='plotly_white', showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    fig.update_xaxes(title_text="Temps t", row=2, col=1)
    fig.update_xaxes(title_text="Y(t)", row=1, col=2)
    fig.update_yaxes(title_text="Y(t)", row=1, col=1)
    fig.update_yaxes(title_text="Y(t+1)", row=1, col=2)
    st.plotly_chart(fig, use_container_width=True)
    
    # Animation
    with st.expander(" Animation temporelle de Y(t)", expanded=False):
        st.markdown("Observez l'évolution pas à pas du revenu national")
        max_t = st.slider("Afficher jusqu'à t =", 2, T + 1, min(20, T + 1), key="anim_slider")
        fig_anim = go.Figure()
        fig_anim.add_trace(go.Scatter(x=t_arr[:max_t + 1], y=Y[:max_t + 1], mode='lines+markers', name='Y(t)', line=dict(color='#667eea', width=2.5), marker=dict(size=6), fill='tozeroy', fillcolor='rgba(102,126,234,0.1)'))
        fig_anim.add_trace(go.Scatter(x=[t_arr[max_t]], y=[Y[max_t]], mode='markers', name=f'Y({max_t})', marker=dict(size=14, color='#ef4444', symbol='circle')))
        fig_anim.add_hline(y=0, line_dash='dash', line_color='gray')
        fig_anim.update_layout(height=380, template='plotly_white', title=f'Y(t) jusqu\'à t = {max_t}')
        st.plotly_chart(fig_anim, use_container_width=True)
    
    # Export CSV
    st.markdown("---")
    st.markdown("###  Export des données")
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        df_y = pd.DataFrame({'t': t_arr, 'Y(t)': Y, 'γ(t)': gamma_plot, 'α(t)': alpha_plot})
        export_csv(df_y, "floquet_Yt.csv", " Exporter Y(t), γ(t), α(t)")
    with col_exp2:
        df_mul = pd.DataFrame({'Multiplicateur': ['λ₁', 'λ₂'], 'Partie réelle': [multipliers[0].real, multipliers[1].real], 'Partie imaginaire': [multipliers[0].imag, multipliers[1].imag], 'Module': [abs(multipliers[0]), abs(multipliers[1])]})
        export_csv(df_mul, "floquet_multipliers.csv", " Exporter multiplicateurs")
    
    # Cercle unité
    fig2 = go.Figure()
    theta = np.linspace(0, 2 * np.pi, 200)
    fig2.add_trace(go.Scatter(x=np.cos(theta), y=np.sin(theta), mode='lines', name='Cercle unité (𝕋)', line=dict(color='black', width=2, dash='dash')))
    colors_mul = ['#2ecc71' if abs(m) < 1 else '#e74c3c' if abs(m) > 1 else '#f39c12' for m in multipliers]
    for i, (lam, color) in enumerate(zip(multipliers, colors_mul)):
        fig2.add_trace(go.Scatter(x=[lam.real], y=[lam.imag], mode='markers+text', name=f'λ{i+1}', marker=dict(size=20, color=color, symbol='circle', line=dict(width=2, color='white')), text=[f' λ{i+1}'], textposition='top right', textfont=dict(size=14, weight='bold')))
    fig2.add_annotation(x=0.5, y=1.1, text="Zone stable (|z| < 1)", showarrow=False, font=dict(color="#2ecc71", size=12))
    fig2.add_annotation(x=1.2, y=0.2, text="Zone instable (|z| > 1)", showarrow=False, font=dict(color="#e74c3c", size=12))
    fig2.update_layout(title="<b> Multiplicateurs de Floquet & Cercle Unité</b>", height=500, template='plotly_white', xaxis_title="Partie réelle", yaxis_title="Partie imaginaire", xaxis=dict(range=[-1.8, 1.8], showgrid=True), yaxis=dict(range=[-1.8, 1.8], showgrid=True, scaleanchor="x", scaleratio=1))
    st.plotly_chart(fig2, use_container_width=True)
    
    # Heatmap
    with st.expander("🗺️ Carte de stabilité (γ₀ vs α₀)", expanded=False):
        st.markdown("Analyse de la stabilité dans l'espace des paramètres γ₀ et α₀")
        st.caption("🟢 Vert = stable | 🟡 Jaune = limite | 🔴 Rouge = instable | ⭐ = paramètres actuels")
        n_grid = st.slider("Résolution de la grille", 10, 30, 20, key="heatmap_res")
        gamma_range = np.linspace(0.1, 0.9, n_grid)
        alpha_range = np.linspace(0.1, 3.5, n_grid)
        stability_grid = np.zeros((n_grid, n_grid))
        with st.spinner("Calcul de la carte de stabilité en cours..."):
            for i, g in enumerate(gamma_range):
                for j, a in enumerate(alpha_range):
                    gs, as_ = build_periodic_params(q, g, a, gamma_amp, alpha_amp, gamma_phase, alpha_phase)
                    muls, _ = floquet_multipliers(gs, as_, q)
                    stability_grid[i, j] = max(abs(m) for m in muls)
        fig_heat = go.Figure(data=go.Heatmap(z=stability_grid.T, x=alpha_range, y=gamma_range, colorscale=[[0, '#EF4444'], [0.5, '#F59E0B'], [1, '#10B981']], colorbar=dict(title='max|λ|', tickvals=[0.5, 1, 1.5], ticktext=['Stable', 'Limite', 'Instable']), hovertemplate='γ₀=%{y:.3f}<br>α₀=%{x:.3f}<br>max|λ|=%{z:.3f}<extra></extra>'))
        fig_heat.add_trace(go.Scatter(x=[alpha0], y=[gamma0], mode='markers', name='Paramètres actuels', marker=dict(size=14, color='white', symbol='star', line=dict(width=2, color='black'))))
        fig_heat.add_hline(y=1.0, line_dash="dash", line_color="white", annotation_text="α=1", annotation_position="right")
        fig_heat.update_layout(height=500, title="Carte de stabilité - Frontière stable/instable", xaxis_title="α₀ (Accélérateur)", yaxis_title="γ₀ (Propension à consommer)", template='plotly_white')
        st.plotly_chart(fig_heat, use_container_width=True)
    
    # Section théorique
    with st.expander(" **Analyse théorique détaillée**", expanded=False):
        st.markdown("""
        ###  Théorèmes clés du document Heijman & von Mouche (2015)
        
        **Proposition 55 (Floquet, 1883)** : Le système (PSH)⁽⁰⁾ a une solution non nulle de type Floquetien (q, z) 
        **si et seulement si** z est un multiplicateur de Floquet.
        
        **Théorème 2** : Pour (PSH)⁽⁰⁾ :
        - dim(SOL⁽⁰⁾ ∩ l^∞) = somme des multiplicités algébriques des multiplicateurs **dans** 𝕋 + somme des multiplicités géométriques **sur** 𝕋
        - dim(SOL⁽⁰⁾ ∩ c₀) = somme des multiplicités algébriques des multiplicateurs **dans** 𝕋
        
        **Proposition 78** : Le produit des multiplicateurs de Floquet vérifie :
        $$\\lambda_1 \\lambda_2 \\cdots \\lambda_k = (-1)^{Mq} \\frac{v_0^{(0)} \\cdots v_{q-1}^{(0)}}{v_0^{(M)} \\cdots v_{q-1}^{(M)}}$$
        
        **Résultat XVII (Article p.10)** : Le modèle constant (SH) est shock-independent si et seulement si α = 1.
        
        **Résultat XVIII (Article p.10-11)** : Sous la Conjecture 1 (1 n'est pas multiplicateur de Floquet), 
        le modèle périodique (PSH) est shock-independent.
        """)
        
        st.latex(r"\mathcal{N} = \prod_{t=0}^{q-1} \begin{pmatrix} \gamma_t + \alpha_t & -\alpha_t \\ 1 & 0 \end{pmatrix}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.latex(r"\mathcal{N} \text{ (matrice monodromique)}")
        with col2:
            st.latex(f"\\text{{det}}(\\mathcal{{N}}) = {det_monodromy:.6f}")
            st.latex(f"\\prod \\alpha = {det_alpha_product:.6f}")
            if abs(det_monodromy - det_alpha_product) < 1e-6:
                st.success(" Vérification proposition 78: det(N) = ∏α")
            else:
                st.warning(f" Écart: {abs(det_monodromy - det_alpha_product):.2e}")
        
        st.markdown("####  Séquences périodiques utilisées")
        df_params = pd.DataFrame({'t': list(range(q)), 'γ(t)': [f"{g:.4f}" for g in gamma_seq], 'α(t)': [f"{a:.4f}" for a in alpha_seq]})
        st.dataframe(df_params, use_container_width=True)
        
        st.markdown("####  Matrice de monodromie (calculée)")
        st.code(f"N =\n{M}")