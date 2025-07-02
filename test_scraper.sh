#!/bin/bash

# Test script for the Case Study Scraper
# Make sure to set your OPENAI_API_KEY before running this

echo "🧪 Testing Case Study Scraper..."
echo "================================"

# Check if API key is set
if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "sk-REPLACE_WITH_YOUR_KEY" ]; then
    echo "❌ Please set your OpenAI API key first:"
    echo "   export OPENAI_API_KEY='your-actual-api-key-here'"
    exit 1
fi

# Ensure PATH includes local bin
export PATH="/home/ubuntu/.local/bin:$PATH"

echo "✅ API key is set"
echo "✅ Testing with example.com..."

# Run the scraper on example.com
python3 case_study_scraper.py https://example.com

echo ""
echo "🎉 Test completed! Check the results/ folder for output."
echo "📁 To process multiple URLs, edit example_urls.txt and run:"
echo "   python3 batch_scraper.py example_urls.txt"