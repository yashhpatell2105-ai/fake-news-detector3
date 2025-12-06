import re
import nltk
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import requests
from bs4 import BeautifulSoup
import tldextract
import whois
from datetime import datetime
import json

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class FakeNewsDetector:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.classifier = MultinomialNB()
        self._initialize_classifier()
        
        # Known credible sources (can be expanded)
        self.credible_domains = {
            'reuters.com', 'bbc.com', 'ap.org', 'nytimes.com', 
            'washingtonpost.com', 'theguardian.com', 'wsj.com',
            'npr.org', 'cnn.com', 'abcnews.go.com', 'cbsnews.com'
        }
        
        # Suspicious patterns
        self.suspicious_patterns = [
            r'click here',
            r'you won\'t believe',
            r'shocking truth',
            r'doctors hate',
            r'this one trick',
            r'number \d+ will',
            r'guaranteed',
            r'limited time',
            r'act now',
            r'exclusive'
        ]
    
    def _initialize_classifier(self):
        """Initialize a simple classifier with training data"""
        # Sample training data (in production, use a larger dataset)
        training_texts = [
            "Breaking news: Scientists discover new breakthrough in medical research.",
            "Official statement from government confirms new policy changes.",
            "Verified sources report major economic development.",
            "CLICK HERE TO WIN $1000! You won't believe this shocking truth!",
            "Doctors hate this one trick! Guaranteed results in 24 hours!",
            "Exclusive: Secret information they don't want you to know!",
            "Breaking: Major company announces revolutionary product launch.",
            "Verified report: International summit concludes successfully.",
            "ACT NOW! Limited time offer! This will change your life!",
            "Number 7 will shock you! Click to see the truth!"
        ]
        training_labels = [1, 1, 1, 0, 0, 0, 1, 1, 0, 0]  # 1 = real, 0 = fake
        
        X_train = self.vectorizer.fit_transform(training_texts)
        self.classifier.fit(X_train, training_labels)
    
    def analyze(self, text, source_url=None):
        """Comprehensive analysis of news article"""
        results = {
            'text_analysis': self._analyze_text(text),
            'source_credibility': self._check_source_credibility(source_url) if source_url else None,
            'fact_checking': self._fact_check(text),
            'overall_score': 0.0,
            'confidence': 0.0,
            'verdict': 'Unknown',
            'details': {}
        }
        
        # Calculate overall score
        scores = []
        weights = []
        
        # Text analysis score
        text_score = results['text_analysis']['score']
        scores.append(text_score)
        weights.append(0.4)
        
        # Source credibility score
        if results['source_credibility']:
            source_score = results['source_credibility']['score']
            scores.append(source_score)
            weights.append(0.3)
        
        # Fact-checking score
        fact_score = results['fact_checking']['score']
        scores.append(fact_score)
        weights.append(0.3)
        
        # Weighted average
        if weights:
            overall_score = sum(s * w for s, w in zip(scores, weights)) / sum(weights)
        else:
            overall_score = text_score
        
        results['overall_score'] = round(overall_score, 2)
        
        # Calculate confidence based on agreement between methods
        if len(scores) > 1:
            variance = np.var(scores)
            confidence = max(0, 1 - variance)  # Lower variance = higher confidence
        else:
            confidence = 0.7
        
        results['confidence'] = round(confidence, 2)
        
        # Determine verdict
        if overall_score >= 0.7:
            results['verdict'] = 'Likely True'
        elif overall_score >= 0.4:
            results['verdict'] = 'Uncertain'
        else:
            results['verdict'] = 'Likely Fake'
        
        results['details'] = {
            'text_score': round(text_score, 2),
            'source_score': round(results['source_credibility']['score'], 2) if results['source_credibility'] else None,
            'fact_score': round(fact_score, 2)
        }
        
        return results
    
    def _analyze_text(self, text):
        """NLP-based text analysis"""
        blob = TextBlob(text)
        
        # Sentiment analysis
        sentiment = blob.sentiment.polarity
        
        # Check for suspicious patterns
        suspicious_count = sum(1 for pattern in self.suspicious_patterns 
                             if re.search(pattern, text.lower()))
        
        # ML-based classification
        X = self.vectorizer.transform([text])
        ml_prediction = self.classifier.predict_proba(X)[0]
        ml_score = ml_prediction[1]  # Probability of being real
        
        # Linguistic features
        words = word_tokenize(text.lower())
        word_count = len(words)
        unique_words = len(set(words))
        avg_word_length = np.mean([len(w) for w in words if w.isalpha()])
        
        # Calculate text credibility score
        base_score = ml_score
        
        # Penalize for suspicious patterns
        pattern_penalty = min(0.3, suspicious_count * 0.1)
        base_score -= pattern_penalty
        
        # Adjust for sentiment extremes (very negative or very positive might indicate bias)
        sentiment_penalty = abs(sentiment) * 0.1 if abs(sentiment) > 0.8 else 0
        base_score -= sentiment_penalty
        
        # Normalize to 0-1 range
        text_score = max(0, min(1, base_score))
        
        return {
            'score': text_score,
            'sentiment': round(sentiment, 2),
            'suspicious_patterns_found': suspicious_count,
            'ml_confidence': round(ml_score, 2),
            'word_count': word_count,
            'unique_words': unique_words,
            'avg_word_length': round(avg_word_length, 2)
        }
    
    def _check_source_credibility(self, url):
        """Verify source credibility"""
        if not url:
            return {'score': 0.5, 'status': 'No URL provided', 'details': {}}
        
        try:
            extracted = tldextract.extract(url)
            domain = f"{extracted.domain}.{extracted.suffix}"
            
            score = 0.5  # Base score
            details = {'domain': domain}
            
            # Check against known credible sources
            if domain in self.credible_domains:
                score = 0.9
                details['status'] = 'Known credible source'
            else:
                # Try to get WHOIS information
                try:
                    w = whois.whois(domain)
                    if w.domain_name:
                        # Check domain age (older domains are generally more credible)
                        if w.creation_date:
                            if isinstance(w.creation_date, list):
                                creation_date = w.creation_date[0]
                            else:
                                creation_date = w.creation_date
                            
                            age_days = (datetime.now() - creation_date).days
                            if age_days > 365:
                                score += 0.2
                            details['domain_age_days'] = age_days
                except:
                    pass
                
                # Check for suspicious TLDs
                suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq']
                if any(tld in url.lower() for tld in suspicious_tlds):
                    score -= 0.3
                    details['suspicious_tld'] = True
                
                details['status'] = 'Unknown source'
            
            return {
                'score': max(0, min(1, score)),
                'status': details.get('status', 'Unknown'),
                'details': details
            }
        except Exception as e:
            return {
                'score': 0.5,
                'status': f'Error checking source: {str(e)}',
                'details': {}
            }
    
    def _fact_check(self, text):
        """Real-time fact-checking simulation"""
        # In a production system, this would integrate with fact-checking APIs
        # like Google Fact Check API, Snopes API, etc.
        
        # For demo purposes, we'll simulate fact-checking based on:
        # 1. Claim detection
        # 2. Keyword matching against known false claims
        # 3. Statistical analysis
        
        # Known false claim keywords (simplified)
        false_claim_keywords = [
            'vaccine causes autism',
            'moon landing fake',
            'flat earth',
            'chemtrails',
            '5g causes covid'
        ]
        
        text_lower = text.lower()
        false_claims_found = sum(1 for keyword in false_claim_keywords 
                                if keyword in text_lower)
        
        # Calculate fact-check score
        if false_claims_found > 0:
            fact_score = 0.2  # Very low if known false claims found
        else:
            # Base score on text quality and structure
            # Well-structured articles with citations are more credible
            has_citations = bool(re.search(r'\[.*?\]|\(.*?\)|source:', text_lower))
            has_dates = bool(re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', text))
            has_quotes = text.count('"') >= 2
            
            fact_score = 0.5  # Base score
            if has_citations:
                fact_score += 0.2
            if has_dates:
                fact_score += 0.15
            if has_quotes:
                fact_score += 0.15
        
        return {
            'score': max(0, min(1, fact_score)),
            'false_claims_detected': false_claims_found,
            'has_citations': bool(re.search(r'\[.*?\]|\(.*?\)|source:', text_lower)),
            'has_dates': bool(re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', text)),
            'has_quotes': text.count('"') >= 2
        }
