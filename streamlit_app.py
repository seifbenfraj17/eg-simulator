import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ============= CONFIGURATION =============
st.set_page_config(
    page_title="🚀 EG Simulator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    [data-testid="stMainBlockContainer"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding-top: 2rem;
    }
    
    .main {
        color: white;
    }
    
    h1, h2, h3 {
        color: white;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    [data-testid="stVerticalBlock"] {
        gap: 1.5rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background-color: rgba(255,255,255,0.1);
        padding: 0.5rem;
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        color: white;
        background-color: rgba(255,255,255,0.2);
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255,255,255,0.3);
        transform: translateY(-2px);
    }
    
    [aria-selected="true"] {
        background-color: rgba(255,255,255,0.9) !important;
        color: #667eea !important;
    }
    
    .stMetric {
        background-color: rgba(255,255,255,0.1);
        padding: 1.5rem;
        border-radius: 12px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        background-color: rgba(255,255,255,0.15);
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .card {
        background-color: rgba(255,255,255,0.1);
        padding: 2rem;
        border-radius: 12px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .stButton > button {
        background-color: rgba(255,255,255,0.9);
        color: #667eea;
        font-weight: 600;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: white;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    }
    
    .stNumberInput, .stSelectbox {
        color: white;
    }
    
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background-color: rgba(255,255,255,0.1) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 8px !important;
    }
    
    .result-container {
        background-color: rgba(255,255,255,0.15);
        padding: 2rem;
        border-radius: 12px;
        border: 2px solid rgba(255,255,255,0.3);
        margin-top: 2rem;
        animation: slideUp 0.5s ease-out;
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #4ade80;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.8);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

# ============= CALCULATION FUNCTIONS =============
def calculate_capital_after_days(initial_capital, days, trades_per_day, bonus_days):
    final_capital = initial_capital
    for day in range(1, days + 1):
        daily_trades = trades_per_day
        if day <= bonus_days:
            daily_trades += 2
        daily_gain = daily_trades * 0.65 / 100
        final_capital *= (1 + daily_gain)
    return final_capital

def calculate_days_to_objective(initial_capital, objective, trades_per_day, bonus_days, max_days=365):
    current_capital = initial_capital
    for day in range(1, max_days + 1):
        daily_trades = trades_per_day
        if day <= bonus_days:
            daily_trades += 2
        daily_gain = daily_trades * 0.65 / 100
        current_capital *= (1 + daily_gain)
        if current_capital >= objective:
            return day
    return None

def calculate_initial_capital(objective, days, trades_per_day, bonus_days):
    daily_gain_factor = 1.0
    for day in range(1, days + 1):
        daily_trades = trades_per_day
        if day <= bonus_days:
            daily_trades += 2
        daily_gain = daily_trades * 0.65 / 100
        daily_gain_factor *= (1 + daily_gain)
    initial_capital = objective / daily_gain_factor if daily_gain_factor > 0 else 0
    return initial_capital

def get_day_by_day_progression(initial_capital, days, trades_per_day, bonus_days):
    progression = []
    current_capital = initial_capital
    for day in range(1, min(days + 1, 31)):
        daily_trades = trades_per_day
        if day <= bonus_days:
            daily_trades += 2
        daily_gain = daily_trades * 0.65 / 100
        current_capital *= (1 + daily_gain)
        progression.append({
            'Jour': day,
            'Capital': round(current_capital, 2),
            'Gain quotidien %': round(daily_gain * 100, 3)
        })
    return progression

def compare_agent_levels(initial_capital, days, bonus_days):
    levels = {}
    for level_name, base_trades in [('LV0', 2), ('LV1', 3), ('LV2', 4)]:
        final_capital = calculate_capital_after_days(initial_capital, days, base_trades, bonus_days)
        levels[level_name] = {
            'Capital final': round(final_capital, 2),
            'Gain': round(final_capital - initial_capital, 2),
            'ROI %': round((final_capital - initial_capital) / initial_capital * 100, 2)
        }
    return levels

def calculate_bonus_impact(initial_capital, days, trades_per_day):
    without_bonus = calculate_capital_after_days(initial_capital, days, trades_per_day, 0)
    with_bonus = calculate_capital_after_days(initial_capital, days, trades_per_day, days)
    impact = with_bonus - without_bonus
    impact_percent = (impact / without_bonus * 100) if without_bonus > 0 else 0
    return {
        'Sans bonus': round(without_bonus, 2),
        'Avec bonus': round(with_bonus, 2),
        'Impact $': round(impact, 2),
        'Impact %': round(impact_percent, 2)
    }

def calculate_multiple_days(initial_capital, multiple, trades_per_day, bonus_days, max_days=365):
    objective = initial_capital * multiple
    current_capital = initial_capital
    for day in range(1, max_days + 1):
        daily_trades = trades_per_day
        if day <= bonus_days:
            daily_trades += 2
        daily_gain = daily_trades * 0.65 / 100
        current_capital *= (1 + daily_gain)
        if current_capital >= objective:
            return day
    return None

def get_long_term_milestones(initial_capital, trades_per_day, bonus_days):
    timeframes = {'3 mois': 90, '6 mois': 180, '1 an': 365, '5 ans': 1825}
    milestones = {}
    for name, days in timeframes.items():
        capital = calculate_capital_after_days(initial_capital, days, trades_per_day, bonus_days)
        milestones[name] = {
            'Capital': round(capital, 2),
            'Gain': round(capital - initial_capital, 2)
        }
    return milestones

# ============= HEADER =============
st.markdown("""
<div style="text-align: center; margin-bottom: 3rem;">
    <h1 style="font-size: 3.5rem; margin-bottom: 0.5rem;">💰 EG Simulator</h1>
    <p style="font-size: 1.2rem; color: rgba(255,255,255,0.85);">Simulez vos gains en trading avec bonus d'agent</p>
</div>
""", unsafe_allow_html=True)

# ============= TABS =============
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📈 Gains X jours",
    "🎯 Atteindre objectif",
    "💼 Capital initial",
    "⚙️ Comparer niveaux",
    "📊 Progression",
    "⚡ Impact bonus",
    "🔢 Multiples",
    "🏆 Long terme"
])

# ============= TAB 1: GAINS X JOURS =============
with tab1:
    st.markdown("### 📈 Calculez vos gains après X jours")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        cap1 = st.number_input("Capital initial", min_value=100, value=1000, key="uc1_capital")
    with col2:
        days1 = st.number_input("Nombre de jours", min_value=1, value=14, key="uc1_days")
    with col3:
        level1 = st.selectbox("Niveau agent", ["LV0", "LV1", "LV2"], key="uc1_level")
    with col4:
        bonus1 = st.number_input("Jours de bonus", min_value=0, value=0, key="uc1_bonus")
    
    if st.button("Calculer gains", key="btn1"):
        trades = 2 + (1 if level1 == "LV1" else 2 if level1 == "LV2" else 0)
        final = calculate_capital_after_days(cap1, days1, trades, bonus1)
        gain = final - cap1
        roi = (gain / cap1) * 100
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💵 Capital final", f"${final:.2f}", f"+${gain:.2f}")
        with col2:
            st.metric("📊 ROI", f"{roi:.2f}%")
        with col3:
            st.metric("📈 Revenus", f"${gain:.2f}")

# ============= TAB 2: ATTEINDRE OBJECTIF =============
with tab2:
    st.markdown("### 🎯 Combien de jours pour atteindre votre objectif ?")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        cap2 = st.number_input("Capital initial", min_value=100, value=1000, key="uc2_capital")
    with col2:
        obj2 = st.number_input("Objectif ($)", min_value=100, value=5000, key="uc2_obj")
    with col3:
        level2 = st.selectbox("Niveau agent", ["LV0", "LV1", "LV2"], key="uc2_level")
    with col4:
        bonus2 = st.number_input("Jours de bonus", min_value=0, value=0, key="uc2_bonus")
    
    if st.button("Calculer", key="btn2"):
        trades = 2 + (1 if level2 == "LV1" else 2 if level2 == "LV2" else 0)
        days_needed = calculate_days_to_objective(cap2, obj2, trades, bonus2)
        
        if days_needed:
            final = calculate_capital_after_days(cap2, days_needed, trades, bonus2)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("⏰ Jours requis", f"{days_needed} j")
            with col2:
                st.metric("💵 Capital final", f"${final:.2f}")
            with col3:
                st.metric("✅ Objectif", f"${obj2:.2f}")
        else:
            st.error("❌ Impossible d'atteindre l'objectif en 365 jours")

# ============= TAB 3: CAPITAL INITIAL =============
with tab3:
    st.markdown("### 💼 Quel capital initial pour atteindre votre objectif ?")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        obj3 = st.number_input("Objectif ($)", min_value=100, value=10000, key="uc3_obj")
    with col2:
        days3 = st.number_input("Nombre de jours", min_value=1, value=30, key="uc3_days")
    with col3:
        level3 = st.selectbox("Niveau agent", ["LV0", "LV1", "LV2"], key="uc3_level")
    with col4:
        bonus3 = st.number_input("Jours de bonus", min_value=0, value=0, key="uc3_bonus")
    
    if st.button("Calculer", key="btn3"):
        trades = 2 + (1 if level3 == "LV1" else 2 if level3 == "LV2" else 0)
        initial = calculate_initial_capital(obj3, days3, trades, bonus3)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏦 Capital initial", f"${initial:.2f}")
        with col2:
            st.metric("📅 Durée", f"{days3} j")
        with col3:
            st.metric("🎯 Objectif", f"${obj3:.2f}")

# ============= TAB 4: COMPARER NIVEAUX =============
with tab4:
    st.markdown("### ⚙️ Comparez les niveaux d'agent")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        cap4 = st.number_input("Capital initial", min_value=100, value=1000, key="uc4_capital")
    with col2:
        days4 = st.number_input("Nombre de jours", min_value=1, value=30, key="uc4_days")
    with col3:
        bonus4 = st.number_input("Jours de bonus", min_value=0, value=0, key="uc4_bonus")
    
    if st.button("Comparer", key="btn4"):
        levels = compare_agent_levels(cap4, days4, bonus4)
        
        col1, col2, col3 = st.columns(3)
        for idx, (level, data) in enumerate(levels.items()):
            with [col1, col2, col3][idx]:
                st.markdown(f"### {level}")
                st.metric("Capital final", f"${data['Capital final']:.2f}")
                st.metric("Gain", f"${data['Gain']:.2f}")
                st.metric("ROI", f"{data['ROI %']:.2f}%")

# ============= TAB 5: PROGRESSION =============
with tab5:
    st.markdown("### 📊 Voir la progression jour par jour")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        cap5 = st.number_input("Capital initial", min_value=100, value=1000, key="uc5_capital")
    with col2:
        days5 = st.number_input("Nombre de jours", min_value=1, value=14, key="uc5_days")
    with col3:
        level5 = st.selectbox("Niveau agent", ["LV0", "LV1", "LV2"], key="uc5_level")
    with col4:
        bonus5 = st.number_input("Jours de bonus", min_value=0, value=0, key="uc5_bonus")
    
    if st.button("Afficher progression", key="btn5"):
        trades = 2 + (1 if level5 == "LV1" else 2 if level5 == "LV2" else 0)
        progression = get_day_by_day_progression(cap5, days5, trades, bonus5)
        
        df = pd.DataFrame(progression)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Jour'], y=df['Capital'], mode='lines+markers',
                                 name='Capital', fill='tozeroy',
                                 line=dict(color='#4ade80', width=3),
                                 marker=dict(size=8)))
        fig.update_layout(
            title="Évolution du capital",
            xaxis_title="Jour",
            yaxis_title="Capital ($)",
            hovermode='x unified',
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255,255,255,0.05)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)

# ============= TAB 6: IMPACT BONUS =============
with tab6:
    st.markdown("### ⚡ Analysez l'impact du bonus")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        cap6 = st.number_input("Capital initial", min_value=100, value=1000, key="uc6_capital")
    with col2:
        days6 = st.number_input("Nombre de jours", min_value=1, value=30, key="uc6_days")
    with col3:
        level6 = st.selectbox("Niveau agent", ["LV0", "LV1", "LV2"], key="uc6_level")
    
    if st.button("Analyser", key="btn6"):
        trades = 2 + (1 if level6 == "LV1" else 2 if level6 == "LV2" else 0)
        impact = calculate_bonus_impact(cap6, days6, trades)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Sans bonus", f"${impact['Sans bonus']:.2f}")
        with col2:
            st.metric("Avec bonus", f"${impact['Avec bonus']:.2f}")
        with col3:
            st.metric("Impact $", f"${impact['Impact $']:.2f}")
        with col4:
            st.metric("Impact %", f"{impact['Impact %']:.2f}%")

# ============= TAB 7: MULTIPLES =============
with tab7:
    st.markdown("### 🔢 Combien de jours pour multiplier votre capital ?")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        cap7 = st.number_input("Capital initial", min_value=100, value=1000, key="uc7_capital")
    with col2:
        mult7 = st.number_input("Multiplicateur (x)", min_value=1.0, value=2.0, step=0.5, key="uc7_mult")
    with col3:
        level7 = st.selectbox("Niveau agent", ["LV0", "LV1", "LV2"], key="uc7_level")
    with col4:
        bonus7 = st.number_input("Jours de bonus", min_value=0, value=0, key="uc7_bonus")
    
    if st.button("Calculer", key="btn7"):
        trades = 2 + (1 if level7 == "LV1" else 2 if level7 == "LV2" else 0)
        days_needed = calculate_multiple_days(cap7, mult7, trades, bonus7)
        objective = cap7 * mult7
        
        if days_needed:
            final = calculate_capital_after_days(cap7, days_needed, trades, bonus7)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("⏰ Jours requis", f"{days_needed} j")
            with col2:
                st.metric("🎯 Objectif", f"${objective:.2f}")
            with col3:
                st.metric("✅ Atteint", f"${final:.2f}")
        else:
            st.error("❌ Impossible d'atteindre ce multiple")

# ============= TAB 8: LONG TERME =============
with tab8:
    st.markdown("### 🏆 Prévisions long terme")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        cap8 = st.number_input("Capital initial", min_value=100, value=1000, key="uc8_capital")
    with col2:
        level8 = st.selectbox("Niveau agent", ["LV0", "LV1", "LV2"], key="uc8_level")
    with col3:
        bonus8 = st.number_input("Jours de bonus", min_value=0, value=0, key="uc8_bonus")
    
    if st.button("Afficher prévisions", key="btn8"):
        trades = 2 + (1 if level8 == "LV1" else 2 if level8 == "LV2" else 0)
        milestones = get_long_term_milestones(cap8, trades, bonus8)
        
        col1, col2, col3, col4 = st.columns(4)
        for idx, (timeframe, data) in enumerate(milestones.items()):
            with [col1, col2, col3, col4][idx]:
                st.markdown(f"### {timeframe}")
                st.metric("Capital", f"${data['Capital']:.2f}")
                st.metric("Gain", f"${data['Gain']:.2f}")

# ============= FOOTER =============
st.markdown("""
---
<div style="text-align: center; margin-top: 3rem; padding: 2rem; color: rgba(255,255,255,0.7);">
    <p>🚀 EG Simulator v2.0 - Streamlit Edition | Dernière mise à jour: Mar 9, 2026</p>
    <p style="font-size: 0.85rem;">Disclaimer: Ceci est un simulateur éducatif. Les résultats réels peuvent varier.</p>
</div>
""", unsafe_allow_html=True)
