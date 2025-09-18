#!/bin/bash
#
# Quick script to add PNG screenshots to the repository
# Usage: ./add-png-images.sh
#

echo "📸 Adding PNG Screenshots to Repository"
echo "======================================"

# Check if we have the images directory
if [ ! -d "docs/images" ]; then
    echo "❌ docs/images directory not found!"
    echo "Please run this script from the project root directory."
    exit 1
fi

echo ""
echo "🎯 Instructions to add your screenshots:"
echo ""
echo "1. Take screenshots of your application:"
echo "   📱 Prediction results page (with form filled and results shown)"
echo "   📱 Welcome page (with educational content visible)"
echo ""
echo "2. Save them as PNG files:"
echo "   • prediction-results.png"
echo "   • welcome-interface.png"
echo ""
echo "3. Copy them to docs/images/:"
echo "   cp /path/to/prediction-results.png docs/images/"
echo "   cp /path/to/welcome-interface.png docs/images/"
echo ""
echo "4. Remove placeholder files:"
echo "   rm docs/images/*.placeholder"
echo ""
echo "5. Commit and push:"
echo "   git add docs/images/*.png"
echo "   git commit -m '📸 Add application screenshots'"
echo "   git push origin main"
echo ""

# Check current status
echo "📋 Current Status:"
if [ -f "docs/images/prediction-results.png" ]; then
    echo "✅ prediction-results.png exists"
else
    echo "❌ prediction-results.png missing"
fi

if [ -f "docs/images/welcome-interface.png" ]; then
    echo "✅ welcome-interface.png exists"
else
    echo "❌ welcome-interface.png missing"
fi

echo ""
echo "📁 Files in docs/images/:"
ls -la docs/images/

echo ""
echo "💡 After adding PNG files, your README screenshots will display properly on GitHub!"