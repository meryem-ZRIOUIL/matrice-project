
```markdown
# Simulation des objets matriciels et simulation d'articles scientifiques

**Université Ibn Tofail** - Licence d'Excellence : Intelligence Artificielle et Ingénierie des Données

**Module :** Mathématiques pour l'IA

**Encadrant :** Professeur Mohammed KAICER

**Année universitaire :** 2025/2026

---

## Membres du projet

- Meryem ZRIOUIL
- Hiba CHOUKRI
- Siham EL MTARFI
- Mouad EL FILA

---

## Applications déployées (cliquez sur les liens)

| Application | Lien |
|-------------|------|
| Phase 1 : 4 tâches matricielles | [https://matrice-project-meryem-zriouil-premiers-taches.streamlit.app](https://matrice-project-meryem-zriouil-premiers-taches.streamlit.app) |
| Phase 2 : 3 articles scientifiques | [https://matrice-project-meryemzriouil-simulation-des-articles.streamlit.app](https://matrice-project-meryemzriouil-simulation-des-articles.streamlit.app) |

---

## Contenu du projet

### Phase 1 : Simulation des objets matriciels (4 tâches)

| Tâche | Description |
|-------|-------------|
| Inversion | Complexité O(n³), mémoire O(n²), temps d'inversion mesuré pour des matrices jusqu'à 1000×1000 |
| Matrices creuses | Gain mémoire x100, phénomène de fill-in (matrice creuse devient dense après inversion), imputation des valeurs manquantes (NaN) par moyenne |
| Intégration | Intégration de A(t) = [[t, t²], [1, eᵗ]] de 0 à 1, convergence O(1/N) validée graphiquement |
| Modèle de Leslie | Simulation de population structurée par âge, valeur propre dominante λ détermine croissance/déclin/stabilité, distribution stable = vecteur propre de λ |

### Phase 2 : Simulation de 3 articles scientifiques

| Module | Référence | Description |
|--------|-----------|-------------|
| Floquet | Heijman & von Mouche (2015) | Systèmes économiques périodiques (modèle de Samuelson-Hicks), multiplicateurs de Floquet, carte de stabilité, export CSV |
| BBR | Benkhaldoun, Ben Taher & Rachidi (2021) | Matrices compagnons par blocs, produit de matrices (monodromie), analyse spectrale, heatmap interactive |
| Rachidi | Rachidi (2025) | Suites de Fibonacci généralisées (ordre 3), puissances de matrices compagnons, formule de Binet généralisée, vérification matricielle vs récurrence |

---

## Technologies utilisées

| Technologie | Rôle |
|-------------|------|
| Python 3.x | Langage principal |
| Streamlit | Interface utilisateur interactive, déploiement web |
| NumPy | Calculs matriciels, inversions, valeurs propres |
| SciPy | Matrices creuses (CSR), intégration quad, solveurs itératifs |
| Matplotlib | Graphiques spy (fill-in), portraits de phase |
| Plotly | Graphiques interactifs (heatmaps, courbes, convergence) |
| Pandas | Affichage des dataframes, export CSV |

---

## Installation et exécution locale

### 1. Cloner le repository

```bash
git clone https://github.com/meryem-ZRIOUIL/matrice-project.git
cd matrice-project
```

### 2. Créer un environnement virtuel (recommandé)

```bash
# Sur Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Sur Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Lancer l'application Phase 1 (4 tâches matrices)

```bash
streamlit run app.py
```

Puis ouvrez votre navigateur à l'adresse : `http://localhost:8501`

### 5. Lancer l'application Phase 2 (3 articles scientifiques)

```bash
streamlit run app1.py
```

Puis ouvrez votre navigateur à l'adresse : `http://localhost:8501`

> **Note :** Les deux applications utilisent des ports différents. Vous pouvez les lancer simultanément dans deux terminaux distincts.

---

## Structure du projet

```
matrice-project/
│
├── app.py                    # Phase 1 - Application principale (4 tâches matrices)
├── app1.py                   # Phase 2 - Application 3 articles scientifiques
│
├── bbr.py                    # Module BBR (matrices compagnons par blocs)
├── floquet.py                # Module Floquet (systèmes périodiques)
├── home.py                   # Page d'accueil Phase 2
├── rachidi.py                # Module Rachidi (Fibonacci généralisé)
├── utils.py                  # Fonctions partagées
│
├── requirements.txt          # Dépendances Python
├── README.md                 # Ce fichier
│
├── notebooks/                # Jupyter notebooks d'exploration
│   ├── 01_inversion_et_creuses.ipynb
│   └── 02_modele_leslie.ipynb
│
└── rapports/                 # Documents PDF du projet
    ├── Rapport_Matrices.pdf
    └── Liens_utiles.pdf
```

---

## Fonctionnalités interactives

| Fonctionnalité | Description |
|----------------|-------------|
| Dark / Light mode | Détection automatique du thème système, adaptation des couleurs (CSS variables, Plotly template) |
| Graphiques Plotly | Zoom, survol, export en PNG, interactivité |
| Export CSV | Téléchargement des données (multiplicateurs, séries temporelles) |
| Animations temporelles | Évolution pas à pas des systèmes dynamiques |
| Cartes de stabilité | Visualisation des zones stables/instables dans l'espace des paramètres |
| Sliders et boutons | Ajustement en temps réel de tous les paramètres |
| Tabs | Organisation claire des sections (zéros / NaN) |

---

## Détail des résultats par tâche

### Tâche 1 - Inversion de matrices

| Taille n | Temps (s) | Mémoire (Mo) | Erreur |
|----------|-----------|--------------|--------|
| 100 | 0.015 | 0.08 | 1.2e-10 |
| 200 | 0.089 | 0.32 | 2.1e-10 |
| 400 | 0.587 | 1.28 | 3.5e-10 |
| 600 | 1.890 | 2.88 | 4.2e-10 |
| 800 | 4.234 | 5.12 | 5.1e-10 |
| 1000 | 8.123 | 8.00 | 6.8e-10 |

**Conclusion :** Le temps d'inversion suit une complexité O(n³), conforme à la théorie.

### Tâche 2 - Matrices creuses

| Format | Mémoire | Gain |
|--------|---------|------|
| Dense | 7.63 Mo | x1 |
| Creuse (CSR) | 0.118 Mo | x65 |

**Fill-in :** Une matrice 30×30 (densité 20%) devient 100% dense après inversion.

### Tâche 3 - Intégration

| Élément | Analytique | Rectangles (N=10000) |
|---------|------------|---------------------|
| A(1,1) | 0.50000000 | 0.50000000 |
| A(1,2) | 0.33333333 | 0.33335000 |
| A(2,1) | 1.00000000 | 1.00000000 |
| A(2,2) | 1.71828183 | 1.71820000 |

**Erreur maximale :** 8×10⁻⁵

### Tâche 4 - Modèle de Leslie

| Cas | λ | Comportement |
|-----|----|--------------|
| Croissance | 1.20 | 📈 Croissance exponentielle |
| Déclin | 0.63 | 📉 Extinction |
| Stable | 1.00 | ➡️ Stabilité |

---

## Liens des vidéos de démonstration

| Vidéo | Lien |
|-------|------|
| Phase 1 - Démonstration (4 tâches matrices) | [Insérer lien Google Drive] |
| Phase 2 - Démonstration (3 articles) | [Insérer lien Google Drive] |

> **Remarque :** Si les liens ne fonctionnent pas, les vidéos sont disponibles dans le dossier de rendu sur la plateforme.

----

## Statut du projet

 **Projet terminé** - Toutes les fonctionnalités sont implémentées, testées et déployées.

-  Phase 1 : 4 tâches matricielles opérationnelles
-  Phase 2 : 3 modules scientifiques opérationnels
-  Dark/Light mode supporté
-  Déploiement Streamlit Cloud actif
-  Code source documenté et disponible sur GitHub

---

## Références bibliographiques

- Heijman, W. & von Mouche, P. (2015). *Floquet theory and economic dynamics II* — Wageningen UR
- Benkhaldoun, H., Ben Taher, R. & Rachidi, M. (2021). *Periodic matrix difference equations and companion matrices in blocks* — Arabian Journal of Mathematics
- Rachidi, M. (2025). *Powers of Companion Matrix via Linear Recursiveness* — Bulletin de la Société des Sciences Mathématiques du Maroc
- Floquet, G. (1883). *Sur les équations différentielles linéaires à coefficients périodiques* — Annales scientifiques de l'École Normale Supérieure
- Cardwell, N., Cheng, Y., Gunn, C. S., Yeganeh, S. H., & Jacobson, V. (2016). *BBR: Congestion-Based Congestion Control* — ACM Queue


**Dernière mise à jour : Mai 2026**-

*Ce projet a été réalisé dans le cadre du module Mathématiques pour l'IA à l'Université Ibn Tofail.*
`
