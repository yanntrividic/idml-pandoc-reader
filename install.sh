#!/bin/bash

###############################################################################
# install.sh – Installation script for idml2docbook
#
# This script performs a full environment check and setup for the idml2docbook
# toolchain. It ensures all required dependencies are installed, clones
# the necessary frontend repository, prepares configuration, and optionally
# installs the module as a pip package.
#
# Functionality:
# - Verifies Java (>= 7.0.0) is installed
# - Verifies Git is installed
# - Prompts for a target directory to clone the `idml2xml-frontend` repo
# - Clones the repository (if not already present and correct)
# - Verifies Python 3 and pip (>= 21.0) are installed
# - Ensures a virtual environment is active (or warns otherwise)
# - Installs Python dependencies from `requirements.txt`
# - Copies `.env.sample` to `.env` if needed, and sets correct frontend path
# - Optionally installs the module using `pip install .`
#
# Prerequisites:
# - Bash shell
# - Java >= 7.0.0
# - Git
# - Python 3.x with pip >= 21.0
#
# Usage:
#   chmod +x install.sh
#   ./install.sh
#
# Author: Yann Trividic
# Repository: https://gitlab.com/deborderbollore/idml-pandoc-reader
###############################################################################

# Function to compare version numbers
version_greater_equal() {
    # Usage: version_greater_equal "7.0.0" "7.1.0"
    [ "$(printf '%s\n' "$1" "$2" | sort -V | head -n1)" = "$1" ]
}

echo "Checking Java version..."
if command -v java >/dev/null 2>&1; then
    JAVA_VERSION=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}')
    echo "Java version: $JAVA_VERSION"
    if version_greater_equal "7.0.0" "$JAVA_VERSION"; then
        echo "✅ Java version is sufficient."
    else
        echo "❌ Java version must be >= 7.0.0"
        exit 1
    fi
else
    echo "❌ Java is not installed. Please install Java (>=7.0.0)"
    exit 1
fi

echo "Checking Git installation..."
if command -v git >/dev/null 2>&1; then
    echo "✅ Git is installed: $(git --version)"
else
    echo "❌ Git is not installed. Please install git"
    exit 1
fi

# Default to current directory
DEFAULT_DIR="$(pwd)"

# Prompt the user
read -p "Enter directory to clone the repo into [${DEFAULT_DIR}]: " CLONE_DIR

# Use default if user presses enter
CLONE_DIR="${CLONE_DIR:-$DEFAULT_DIR}"

# Add your repo name to the path (optional)
REPO_NAME="idml2xml-frontend"
IDML2XML_FRONTEND_TARGET_DIR="${CLONE_DIR}/${REPO_NAME}"

# Check if repo already exists
EXPECTED_URL="https://github.com/transpect/idml2xml-frontend.git"

if [ -d "$IDML2XML_FRONTEND_TARGET_DIR/.git" ]; then
    ACTUAL_URL=$(git -C "$IDML2XML_FRONTEND_TARGET_DIR" remote get-url origin)
    if [ "$ACTUAL_URL" = "$EXPECTED_URL" ]; then
        echo "✅ Repository already exists at $IDML2XML_FRONTEND_TARGET_DIR and is correct."
    else
        echo "⚠️ Found a Git repo at $IDML2XML_FRONTEND_TARGET_DIR, but remote URL does not match."
        echo "Expected: $EXPECTED_URL"
        echo "Found:    $ACTUAL_URL"
        exit 1
    fi
else
    echo "📦 Cloning $REPO_NAME and submodules into $IDML2XML_FRONTEND_TARGET_DIR..."
    git clone "$EXPECTED_URL" "$IDML2XML_FRONTEND_TARGET_DIR" --recurse-submodules || { echo "❌ Git clone failed."; exit 1; }
fi

if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️ You are NOT in a virtual environment. This installation script will install Python dependencies. It is highly recommended to activate a virtual environment before continuing."
    read -p "Continue anyway? [y/n] " RESP
    if [[ ! "$RESP" =~ ^[Yy]$ ]]; then
        echo "❌ Aborting. Activate a venv first."
        exit 1
    fi
else
    echo "✅ Virtual environment detected: $VIRTUAL_ENV"
fi

echo "Checking Python version..."
if command -v python3 >/dev/null 2>&1; then
    PYTHON_VERSION=$(python3 -c 'import platform; print(platform.python_version())')
    echo "Python version: $PYTHON_VERSION"
    if version_greater_equal "3.0.0" "$PYTHON_VERSION"; then
        echo "✅ Python version is sufficient."
    else
        echo "❌ Python version must be >= 3.0.0"
        exit 1
    fi
else
    echo "❌ Python 3 is not installed. Please install Python (>=3.0.0)"
    exit 1
fi

# Try to find pip or pip3
if command -v pip &> /dev/null; then
    PIP_CMD="pip"
elif command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
else
    echo "❌ Neither pip nor pip3 is installed."
    exit 1
fi

# echo "✅ Using $PIP_CMD"

# Extract the pip version
INSTALLED_PIP_VERSION=$($PIP_CMD --version | awk '{print $2}')
REQUIRED_PIP_VERSION="21.0"

# Compare versions
version_greater() {
    [ "$(printf '%s\n' "$1" "$2" | sort -V | head -n1)" != "$1" ]
}

if version_greater "$REQUIRED_PIP_VERSION" "$INSTALLED_PIP_VERSION"; then
    echo "❌ $PIP_CMD version must be > $REQUIRED_PIP_VERSION. Found: $INSTALLED_PIP_VERSION"
    exit 1
else
    echo "✅ $PIP_CMD version $INSTALLED_PIP_VERSION is sufficient."
fi

# Attempt to install from requirements.txt
echo "📦 Installing dependencies from requirements.txt..."

if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found in current directory: $(pwd)"
    exit 1
fi

# Run the pip install command
$PIP_CMD install -r requirements.txt

# Check the exit code
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully."
else
    echo "❌ pip install failed. Check errors above."
    exit 1
fi

# 1. Check for .env
if [ -f ".env" ]; then
    echo "✅ .env file already exists. Skipping creation."
else
    # 2. Check if .env.sample exists
    if [ ! -f ".env.sample" ]; then
        echo "❌ .env.sample not found. Cannot create .env."
        exit 1
    fi

    echo "📝 Creating .env file from .env.sample..."
    cp .env.sample .env

    # 3. Replace the value of IDML2HUBXML_SCRIPT_FOLDER in .env
    # Use `sed` to replace the line (make sure to escape slashes)
    ESCAPED_PATH=$(printf '%s\n' "$IDML2XML_FRONTEND_TARGET_DIR" | sed 's:/:\\/:g')

    sed -i "s|^IDML2HUBXML_SCRIPT_FOLDER=.*$|IDML2HUBXML_SCRIPT_FOLDER=\"$ESCAPED_PATH\"|" .env

    echo "✅ .env file created and updated with install path of idml2xml-frontend."
    echo "📍 IDML2HUBXML_SCRIPT_FOLDER=$IDML2XML_FRONTEND_TARGET_DIR"
fi

echo ""
read -p "🚀 Do you want to build the module now using '$PIP_CMD install .'? This step is not necessary, but it will allow you to execute idml2docbook from outside this directory. Continue? [y/n]: " BUILD_CONFIRM

# Default to yes if user just presses enter
BUILD_CONFIRM=${BUILD_CONFIRM:-Y}

if [[ "$BUILD_CONFIRM" =~ ^[Yy]$ ]]; then
    echo "📦 Installing module with '$PIP_CMD install .'..."
    $PIP_CMD install . || {
        echo "❌ pip install failed."
        exit 1
    }
    echo "✅ Module installed successfully."
else
    echo "⏩ Skipping module build as requested."
fi

echo "✅ All checks passed. Installation complete."