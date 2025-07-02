#!/bin/bash

# Case Study Scraper Setup Script
# Automates the installation and setup process

echo "🚀 Setting up Case Study Scraper for Mesh-AI Competitor Analysis"
echo "=============================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# Install Playwright browsers
echo "🌐 Installing Playwright browser..."
playwright install chromium

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Playwright browser"
    exit 1
fi

# Create results directory
echo "📁 Creating results directory..."
mkdir -p results

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x case_study_scraper.py
chmod +x batch_scraper.py

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Set your OpenAI API key:"
echo "   export OPENAI_API_KEY='your-api-key-here'"
echo ""
echo "2. Test the scraper:"
echo "   python3 case_study_scraper.py https://example.com"
echo ""
echo "3. For batch processing, edit example_urls.txt and run:"
echo "   python3 batch_scraper.py example_urls.txt"
echo ""
echo "📖 See README.md for detailed usage instructions"