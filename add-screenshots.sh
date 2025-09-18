#!/bin/bash
# 
# Script to help add screenshots to the repository
# Usage: ./add-screenshots.sh
#

echo "📸 Adding Screenshots to Developer Salary Prediction App"
echo "======================================================"
echo ""

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Please run this script from the project root directory (where app.py is located)"
    exit 1
fi

# Create docs/images directory if it doesn't exist
mkdir -p docs/images

echo "🎯 To add screenshots to your README:"
echo ""
echo "1. Take screenshots of your application:"
echo "   📋 Welcome interface (empty form with educational content)"
echo "   📊 Prediction results (filled form showing salary prediction)"
echo ""
echo "2. Save the screenshots as:"
echo "   • docs/images/welcome-interface.png"
echo "   • docs/images/prediction-results.png"
echo ""
echo "3. Screenshots should be:"
echo "   • High quality (at least 1200px wide)"
echo "   • PNG format for best quality"
echo "   • Show the complete interface"
echo ""
echo "4. Remove the placeholder files:"
echo "   rm docs/images/*.placeholder"
echo ""
echo "5. Commit and push the changes:"
echo "   git add docs/images/*.png"
echo "   git commit -m 'Add application screenshots'"
echo "   git push origin main"
echo ""

# Check if placeholder files exist and offer to remove them
if [ -f "docs/images/prediction-results.png.placeholder" ] || [ -f "docs/images/welcome-interface.png.placeholder" ]; then
    echo "🗑️  Found placeholder files. After adding real screenshots, run:"
    echo "   rm docs/images/*.placeholder"
    echo ""
fi

# Check if real screenshots exist
real_screenshots=0
if [ -f "docs/images/prediction-results.png" ]; then
    echo "✅ Found: prediction-results.png"
    real_screenshots=$((real_screenshots + 1))
fi

if [ -f "docs/images/welcome-interface.png" ]; then
    echo "✅ Found: welcome-interface.png"
    real_screenshots=$((real_screenshots + 1))
fi

if [ $real_screenshots -eq 2 ]; then
    echo ""
    echo "🎉 All screenshots are present! Your README will display properly."
elif [ $real_screenshots -eq 1 ]; then
    echo ""
    echo "⚠️  Only 1 of 2 screenshots found. Add the missing screenshot for complete documentation."
else
    echo ""
    echo "📝 No screenshots found yet. Add them to make your README more appealing!"
fi

echo ""
echo "💡 Tip: Take screenshots with both interfaces shown to demonstrate the full functionality."