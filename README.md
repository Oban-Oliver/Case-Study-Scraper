# Marketing Metrics Analyzer

A single-file Python tool that scrapes URLs and analyzes marketing content using OpenAI GPT-4o-mini.

## Features

- **URL Scraping**: Extracts text content from web pages
- **Marketing Metrics Analysis**:
  - Jargon density (AI/ML terms per 500 words)
  - Process clarity (action verb percentage)
  - Vague terms count (buzzwords per 1000 words)
  - Statistics usage (quantitative data sentences)
  - Future vs past focus ratio
  - Overall marketing effectiveness score (0-100)
- **OpenAI Integration**: Enhanced analysis using GPT-4o-mini for readability, persuasiveness, credibility, and engagement scores
- **JSON Export**: Saves analysis results to a JSON file

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your OpenAI API key**:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

3. **Run the analyzer**:
   ```bash
   python marketing_analyzer.py
   ```

The script will analyze the default test URL and display comprehensive metrics.

## Usage

The analyzer includes a test URL by default, but you can modify the `test_url` variable in the `main()` function to analyze any URL you want.

## Dependencies

- `requests`: For web scraping
- `openai`: For AI-powered analysis

## Output

The analyzer provides:
- Detailed console output with all metrics
- JSON file (`marketing_analysis_results.json`) with complete results
- Marketing effectiveness score with interpretation

## Example Output

```
============================================================
MARKETING METRICS ANALYSIS
============================================================
URL: https://example.com
Word Count: 1,234
Character Count: 7,890

BASIC METRICS:
  Jargon Density: 15.67 AI/ML terms per 500 words
  Process Clarity: 8.42% action verbs
  Vague Terms: 12.34 buzzwords per 1000 words
  Statistics Usage: 5 quantitative data points
  Future/Past Ratio: 1.25

OPENAI ANALYSIS:
  Readability Score: 7/10
  Persuasiveness Score: 8/10
  Credibility Score: 6/10
  Engagement Score: 7/10
  Call-to-Action Strength: 5/10
  Tone: Professional, technical
  Target Audience: Technical professionals and decision-makers

MARKETING EFFECTIVENESS SCORE: 72.3/100
Interpretation: Good - Effective with room for improvement
============================================================
```

## License

This project is provided as-is for educational and analysis purposes.
