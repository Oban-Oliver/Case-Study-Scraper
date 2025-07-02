#!/usr/bin/env python3
"""
Case Study Scraper for Mesh-AI Competitor Analysis
Extracts metrics and data points from competitor case studies using Playwright and OpenAI.
"""

from playwright.sync_api import sync_playwright
import requests
import os
import json
import time
from datetime import datetime
from urllib.parse import urlparse
import argparse

# Configuration
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    OPENAI_KEY = "sk-REPLACE_WITH_YOUR_KEY"

def log_message(message, level="INFO"):
    """Simple logging function with timestamps."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")

def save_results(url, structured_metrics, raw_text=None):
    """Save results to a JSON file for later analysis."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    domain = urlparse(url).netloc.replace(".", "_")
    filename = f"results/{domain}_{timestamp}.json"
    
    # Create results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    
    data = {
        "url": url,
        "scraped_at": datetime.now().isoformat(),
        "structured_metrics": structured_metrics,
        "raw_text_length": len(raw_text) if raw_text else 0
    }
    
    # Optionally save raw text for debugging
    if raw_text and len(raw_text) < 50000:  # Only save if not too large
        data["raw_text"] = raw_text
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    log_message(f"Results saved to {filename}")
    return filename

def extract_metrics_from_url(target_url, save_to_file=True, custom_prompt=None):
    """
    Extract metrics and data points from a given URL.
    
    Args:
        target_url (str): The URL to scrape
        save_to_file (bool): Whether to save results to a file
        custom_prompt (str): Custom prompt for OpenAI, defaults to standard metrics extraction
    
    Returns:
        dict: Contains the structured metrics and metadata
    """
    
    if not OPENAI_KEY or OPENAI_KEY == "sk-REPLACE_WITH_YOUR_KEY":
        log_message("ERROR: Please set your OpenAI API key in the OPENAI_API_KEY environment variable", "ERROR")
        return None
    
    # Default prompt for case study analysis
    if not custom_prompt:
        custom_prompt = (
            "Extract all numbers, statistics, and key metrics from this case study or article. "
            "Group them logically by topic (e.g., Performance Metrics, Financial Data, User Engagement, etc.). "
            "Only include data points with specific numbers or percentages. "
            "Format the output as structured sections with clear headings. "
            "Also identify the company name, industry, and main use case if mentioned."
        )
    
    try:
        with sync_playwright() as p:
            # Launch browser in headless mode
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Set a reasonable user agent
            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            })
            
            log_message(f"Navigating to {target_url}...")
            
            # Navigate with timeout and wait for network to be idle
            try:
                page.goto(target_url, wait_until="networkidle", timeout=30000)
            except Exception as e:
                log_message(f"Navigation timeout or error: {e}", "WARNING")
                # Try with a shorter timeout
                page.goto(target_url, wait_until="domcontentloaded", timeout=15000)
            
            # Wait a bit for any dynamic content to load
            page.wait_for_timeout(2000)
            
            # Extract visible text from the full page body
            page_text = page.locator("body").inner_text()
            
            if not page_text or len(page_text.strip()) < 100:
                log_message("Warning: Very little text extracted from the page", "WARNING")
            
            log_message(f"Extracted {len(page_text)} characters of text")
            browser.close()
            
    except Exception as e:
        log_message(f"Error during web scraping: {e}", "ERROR")
        return None
    
    # Send to OpenAI
    log_message("Sending text to OpenAI for analysis...")
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "system", 
                        "content": "You are a business analyst specializing in extracting key metrics and data points from case studies and competitor analysis."
                    },
                    {
                        "role": "user", 
                        "content": f"{custom_prompt}\n\n{page_text}"
                    }
                ],
                "temperature": 0.3,  # Lower temperature for more consistent extraction
                "max_tokens": 2000
            },
            timeout=60
        )
        
        response.raise_for_status()  # Raise an exception for bad status codes
        
    except requests.exceptions.RequestException as e:
        log_message(f"Error calling OpenAI API: {e}", "ERROR")
        return None
    
    try:
        result = response.json()
        structured_metrics = result["choices"][0]["message"]["content"]
        
        log_message("✅ Successfully extracted metrics from OpenAI")
        
        # Prepare return data
        return_data = {
            "url": target_url,
            "structured_metrics": structured_metrics,
            "raw_text_length": len(page_text),
            "scraped_at": datetime.now().isoformat()
        }
        
        # Save to file if requested
        if save_to_file:
            save_results(target_url, structured_metrics, page_text)
        
        return return_data
        
    except (KeyError, json.JSONDecodeError) as e:
        log_message(f"Error parsing OpenAI response: {e}", "ERROR")
        return None

def main():
    """Main function to handle command line arguments and run the scraper."""
    parser = argparse.ArgumentParser(description="Extract metrics from case studies using Playwright and OpenAI")
    parser.add_argument("url", nargs="?", default="https://www.example.com", help="URL to scrape")
    parser.add_argument("--no-save", action="store_true", help="Don't save results to file")
    parser.add_argument("--prompt", help="Custom prompt for OpenAI analysis")
    
    args = parser.parse_args()
    
    log_message("Starting Case Study Scraper for Mesh-AI Competitor Analysis")
    log_message(f"Target URL: {args.url}")
    
    # Run the extraction
    result = extract_metrics_from_url(
        target_url=args.url,
        save_to_file=not args.no_save,
        custom_prompt=args.prompt
    )
    
    if result:
        print("\n" + "="*60)
        print("📊 EXTRACTED METRICS & DATA POINTS")
        print("="*60)
        print(result["structured_metrics"])
        print("\n" + "="*60)
        log_message(f"Scraping completed successfully. Processed {result['raw_text_length']} characters.")
    else:
        log_message("Scraping failed. Please check the logs above for details.", "ERROR")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())