#!/bin/bash

# Video Compressor - Deployment Helper
# This script helps you deploy to Vercel or Railway

echo "╔════════════════════════════════════════════════════════╗"
echo "║     Video Compressor - Deployment Helper              ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Git not initialized. Initializing..."
    git init
    echo "✅ Git initialized"
    echo ""
fi

# Create .gitignore if it doesn't exist
if [ ! -f .gitignore ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.log
web/uploads/*
web/compressed/*
!web/uploads/.gitkeep
!web/compressed/.gitkeep
.env
venv/
*.mp4
*.webm
*.mov
.DS_Store
test_output/
*.output
EOF
    echo "✅ .gitignore created"
    echo ""
fi

# Create .gitkeep files
mkdir -p web/uploads web/compressed
touch web/uploads/.gitkeep web/compressed/.gitkeep

# Add all files
echo "📦 Adding files to git..."
git add .
echo "✅ Files added"
echo ""

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "ℹ️  No changes to commit"
else
    echo "💾 Creating commit..."
    git commit -m "Prepare for deployment - Video Compressor SDK"
    echo "✅ Commit created"
fi
echo ""

echo "╔════════════════════════════════════════════════════════╗"
echo "║     Choose Deployment Method                           ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "1. 🚀 Vercel (Quick demo, 10s timeout limit)"
echo "2. 🚂 Railway (Recommended for production, no timeout)"
echo "3. 📚 Show deployment guides"
echo "4. ❌ Exit"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "╔════════════════════════════════════════════════════════╗"
        echo "║     Deploying to Vercel                                ║"
        echo "╚════════════════════════════════════════════════════════╝"
        echo ""

        # Check if vercel is installed
        if ! command -v vercel &> /dev/null; then
            echo "⚠️  Vercel CLI not found."
            echo ""
            echo "Install it with:"
            echo "  npm install -g vercel"
            echo "  or"
            echo "  brew install vercel-cli"
            echo ""
            read -p "Open installation guide? (y/n): " open_guide
            if [ "$open_guide" = "y" ]; then
                open "https://vercel.com/docs/cli"
            fi
            exit 1
        fi

        echo "🔑 Logging into Vercel..."
        vercel login

        echo ""
        echo "📦 Deploying to production..."
        cd web
        vercel --prod

        echo ""
        echo "✅ Deployment complete!"
        echo "⚠️  Remember: Vercel has a 10 second timeout."
        echo "    Only use with very short videos or upgrade to Pro."
        echo ""
        ;;

    2)
        echo ""
        echo "╔════════════════════════════════════════════════════════╗"
        echo "║     Deploying to Railway                               ║"
        echo "╚════════════════════════════════════════════════════════╝"
        echo ""
        echo "Railway deployment requires GitHub."
        echo ""
        echo "Steps:"
        echo "1. ✅ Your code is ready (already committed)"
        echo "2. 📤 Push to GitHub"
        echo "3. 🔗 Connect Railway to your GitHub repo"
        echo "4. 🚀 Deploy!"
        echo ""
        read -p "Do you have a GitHub repository URL? (y/n): " has_repo

        if [ "$has_repo" = "y" ]; then
            read -p "Enter GitHub repository URL: " repo_url
            echo ""
            echo "📤 Adding remote and pushing..."
            git remote add origin "$repo_url" 2>/dev/null || git remote set-url origin "$repo_url"
            git branch -M main
            git push -u origin main
            echo ""
            echo "✅ Pushed to GitHub!"
            echo ""
            echo "Next steps:"
            echo "1. Go to https://railway.app"
            echo "2. Sign up with GitHub"
            echo "3. Click 'New Project' → 'Deploy from GitHub repo'"
            echo "4. Select your repository"
            echo "5. Railway will auto-deploy!"
            echo ""
            read -p "Open Railway? (y/n): " open_railway
            if [ "$open_railway" = "y" ]; then
                open "https://railway.app"
            fi
        else
            echo ""
            echo "Please create a GitHub repository first:"
            echo "1. Go to https://github.com/new"
            echo "2. Name it: video-compressor-sdk"
            echo "3. Click 'Create repository'"
            echo "4. Run this script again"
            echo ""
            read -p "Open GitHub? (y/n): " open_github
            if [ "$open_github" = "y" ]; then
                open "https://github.com/new"
            fi
        fi
        ;;

    3)
        echo ""
        echo "📚 Opening deployment guides..."
        echo ""
        echo "Available guides:"
        echo "  • DEPLOYMENT.md - Complete guide for all platforms"
        echo "  • web/DEPLOY_NOW.md - Quick Vercel deployment"
        echo ""
        cat DEPLOYMENT.md
        ;;

    4)
        echo ""
        echo "👋 Exiting..."
        exit 0
        ;;

    *)
        echo ""
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║     Deployment Complete! 🎉                            ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📖 For more help, see:"
echo "   • DEPLOYMENT.md (full guide)"
echo "   • web/DEPLOY_NOW.md (Vercel quick start)"
echo ""
