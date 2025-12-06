# Fake News Detection System - TRUTH

An AI-powered system to detect and combat misinformation and fake news in digital media.

## Features

- **Natural Language Processing**: Advanced NLP techniques for content analysis including sentiment analysis, pattern detection, and machine learning classification
- **Source Credibility Verification**: Automatic checking of source domains, WHOIS information, and known credible sources
- **Real-time Fact-Checking**: Simulated fact-checking capabilities with claim detection and verification
- **User-Friendly Interface**: Modern, responsive web interface for easy news verification
- **Accuracy Metrics**: Comprehensive scoring system with confidence levels and detailed breakdowns

## Installation

1. Install Python 3.8 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. **Single Article Verification**:
   - Paste the article text in the text area
   - Optionally provide the source URL
   - Click "Verify News Article"
   - View the comprehensive analysis results

2. **Sample Articles**:
   - Use the sample article buttons to test the system with pre-loaded examples
   - Try "Real News Sample", "Fake News Sample", or "Uncertain Sample"

## How It Works

The system uses a multi-layered approach:

1. **Text Analysis (40% weight)**:
   - Sentiment analysis
   - Suspicious pattern detection
   - Machine learning classification
   - Linguistic feature analysis

2. **Source Credibility (30% weight)**:
   - Domain verification against known credible sources
   - WHOIS information checking
   - Domain age analysis
   - Suspicious TLD detection

3. **Fact-Checking (30% weight)**:
   - False claim keyword detection
   - Citation verification
   - Date and quote presence checking
   - Structural analysis

The final score is a weighted average of these three components, with a confidence metric based on agreement between methods.

## API Endpoints

### POST /api/verify
Verify a single news article.

**Request Body**:
```json
{
  "text": "Article text here...",
  "source_url": "https://example.com/article"
}
```

**Response**:
```json
{
  "text_analysis": {...},
  "source_credibility": {...},
  "fact_checking": {...},
  "overall_score": 0.85,
  "confidence": 0.92,
  "verdict": "Likely True",
  "details": {...}
}
```

### POST /api/batch-verify
Verify multiple articles at once.

**Request Body**:
```json
{
  "articles": [
    {
      "title": "Article 1",
      "text": "Article text...",
      "source_url": "https://example.com"
    }
  ]
}
```

## Technical Stack

- **Backend**: Flask (Python)
- **NLP**: NLTK, TextBlob, scikit-learn
- **Frontend**: HTML, CSS, JavaScript
- **Source Verification**: whois, tldextract

## Limitations

This is a prototype system. For production use, consider:

- Integration with real fact-checking APIs (Google Fact Check API, Snopes API)
- Larger training datasets for the ML classifier
- More sophisticated NLP models (BERT, GPT-based)
- Real-time web scraping for source verification
- Database for storing and tracking verified claims

## License

This project is provided as-is for educational and demonstration purposes.

