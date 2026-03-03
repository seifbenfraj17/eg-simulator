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
    return None  # Objectif non atteint dans 365 jours

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    capital = 0
    use_case = 'uc1'  # Use case sélectionné
    
    if request.method == 'POST':
        use_case = request.form.get('use_case', 'uc1')
        agent_level = request.form.get('agent_level', 'LV0')
        has_bonus = request.form.get('has_bonus', 'no')
        bonus_days = int(request.form.get('bonus_days', 0))
        
        # Base trades per day
        trades_per_day = 2
        if agent_level == 'LV1':
            trades_per_day += 1
        elif agent_level == 'LV2':
            trades_per_day += 2
        
        if use_case == 'uc1':
            # Use Case 1 : Calculer les gains après X jours
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
            # Use Case 2 : Calculer jours pour atteindre un objectif
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
    
    return render_template('index.html', result=result, capital=capital, use_case=use_case)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)
