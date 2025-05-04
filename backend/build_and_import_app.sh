#!/bin/bash

# Exit on any error
set -e
echo "🚀 Starting build and deployment process..."

# Define paths relative to script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$(dirname "$SCRIPT_DIR")/frontend"
BACKEND_DIR="$SCRIPT_DIR"
BACKEND_STATIC_DIR="$BACKEND_DIR/app/static"

# Check if frontend directory exists
if [ ! -d "$FRONTEND_DIR" ]; then
    echo "❌ Frontend directory not found!"
    exit 1
fi

# Check if backend directory exists
if [ ! -d "$BACKEND_DIR" ]; then
    echo "❌ Backend directory not found!"
    exit 1
fi

# Build frontend
echo "📦 Building Astro frontend..."
cd "$FRONTEND_DIR"
npm run build

# Ensure backend static directory exists
echo "📁 Setting up static directory in backend..."
mkdir -p "$BACKEND_STATIC_DIR"

# Clean existing static files in backend
echo "🧹 Cleaning existing static files..."
rm -rf "$BACKEND_STATIC_DIR"/*

# Copy frontend dist to backend static directory
echo "📋 Copying frontend build to backend..."
cp -r dist/* "$BACKEND_STATIC_DIR/"

echo "✅ Build and copy process completed!"