#!/bin/bash
# Deployment script for Andalusian Archive
# Usage: ./deploy.sh [commit_message]

set -e

COMMIT_MSG=${1:-"Update archive content"}
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== Andalusian Archive Deployment ==="
echo ""

# Check if we're in a git repo
if [ ! -d "$REPO_DIR/.git" ]; then
    echo "Initializing git repository..."
    cd "$REPO_DIR"
    git init
    git remote add origin https://github.com/YOUR_USERNAME/andalusian-archive.git
fi

cd "$REPO_DIR"

# Build the site
echo "Building Jekyll site..."
bundle exec jekyll build

# Check for changes
echo "Checking for changes..."
if git diff --quiet; then
    echo "No changes to commit."
    exit 0
fi

# Stage and commit
echo "Staging changes..."
git add -A

echo "Committing changes..."
git commit -m "$COMMIT_MSG"

# Push to GitHub
echo "Pushing to GitHub..."
git push origin main

echo ""
echo "=== Deployment complete! ==="
echo "Site will be available at: https://YOUR_USERNAME.github.io/andalusian-archive/"
