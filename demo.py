"""
Demo script to test the Fake News Detection System
Run this after starting the Flask app to test the API
"""

import requests
import json

# Sample articles for testing
sample_articles = [
    {
        "title": "Real News - Scientific Breakthrough",
        "text": "Breaking News: Scientists at the Massachusetts Institute of Technology have announced a significant breakthrough in renewable energy technology. According to a peer-reviewed study published in Nature Energy, researchers have developed a new solar cell design that increases efficiency by 25%. The research, conducted over three years with funding from the National Science Foundation, has been verified by independent laboratories. Dr. Sarah Johnson, lead researcher, stated: 'This advancement could significantly reduce the cost of solar energy production.' The findings were presented at the International Renewable Energy Conference on March 15, 2024.",
        "source_url": "https://www.reuters.com/technology/solar-breakthrough"
    },
    {
        "title": "Fake News - Clickbait",
        "text": "SHOCKING TRUTH: Doctors HATE this one simple trick that cures diabetes in 24 hours! Click here to discover the secret that Big Pharma doesn't want you to know! Number 7 will absolutely blow your mind! This guaranteed method has been hidden from the public for years. ACT NOW - Limited time offer! You won't believe what happens next!",
        "source_url": "https://suspicious-site.tk/amazing-cure"
    },
    {
        "title": "Uncertain News - Mixed Evidence",
        "text": "A new study suggests that regular consumption of green tea may have health benefits. Some researchers claim it can help with weight loss, though the evidence is mixed. The study involved 100 participants over 6 months. However, critics point out that the sample size was relatively small and more research is needed. The findings were published in a nutrition journal, but some experts remain skeptical about the conclusions.",
        "source_url": "https://healthblog.com/green-tea-study"
    }
]

def test_verification(article_text, source_url=""):
    """Test a single article verification"""
    url = "http://localhost:5000/api/verify"
    payload = {
        "text": article_text,
        "source_url": source_url
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure Flask app is running on http://localhost:5000")
        return None

def print_results(title, result):
    """Pretty print the verification results"""
    print("\n" + "="*60)
    print(f"Article: {title}")
    print("="*60)
    print(f"Verdict: {result['verdict']}")
    print(f"Overall Score: {result['overall_score']:.2%}")
    print(f"Confidence: {result['confidence']:.2%}")
    print("\nDetailed Scores:")
    print(f"  Text Analysis: {result['text_analysis']['score']:.2%}")
    if result['source_credibility']:
        print(f"  Source Credibility: {result['source_credibility']['score']:.2%}")
    print(f"  Fact-Checking: {result['fact_checking']['score']:.2%}")
    print("\nText Analysis Details:")
    print(f"  Sentiment: {result['text_analysis']['sentiment']:.2f}")
    print(f"  Suspicious Patterns: {result['text_analysis']['suspicious_patterns_found']}")
    print(f"  ML Confidence: {result['text_analysis']['ml_confidence']:.2%}")
    print("="*60)

def main():
    print("Fake News Detection System - Demo")
    print("="*60)
    print("Testing sample articles...\n")
    
    for article in sample_articles:
        result = test_verification(article['text'], article.get('source_url', ''))
        if result:
            print_results(article['title'], result)
    
    print("\n" + "="*60)
    print("Demo completed!")
    print("="*60)
    print("\nTo use the web interface, open http://localhost:5000 in your browser")

if __name__ == "__main__":
    main()

