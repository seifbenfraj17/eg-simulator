from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    capital = 0
    
    if request.method == 'POST':
        capital = float(request.form.get('capital', 1000))
        days = int(request.form.get('days', 1))
        agent_level = request.form.get('agent_level', 'LV0')
        has_bonus = request.form.get('has_bonus', 'no')
        bonus_days = int(request.form.get('bonus_days', 0))

        # Base trades per day
        trades_per_day = 2
        if agent_level == 'LV1':
            trades_per_day += 1
        elif agent_level == 'LV2':
            trades_per_day += 2

        final_capital = capital
        for day in range(1, days + 1):
            daily_trades = trades_per_day
            if has_bonus == 'yes' and day <= bonus_days:
                daily_trades += 2
            daily_gain = daily_trades * 0.65 / 100
            final_capital *= (1 + daily_gain)
        result = round(final_capital, 2)
    return render_template('index.html', result=result, capital=capital)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)
