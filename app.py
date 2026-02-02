from flask import Flask, render_template, request, jsonify
import sys
sys.path.append('src')
from predictor import predict_post_performance, compare_post_types
from text_predictor import predict_from_text

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

@app.route('/predict-text', methods=['POST'])
def predict_text():
    try:
        data = request.json
        post_text = data.get('post_text', '')
        post_type = data.get('post_type', 'Text')
        
        if not post_text or len(post_text.strip()) < 10:
            return jsonify({
                'success': False,
                'error': 'Post text is too short. Please enter at least 10 characters.'
            }), 400
        
        result = predict_from_text(post_text, post_type)
        
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

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'LinkedIn Post Predictor',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

