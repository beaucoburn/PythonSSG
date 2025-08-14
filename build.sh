#!/bin/bash

# Build script for production deployment to GitHub Pages
# This script builds the site with the correct basepath for GitHub Pages

# Get the repository name from the current directory
REPO_NAME=$(basename $(pwd))

echo "Building site for GitHub Pages deployment..."
echo "Repository name: $REPO_NAME"
echo "Basepath will be: /$REPO_NAME/"

# Build the site with the repository name as basepath
python3 src/main.py "/$REPO_NAME/"

echo "Build completed! Site is ready for GitHub Pages deployment."
echo "The site will be available at: https://YOUR_USERNAME.github.io/$REPO_NAME/"
