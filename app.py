from flask import Flask, request, jsonify
import numpy as np
import pandas as pd

app = Flask(__name__)

# Function to scale days to percentage
def scale_days_to_percentage(days_difference, today_value=None, min_val=5, max_val=97):
    if today_value is None:
        today_value = np.random.uniform(40, 60)

    if days_difference == 0:
        return today_value
    elif days_difference < 0:
        scale_factor = 1 - (abs(days_difference) / 3650)
        percentage = today_value * scale_factor
        return max(percentage, min_val)
    else:
        scale_factor = 1 + (days_difference / 3650)
        percentage = today_value * scale_factor
        return min(percentage, max_val)

# Flask route to handle the input date and return the pollution level
@app.route('/predict', methods=['POST'])
def predict_pollution():
    try:
        data = request.get_json()
        input_year = data.get('year')
        input_month = data.get('month')
        input_day = data.get('day')
        
        if not (input_year and input_month and input_day):
            return jsonify({'error': 'Missing year, month or day input'}), 400

        today_date = pd.Timestamp.now()
        input_date = pd.to_datetime(f'{input_year}-{input_month}-{input_day}')
        days_difference = (input_date - today_date).days

        # Get the predicted pollution level as a percentage
        predicted_pollution_percentage = scale_days_to_percentage(days_difference)

        # Return the predicted pollution level as a JSON response
        return jsonify({
            'predicted_pollution_percentage': round(predicted_pollution_percentage, 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
