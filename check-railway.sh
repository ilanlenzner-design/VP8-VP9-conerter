#!/bin/bash

echo "🚂 Railway Deployment Checker"
echo "=============================="
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found"
    echo "Install with: brew install railway"
    exit 1
fi

echo "✅ Railway CLI installed"
echo ""

# Link to project (you need to run this manually first time)
echo "To link your project, run:"
echo "  railway link"
echo ""
echo "Then run this script again to see status"
echo ""

# Try to get status
echo "Attempting to get deployment status..."
railway status 2>&1 || echo "Not linked to a project. Run 'railway link' first."

echo ""
echo "To see logs:"
echo "  railway logs"
echo ""
echo "To open in browser:"
echo "  railway open"

