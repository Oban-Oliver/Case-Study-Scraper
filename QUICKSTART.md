# 🚀 Quick Start Guide

## **Ready to Run!** ✅

Your case study scraper is already set up and ready to use. Here's how to run it:

## **1. Set Your OpenAI API Key**

```bash
export OPENAI_API_KEY="your-actual-openai-api-key-here"
```

**⚠️ IMPORTANT:** Replace `"your-actual-openai-api-key-here"` with your real OpenAI API key!

## **2. Run the Scraper**

### **Single URL:**
```bash
export PATH="/home/ubuntu/.local/bin:$PATH"
python3 case_study_scraper.py https://example-competitor.com/case-study
```

### **Multiple URLs (Batch):**
1. Edit `example_urls.txt` and add your competitor URLs (one per line)
2. Run:
```bash
export PATH="/home/ubuntu/.local/bin:$PATH"
python3 batch_scraper.py example_urls.txt
```

## **3. Find Your Results**

Results are automatically saved in the `results/` folder as JSON files with timestamps.

## **Examples:**

```bash
# Basic scraping
python3 case_study_scraper.py https://www.salesforce.com/resources/customer-success-stories/

# Custom analysis focus
python3 case_study_scraper.py https://competitor.com/case-study --prompt "Extract only ROI and cost savings metrics"

# Batch process multiple competitors
python3 batch_scraper.py competitor_urls.txt
```

## **🎯 Pro Tips:**

- **Find competitor case studies** by searching: `site:competitor.com "case study" OR "success story" OR "customer story"`
- **Focus your prompts** on specific metrics you care about (ROI, user adoption, performance improvements)
- **Use batch processing** to analyze multiple competitors efficiently
- **Results are JSON files** - easy to import into spreadsheets or analysis tools

## **Need Help?**

- Check `README.md` for full documentation
- Results are saved in `results/` folder
- Each run creates a timestamped file
- Batch processing creates consolidated reports

**You're all set! Start scraping competitor data! 🎉**