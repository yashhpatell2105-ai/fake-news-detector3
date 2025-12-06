# Quick Start Guide

## Step 1: Install Dependencies

Open a terminal in the `fake-news-detector` directory and run:

```bash
pip install -r requirements.txt
```

This will install all required Python packages including Flask, NLTK, scikit-learn, and others.

## Step 2: Run the Application

Start the Flask server:

```bash
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
```

## Step 3: Access the Web Interface

Open your web browser and navigate to:
```
http://localhost:5000
```

## Step 4: Test the System

1. **Using the Web Interface**:
   - Click one of the sample article buttons (Real News, Fake News, or Uncertain)
   - Or paste your own article text
   - Optionally add a source URL
   - Click "Verify News Article"
   - View the comprehensive analysis results

2. **Using the Demo Script** (Optional):
   - In a new terminal, run:
   ```bash
   python demo.py
   ```
   - This will test the API with sample articles

## Features to Try

- **Text Analysis**: See how the system analyzes sentiment, detects suspicious patterns, and uses ML classification
- **Source Credibility**: Test with different URLs to see source verification in action
- **Fact-Checking**: Observe how the system checks for false claims and verifies article structure
- **Confidence Scoring**: Notice how confidence changes based on agreement between different analysis methods

## Troubleshooting

- **Port already in use**: Change the port in `app.py` (line: `app.run(debug=True, port=5000)`)
- **NLTK data not downloading**: The system will automatically download required NLTK data on first run
- **Import errors**: Make sure all dependencies are installed: `pip install -r requirements.txt`

## Next Steps

- Try verifying real news articles from different sources
- Experiment with different types of content
- Review the detailed analysis breakdowns to understand how the system works
- Check the README.md for more information about the system architecture

