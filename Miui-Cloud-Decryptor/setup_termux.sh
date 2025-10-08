#!/bin/bash

# MIUI Cloud Decryptor - Termux Setup Script
# This script automates the installation process for Termux

echo "========================================"
echo "🔓 MIUI Cloud Decryptor Setup for Termux"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running in Termux
if [[ ! "$PREFIX" == *"termux"* ]]; then
    print_warning "This script is designed for Termux. Continue anyway? (y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

print_status "Starting setup process..."

# Update packages
print_status "Updating Termux packages..."
pkg update -y && pkg upgrade -y

# Install Python if not already installed
if ! command -v python &> /dev/null; then
    print_status "Installing Python..."
    pkg install python -y
else
    print_status "Python is already installed"
fi

# Install pip if not available
if ! command -v pip &> /dev/null; then
    print_status "Installing pip..."
    pkg install python-pip -y
else
    print_status "pip is already installed"
fi

# Install required Python packages
print_status "Installing Python dependencies..."
pip install Flask==2.3.3 pycryptodome==3.19.0 filetype==1.2.0 Werkzeug==2.3.7

# Setup storage permissions
print_status "Setting up storage permissions..."
termux-setup-storage

# Create directories
print_status "Creating necessary directories..."
mkdir -p uploads decrypted

# Set executable permissions
chmod +x setup_termux.sh

# Get device IP for network access
IP_ADDRESS=$(ifconfig wlan0 2>/dev/null | grep 'inet ' | awk '{print $2}' | cut -d: -f2)
if [ -z "$IP_ADDRESS" ]; then
    IP_ADDRESS=$(ip route get 8.8.8.8 2>/dev/null | awk '{print $7; exit}')
fi

echo ""
echo "========================================"
print_status "Setup completed successfully!"
echo "========================================"
echo ""
print_status "To start the web application, run:"
echo "    python app.py"
echo ""
print_status "To configure Telegram integration (optional):"
echo "    export TELEGRAM_BOT_TOKEN='your_bot_token'"
echo "    export TELEGRAM_USER_ID='your_user_id'"
echo "    python app.py"
echo ""
print_status "Access the web app at:"
echo "    Local:   http://localhost:5000"
if [ ! -z "$IP_ADDRESS" ]; then
    echo "    Network: http://$IP_ADDRESS:5000"
fi
echo ""
print_status "Features:"
echo "  ✓ Upload .lsa/.lsav files or ZIP archives"
echo "  ✓ Automatic decryption and file type detection"
echo "  ✓ Mobile-friendly interface"
echo "  ✓ Batch processing support"
echo "  ✓ API endpoint for automation"
echo "  ✓ Optional Telegram integration"
echo ""
print_warning "Note: Make sure your encrypted files follow the naming pattern:"
print_warning "<filename>.<md5_hash>.lsa or <filename>.<md5_hash>.lsav"
echo ""
print_status "© 2025 The Apophis Code. All rights reserved."
print_status "Telegram Channel: https://t.me/TheApophisCode"
echo ""
print_status "Enjoy using MIUI Cloud Decryptor! 🚀"