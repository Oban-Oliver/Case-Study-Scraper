# Case-Study-Scraper

Extract case studies and metrics from Mesh-AI's competitors using web scraping and OpenAI analysis.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Set Your OpenAI API Key

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

Or edit the script directly to replace `sk-REPLACE_WITH_YOUR_KEY` with your actual key.

### 3. Run the Scraper

#### Single URL:
```bash
python case_study_scraper.py https://competitor-website.com/case-study
```

#### Batch Processing:
```bash
# Add URLs to example_urls.txt, then run:
python batch_scraper.py example_urls.txt
```

## 📋 Features

- **Web Scraping**: Uses Playwright to extract content from any webpage
- **AI Analysis**: Leverages OpenAI GPT-4o to extract structured metrics and data points
- **Batch Processing**: Process multiple URLs in sequence with rate limiting
- **Data Storage**: Automatically saves results to JSON files with timestamps
- **Error Handling**: Robust error handling with detailed logging
- **Customizable Prompts**: Use custom prompts for specific analysis needs

## 🛠 Usage Examples

### Basic Usage
```bash
# Scrape a single case study
python case_study_scraper.py https://example-competitor.com/case-study

# Use a custom prompt
python case_study_scraper.py https://example.com --prompt "Extract only financial metrics and ROI data"

# Don't save results to file
python case_study_scraper.py https://example.com --no-save
```

### Batch Processing
```bash
# Process multiple URLs with default 2-second delay
python batch_scraper.py competitor_urls.txt

# Custom delay and output file
python batch_scraper.py competitor_urls.txt --delay 5 --output my_analysis.json

# Custom prompt for all URLs
python batch_scraper.py urls.txt --prompt "Focus on performance metrics and user adoption rates"
```

### URL File Format
Create a text file with URLs (one per line):
```
# competitor_urls.txt
https://competitor1.com/case-studies/enterprise-success
https://competitor2.com/customer-stories/retail-transformation
https://competitor3.com/case-study/manufacturing-efficiency
```

## 📊 Output Format

### Individual Results
Each scraping session creates a JSON file in the `results/` directory:
```json
{
  "url": "https://example.com/case-study",
  "scraped_at": "2024-01-15T10:30:00",
  "structured_metrics": "# Company: TechCorp\n## Performance Metrics\n- 40% increase in efficiency...",
  "raw_text_length": 15420
}
```

### Consolidated Reports
Batch processing generates consolidated reports:
```json
{
  "report_generated_at": "2024-01-15T10:35:00",
  "total_urls_processed": 5,
  "summary": {
    "successful_extractions": 4,
    "total_text_processed": 45000,
    "urls_processed": ["url1", "url2", ...]
  },
  "results": [...]
}
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Customization Options
- **Custom Prompts**: Tailor the AI analysis for specific metrics
- **Rate Limiting**: Adjust delays between requests
- **Output Formats**: JSON files with structured data
- **Error Handling**: Comprehensive logging and error recovery

## 📁 Project Structure

```
case-study-scraper/
├── case_study_scraper.py    # Main scraper script
├── batch_scraper.py         # Batch processing script
├── requirements.txt         # Python dependencies
├── example_urls.txt         # Example URL list
├── results/                 # Output directory (auto-created)
└── README.md               # This file
```

## 🎯 Tips for Competitor Analysis

1. **Target Specific Pages**: Focus on case studies, success stories, and customer testimonials
2. **Custom Prompts**: Use prompts like:
   - "Extract ROI, cost savings, and efficiency improvements"
   - "Focus on implementation timeline and team size metrics"
   - "Identify industry verticals and use cases mentioned"
3. **Batch Processing**: Process multiple competitors at once for comparative analysis
4. **Data Export**: Results are saved in JSON format for easy analysis in Excel, Python, or BI tools

## 🚨 Important Notes

- **Rate Limiting**: Default 2-second delay between requests to be respectful to servers
- **API Costs**: OpenAI API usage will incur costs based on token consumption
- **Legal Compliance**: Ensure compliance with websites' terms of service and robots.txt
- **Data Privacy**: Be mindful of any sensitive information in scraped content

## 🐛 Troubleshooting

- **Playwright Installation**: Run `playwright install chromium` if browser fails to launch
- **API Key Issues**: Ensure `OPENAI_API_KEY` environment variable is set correctly
- **Network Timeouts**: Some sites may take longer to load; the script includes retry logic
- **Empty Results**: Check if the target site has anti-bot protection or requires authentication
