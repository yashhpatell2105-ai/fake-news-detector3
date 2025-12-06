from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from fake_news_detector import FakeNewsDetector

app = Flask(__name__)
CORS(app)

# Initialize the detector
detector = FakeNewsDetector()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/verify', methods=['POST'])
def verify_news():
    try:
        data = request.json
        article_text = data.get('text', '')
        source_url = data.get('source_url', '')
        
        if not article_text:
            return jsonify({'error': 'Article text is required'}), 400
        
        # Perform comprehensive analysis
        result = detector.analyze(article_text, source_url)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/batch-verify', methods=['POST'])
def batch_verify():
    try:
        data = request.json
        articles = data.get('articles', [])
        
        results = []
        for article in articles:
            text = article.get('text', '')
            source = article.get('source_url', '')
            result = detector.analyze(text, source)
            results.append({
                'title': article.get('title', 'Unknown'),
                'result': result
            })
        
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
