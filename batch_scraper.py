#!/usr/bin/env python3
"""
Batch Case Study Scraper for Mesh-AI Competitor Analysis
Process multiple URLs in batch and generate consolidated reports.
"""

import json
import time
from datetime import datetime
from case_study_scraper import extract_metrics_from_url, log_message
import argparse

def process_urls_from_file(file_path, delay_seconds=2, custom_prompt=None):
    """
    Process multiple URLs from a text file.
    
    Args:
        file_path (str): Path to file containing URLs (one per line)
        delay_seconds (int): Delay between requests to be respectful to servers
        custom_prompt (str): Custom prompt for all extractions
    
    Returns:
        list: Results from all processed URLs
    """
    results = []
    
    try:
        with open(file_path, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        log_message(f"File not found: {file_path}", "ERROR")
        return results
    
    log_message(f"Processing {len(urls)} URLs from {file_path}")
    
    for i, url in enumerate(urls, 1):
        log_message(f"Processing URL {i}/{len(urls)}: {url}")
        
        result = extract_metrics_from_url(
            target_url=url,
            save_to_file=True,
            custom_prompt=custom_prompt
        )
        
        if result:
            results.append(result)
            log_message(f"✅ Successfully processed {url}")
        else:
            log_message(f"❌ Failed to process {url}", "WARNING")
        
        # Add delay between requests to be respectful
        if i < len(urls):
            log_message(f"Waiting {delay_seconds} seconds before next request...")
            time.sleep(delay_seconds)
    
    return results

def generate_consolidated_report(results, output_file="consolidated_report.json"):
    """Generate a consolidated report from all results."""
    
    if not results:
        log_message("No results to consolidate", "WARNING")
        return
    
    consolidated = {
        "report_generated_at": datetime.now().isoformat(),
        "total_urls_processed": len(results),
        "results": results,
        "summary": {
            "successful_extractions": len([r for r in results if r]),
            "total_text_processed": sum(r.get("raw_text_length", 0) for r in results if r),
            "urls_processed": [r["url"] for r in results if r]
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(consolidated, f, indent=2, ensure_ascii=False)
    
    log_message(f"Consolidated report saved to {output_file}")
    return output_file

def main():
    """Main function for batch processing."""
    parser = argparse.ArgumentParser(description="Batch process multiple URLs for case study analysis")
    parser.add_argument("urls_file", help="Text file containing URLs (one per line)")
    parser.add_argument("--delay", type=int, default=2, help="Delay between requests in seconds (default: 2)")
    parser.add_argument("--prompt", help="Custom prompt for all extractions")
    parser.add_argument("--output", default="consolidated_report.json", help="Output file for consolidated report")
    
    args = parser.parse_args()
    
    log_message("Starting Batch Case Study Scraper")
    
    # Process all URLs
    results = process_urls_from_file(
        file_path=args.urls_file,
        delay_seconds=args.delay,
        custom_prompt=args.prompt
    )
    
    # Generate consolidated report
    if results:
        report_file = generate_consolidated_report(results, args.output)
        log_message(f"Batch processing completed. {len(results)} URLs processed successfully.")
        print(f"\n📊 Consolidated report available at: {report_file}")
    else:
        log_message("No URLs were processed successfully", "ERROR")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())