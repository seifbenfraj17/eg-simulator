from flask import Flask, render_template, request
import os

app = Flask(__name__)

def calculate_capital_after_days(initial_capital, days, trades_per_day, bonus_days):
    """Calcule le capital après X jours"""
    final_capital = initial_capital
    for day in range(1, days + 1):
        daily_trades = trades_per_day
        if day <= bonus_days:
            daily_trades += 2
        daily_gain = daily_trades * 0.65 / 100
        final_capital *= (1 + daily_gain)
    return final_capital

def calculate_days_to_objective(initial_capital, objective, trades_per_day, bonus_days, max_days=365):
    """Calcule combien de jours pour atteindre un objectif"""
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
    """Calcule le capital initial pour atteindre un objectif en X jours"""
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
    """Retourne la progression chaque jour"""
    progression = []
    current_capital = initial_capital
    for day in range(1, min(days + 1, 31)):
        daily_trades = trades_per_day
        if day <= bonus_days:
            daily_trades += 2
        daily_gain = daily_trades * 0.65 / 100
        current_capital *= (1 + daily_gain)
        progression.append({
            'day': day,
            'capital': round(current_capital, 2),
            'daily_gain': round(daily_gain * 100, 2)
        })
    return progression

def compare_agent_levels(initial_capital, days, bonus_days):
    """Compare les 3 niveaux d'agent"""
    levels = {}
    for level_name, base_trades in [('LV0', 2), ('LV1', 3), ('LV2', 4)]:
        final_capital = calculate_capital_after_days(initial_capital, days, base_trades, bonus_days)
        levels[level_name] = {
            'final_capital': round(final_capital, 2),
            'gain': round(final_capital - initial_capital, 2),
            'roi': round((final_capital - initial_capital) / initial_capital * 100, 2)
        }
    return levels

def calculate_bonus_impact(initial_capital, days, trades_per_day):
    """Calcule l'impact du bonus"""
    without_bonus = calculate_capital_after_days(initial_capital, days, trades_per_day, 0)
    with_bonus = calculate_capital_after_days(initial_capital, days, trades_per_day, days)
    impact = with_bonus - without_bonus
    impact_percent = (impact / without_bonus * 100) if without_bonus > 0 else 0
    return {
        'without_bonus': round(without_bonus, 2),
        'with_bonus': round(with_bonus, 2),
        'impact': round(impact, 2),
        'impact_percent': round(impact_percent, 2)
    }

def calculate_multiple_days(initial_capital, multiple, trades_per_day, bonus_days, max_days=365):
    """Calcule en combien de jours atteindre un multiple"""
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
    """Retourne les milestones à long terme"""
    timeframes = {'1 mois': 30, '3 mois': 90, '6 mois': 180, '1 an': 365}
    milestones = {}
    for name, days in timeframes.items():
        capital = calculate_capital_after_days(initial_capital, days, trades_per_day, bonus_days)
        milestones[name] = {
            'capital': round(capital, 2),
            'gain': round(capital - initial_capital, 2)
        }
    return milestones

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    capital = 0
    use_case = 'uc1'
    
    if request.method == 'POST':
        try:
            use_case = request.form.get('use_case', 'uc1')
            agent_level = request.form.get('agent_level', 'LV0')
            has_bonus = request.form.get('has_bonus', 'no')
            bonus_days = int(request.form.get('bonus_days', 0)) if request.form.get('bonus_days') else 0
            
            trades_per_day = 2
            if agent_level == 'LV1':
                trades_per_day += 1
            elif agent_level == 'LV2':
                trades_per_day += 2
            
            if use_case == 'uc1':
                capital = float(request.form.get('capital', 1000))
                days = int(request.form.get('days', 1))
                final_capital = calculate_capital_after_days(capital, days, trades_per_day, bonus_days)
                result = {
                    'type': 'uc1',
                    'capital': capital,
                    'final_capital': round(final_capital, 2),
                    'gain': round(final_capital - capital, 2)
                }
            
            elif use_case == 'uc2':
                capital = float(request.form.get('capital', 1000))
                objective = float(request.form.get('objective', 2000))
                days_needed = calculate_days_to_objective(capital, objective, trades_per_day, bonus_days)
                result = {
                    'type': 'uc2',
                    'capital': capital,
                    'objective': objective,
                    'days_needed': days_needed,
                    'final_capital': round(calculate_capital_after_days(capital, days_needed, trades_per_day, bonus_days), 2) if days_needed else None
                }
            
            elif use_case == 'uc3':
                objective = float(request.form.get('objective', 2000))
                days = int(request.form.get('days', 30))
                initial_capital = calculate_initial_capital(objective, days, trades_per_day, bonus_days)
                result = {
                    'type': 'uc3',
                    'objective': objective,
                    'days': days,
                    'initial_capital': round(initial_capital, 2),
                    'final_capital': objective
                }
            
            elif use_case == 'uc4':
                capital = float(request.form.get('capital', 1000))
                days = int(request.form.get('days', 30))
                comparisons = compare_agent_levels(capital, days, bonus_days)
                result = {
                    'type': 'uc4',
                    'capital': capital,
                    'days': days,
                    'comparisons': comparisons
                }
            
            elif use_case == 'uc5':
                capital = float(request.form.get('capital', 1000))
                days = int(request.form.get('days', 14))
                progression = get_day_by_day_progression(capital, days, trades_per_day, bonus_days)
                result = {
                    'type': 'uc5',
                    'capital': capital,
                    'progression': progression
                }
            
            elif use_case == 'uc6':
                capital = float(request.form.get('capital', 1000))
                days = int(request.form.get('days', 30))
                impact = calculate_bonus_impact(capital, days, trades_per_day)
                result = {
                    'type': 'uc6',
                    'capital': capital,
                    'days': days,
                    'impact': impact
                }
            
            elif use_case == 'uc7':
                capital = float(request.form.get('capital', 1000))
                multiple = float(request.form.get('multiple', 2))
                days_needed = calculate_multiple_days(capital, multiple, trades_per_day, bonus_days)
                result = {
                    'type': 'uc7',
                    'capital': capital,
                    'multiple': multiple,
                    'objective': round(capital * multiple, 2),
                    'days_needed': days_needed,
                    'final_capital': round(calculate_capital_after_days(capital, days_needed, trades_per_day, bonus_days), 2) if days_needed else None
                }
            
            elif use_case == 'uc8':
                capital = float(request.form.get('capital', 1000))
                milestones = get_long_term_milestones(capital, trades_per_day, bonus_days)
                result = {
                    'type': 'uc8',
                    'capital': capital,
                    'milestones': milestones
                }
        except Exception as e:
            print(f"Error: {e}")
            result = None
    
    return render_template('index.html', result=result, capital=capital, use_case=use_case)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)
