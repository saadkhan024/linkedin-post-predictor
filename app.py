from flask import Flask, render_template, request, jsonify
import sys
sys.path.append('src')
from predictor import predict_post_performance, compare_post_types

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        result = predict_post_performance(
            post_type=data.get('post_type', 'Video'),
            month=data.get('month', 'February'),
            impressions=int(data.get('impressions', 5000)),
            reach=int(data.get('reach', 6000)),
            clicks=int(data.get('clicks', 400))
        )
        
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/compare', methods=['POST'])
def compare():
    try:
        data = request.json
        
        comparison = compare_post_types(
            month=data.get('month', 'February'),
            impressions=int(data.get('impressions', 5000)),
            reach=int(data.get('reach', 6000)),
            clicks=int(data.get('clicks', 400))
        )
        
        return jsonify({
            'success': True,
            'comparison': comparison.to_dict(orient='records')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

