# 💰 EG Simulator - Streamlit Edition

Une belle application web pour simuler les gains en trading avec bonus d'agent.

## 🚀 Déployer sur Streamlit Cloud

### Option 1: Déploiement automatique (Recommandé)

1. Allez sur [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Cliquez sur **"New app"**
3. Sélectionnez:
   - **Repository**: `seifbenfraj17/eg-simulator`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
4. Cliquez sur **"Deploy"**

✅ Voilà! L'app se déploiera automatiquement en quelques secondes et vous recevrez une URL publique.

### Option 2: Liens des déploiements

- **Streamlit Cloud** (GRATUIT, illimité): [Version Streamlit]()
- **Railway** (25 jours gratuits): [Version Flask](https://eg-simulator.railway.app)

## 📊 Features

### 8 Cas d'utilisation
1. **📈 Gains X jours** - Calculez vos gains après X jours
2. **🎯 Atteindre objectif** - Combien de jours pour atteindre votre objectif ?
3. **💼 Capital initial** - Quel capital initial pour atteindre votre objectif ?
4. **⚙️ Comparer niveaux** - Comparez les 3 niveaux d'agent (LV0, LV1, LV2)
5. **📊 Progression** - Voir la progression jour par jour avec graphique
6. **⚡ Impact bonus** - Analysez l'impact du bonus sur vos gains
7. **🔢 Multiples** - Combien de jours pour multiplier votre capital ?
8. **🏆 Long terme** - Prévisions long terme (3 mois, 6 mois, 1 an, 5 ans)

### Design
- ✨ Gradient violet premium (#667eea → #764ba2)
- 🎨 Interface moderne avec animations fluides
- 📱 Responsive sur desktop et mobile
- 🌙 Dark mode optimisé
- 📊 Graphiques interactifs avec Plotly

### Modèle de calcul
- **Base**: 2 trades/jour = 0.65% gain/trade
- **LV1**: +1 trade (3 total)
- **LV2**: +2 trades (4 total)
- **Bonus**: +2 trades/jour pendant X jours

## 💻 Installation locale

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

L'app s'ouvrira sur `http://localhost:8501`

## 📁 Structure

```
EG Simulator/
├── streamlit_app.py      # App Streamlit (version moderne)
├── app.py                # App Flask (ancienne version)
├── requirements.txt      # Dépendances Python
├── .streamlit/
│   └── config.toml      # Configuration Streamlit
└── README.md
```

## 🔧 Stack technique

- **Frontend**: Streamlit + Custom CSS + Plotly
- **Backend**: Python (functions pures)
- **Déploiement**: Streamlit Cloud (gratuit) ou Railway
- **Hosting**: Gratuit et illimité sur Streamlit Cloud

## 📝 Calculs

### Capital après X jours
```
final_capital = initial_capital × (1 + (trades × 0.65%))^jours
```

Avec bonus les premiers jours:
```
daily_trades = base_trades + bonus_trades (si day ≤ bonus_days)
```

## ⚠️ Disclaimer

Ceci est un simulateur éducatif pour comprendre la croissance composée. Les résultats réels peuvent varier significativement en fonction des conditions du marché et d'autres facteurs.

## 📧 Questions?

N'hésitez pas à créer une issue sur GitHub!

---

**Version**: 2.0 (Streamlit Edition)  
**Dernière mise à jour**: Mar 9, 2026
