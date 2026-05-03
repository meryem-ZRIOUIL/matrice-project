import streamlit as st

def show_home():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700&display=swap');
        
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Animation */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .animate-fade-in {
            animation: fadeIn 0.5s ease-out;
        }
        
        /* Carte */
        .card {
            transition: all 0.25s ease;
            background: var(--st-color-background);
            border: 1px solid var(--st-color-border);
            border-radius: 16px;
            padding: 1.5rem;
            height: 100%;
        }
        
        .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px -12px rgba(0,0,0,0.2);
            border-color: #3b82f6;
        }
        
        /* Badges */
        .badge-blue {
            background: rgba(59,130,246,0.12);
            color: #3b82f6;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: 500;
        }
        
        .badge-emerald {
            background: rgba(16,185,129,0.12);
            color: #10b981;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: 500;
        }
        
        .badge-amber {
            background: rgba(245,158,11,0.12);
            color: #f59e0b;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: 500;
        }
        
        /* Section fonctionnalités */
        .feature-box {
            text-align: center;
            padding: 1rem;
        }
        
        .feature-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        
        .feature-title {
            font-weight: 600;
            font-size: 0.85rem;
            margin: 0.25rem 0;
            color: var(--st-color-text-primary);
        }
        
        .feature-desc {
            font-size: 0.7rem;
            color: var(--st-color-text-secondary);
        }
        
        /* Section références */
        .ref-section {
            background: var(--st-color-background);
            border: 1px solid var(--st-color-border);
            border-radius: 16px;
            padding: 1.5rem;
            margin-top: 1rem;
        }
        
        .ref-item {
            margin: 0.5rem 0;
            font-size: 0.8rem;
            line-height: 1.4;
            color: var(--st-color-text-primary);
        }
        
        .ref-item strong {
            color: #3b82f6;
        }
        
        .ref-item em {
            color: var(--st-color-text-secondary);
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 1.5rem 0 0.5rem 0;
            color: var(--st-color-text-secondary);
            font-size: 0.65rem;
            border-top: 1px solid var(--st-color-border);
            margin-top: 1rem;
        }
        
        /* Titres */
        h1, h2, h3 {
            color: var(--st-color-text-primary);
        }
        
        p {
            color: var(--st-color-text-secondary);
        }
        
        hr {
            border-color: var(--st-color-border);
        }
        
        /* Dark mode spécifique */
        @media (prefers-color-scheme: dark) {
            .badge-blue { background: rgba(59,130,246,0.2); }
            .badge-emerald { background: rgba(16,185,129,0.2); }
            .badge-amber { background: rgba(245,158,11,0.2); }
        }
    </style>
    """, unsafe_allow_html=True)

    # =========================================================
    # BANNIÈRE PRINCIPALE
    # =========================================================
    st.markdown("""
    <div class="animate-fade-in" style="text-align: center; padding: 1rem 0 2rem 0;">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;"></div>
        <h1 style="font-size: 2rem; font-weight: 700; margin: 0.5rem 0;">Simulation des objets matriciels</h1>
        <p style="font-size: 0.9rem; max-width: 600px; margin: 0.5rem auto;">Simulation interactive de trois articles scientifiques majeurs</p>
        <div style="display: flex; justify-content: center; gap: 8px; margin-top: 1rem; flex-wrap: wrap;">
            <span class="badge-blue">Floquet Theory</span>
            <span class="badge-emerald">Matrices compagnons</span>
            <span class="badge-amber">Fibonacci généralisée</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================================================
    # CARTES DES 3 ARTICLES
    # =========================================================
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown("""
        <div class="card">
            <div style="text-align: center; margin-bottom: 1rem;">
            </div>
            <h3 style="text-align: center; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.25rem;">Floquet Theory</h3>
            <p style="text-align: center; font-size: 0.7rem; color: #3b82f6; margin-bottom: 1rem;">Heijman &amp; von Mouche (2015)</p>
            <div style="height: 1px; background: var(--st-color-border); margin: 1rem 0;"></div>
            <div style="margin-top: 0.5rem;">
                <p style="margin: 0.4rem 0; font-size: 0.8rem;">▸ Modèle de Samuelson-Hicks périodique</p>
                <p style="margin: 0.4rem 0; font-size: 0.8rem;">▸ Matrice monodromique et multiplicateurs</p>
                <p style="margin: 0.4rem 0; font-size: 0.8rem;">▸ Analyse de stabilité (cercle unité)</p>
                <p style="margin: 0.4rem 0; font-size: 0.8rem;">▸ Shock-dependency (Résultats XVII, XVIII)</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div style="text-align: center; margin-bottom: 1rem;">
            </div>
            <h3 style="text-align: center; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.25rem;">BBR</h3>
            <p style="text-align: center; font-size: 0.7rem; color: #10b981; margin-bottom: 1rem;">Benkhaldoun, Ben Taher &amp; Rachidi (2021)</p>
            <div style="height: 1px; background: var(--st-color-border); margin: 1rem 0;"></div>
            <div style="margin-top: 0.5rem;">
                <p style="margin: 0.4rem 0; font-size: 0.8rem;">▸ Matrices compagnons en blocs</p>
                <p style="margin: 0.4rem 0; font-size: 0.8rem;">▸ Produit de matrices (ordre correct)</p>
                <p style="margin: 0.4rem 0; font-size: 0.8rem;">▸ Matrice monodromique et valeurs propres</p>
                <p style="margin: 0.4rem 0; font-size: 0.8rem;">▸ Dynamique Y(n+1) = P × Y(n)</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
            <div style="text-align: center; margin-bottom: 1rem;">
            </div>
            <h3 style="text-align: center; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.25rem;">Rachidi</h3>
            <p style="text-align: center; font-size: 0.7rem; color: #f59e0b; margin-bottom: 1rem;">Rachidi (2025)</p>
            <div style="height: 1px; background: var(--st-color-border); margin: 1rem 0;"></div>
            <div style="margin-top: 0.5rem;">
                <p style="margin: 0.4rem 0; font-size: 0.8rem;">▸ Matrice compagnon et puissance Aⁿ</p>
                <p style="margin: 0.4rem 0; font-size: 0.8rem;">▸ Suite de Fibonacci généralisée</p>
                <p style="margin: 0.4rem 0; font-size: 0.8rem;">▸ Formule de Binet généralisée</p>
                <p style="margin: 0.4rem 0; font-size: 0.8rem;">▸ Vérification numérique matriciel vs récurrence</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # =========================================================
    # SECTION FONCTIONNALITÉS
    # =========================================================
    st.markdown("""
    <div style="text-align: center; margin: 1rem 0 1.5rem 0;">
        <div style="display: inline-block; background: #3b82f6; padding: 4px 20px; border-radius: 30px; margin-bottom: 0.75rem;">
            <span style="color: white; font-weight: 600; font-size: 0.7rem; letter-spacing: 1px;">FONCTIONNALITES</span>
        </div>
        <h2 style="font-size: 1.3rem; font-weight: 600; margin: 0.5rem 0;">Experience interactive complete</h2>
        <p style="font-size: 0.85rem; max-width: 500px; margin: 0.25rem auto;">Tous les outils pour explorer et analyser</p>
    </div>
    """, unsafe_allow_html=True)

    col_f1, col_f2, col_f3, col_f4 = st.columns(4)

    with col_f1:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon"></div>
            <div class="feature-title">Export CSV</div>
            <div class="feature-desc">Données téléchargeables</div>
        </div>
        """, unsafe_allow_html=True)

    with col_f2:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon"></div>
            <div class="feature-title">Heatmap interactive</div>
            <div class="feature-desc">Carte de stabilité</div>
        </div>
        """, unsafe_allow_html=True)

    with col_f3:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon"></div>
            <div class="feature-title">Animation temporelle</div>
            <div class="feature-desc">Évolution pas à pas</div>
        </div>
        """, unsafe_allow_html=True)

    with col_f4:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon"></div>
            <div class="feature-title">Vérification numérique</div>
            <div class="feature-desc">Matriciel vs récurrence</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # =========================================================
    # SECTION RÉFÉRENCES
    # =========================================================
    st.markdown("""
    <div class="ref-section">
        <div style="text-align: center; margin-bottom: 0.75rem;">
            <h3 style="font-size: 1.1rem; font-weight: 600;">References bibliographiques</h3>
        </div>
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 1rem;">
            <div style="flex: 1;">
                <div class="ref-item">
                    <strong>Heijman, W. &amp; von Mouche, P. (2015).</strong><br>
                    <em>Floquet theory and economic dynamics II</em> — Wageningen UR
                </div>
                <div class="ref-item" style="margin-top: 0.75rem;">
                    <strong>Benkhaldoun, H., Ben Taher, R. &amp; Rachidi, M. (2021).</strong><br>
                    <em>Periodic matrix difference equations</em> — Arabian J. Math.
                </div>
            </div>
            <div style="flex: 1;">
                <div class="ref-item">
                    <strong>Rachidi, M. (2025).</strong><br>
                    <em>Powers of Companion Matrix via Linear Recursiveness</em> — BSPM
                </div>
                <div class="ref-item" style="margin-top: 0.75rem;">
                    <strong>Floquet, G. (1883).</strong><br>
                    <em>Sur les equations differentielles lineaires a coefficients periodiques</em>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================================================
    # FOOTER
    # =========================================================
    st.markdown("""
    <div class="footer">
        Floquet Theory Suite — Heijman &amp; von Mouche (2015) · BBR (2021) · Rachidi (2025)
    </div>
    """, unsafe_allow_html=True)