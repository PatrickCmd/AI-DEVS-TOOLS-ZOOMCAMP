#!/bin/bash

# Quick Start Script for FreeCodeCamp MCP Server and OpenAI Agent Client
# This script helps you quickly set up and run the system

set -e  # Exit on error

echo "========================================"
echo "🚀 FreeCodeCamp MCP Server Quick Start"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

print_success "Python 3 is installed"

# Check if .env file exists
if [ ! -f .env ]; then
    print_info "Creating .env file..."
    echo "OPENAI_API_KEY=your-api-key-here" > .env
    echo "MCP_SERVER_URL=http://localhost:8000" >> .env
    echo "OPENAI_MODEL=gpt-4o-mini" >> .env
    print_success ".env file created"
    print_error "Please edit .env file and add your OpenAI API key!"
    echo ""
    echo "Edit the .env file:"
    echo "  nano .env"
    echo ""
    echo "Then run this script again."
    exit 1
else
    print_success ".env file exists"
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_info "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Install dependencies
print_info "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
pip install -q -r requirements_client.txt
print_success "Dependencies installed"

echo ""
echo "========================================"
echo "Setup complete! 🎉"
echo "========================================"
echo ""

# Ask what to run
echo "What would you like to do?"
echo "1. Start MCP Server"
echo "2. Run Basic Client (after server is running)"
echo "3. Run Advanced Client (after server is running)"
echo "4. Run Server and Client (in separate terminals)"
echo "5. Exit"
echo ""

read -p "Enter choice (1-5): " choice

case $choice in
    1)
        print_info "Starting MCP Server on http://localhost:8000..."
        echo ""
        python feed_deployment.py
        ;;
    2)
        print_info "Starting Basic Client..."
        echo ""
        python agent_client.py
        ;;
    3)
        print_info "Starting Advanced Client..."
        echo ""
        python agent_client_advanced.py
        ;;
    4)
        print_info "Starting server in background..."
        python feed_deployment.py > server.log 2>&1 &
        SERVER_PID=$!
        print_success "Server started (PID: $SERVER_PID)"
        print_info "Waiting for server to be ready..."
        sleep 5

        print_info "Starting client..."
        python agent_client.py

        print_info "Stopping server..."
        kill $SERVER_PID
        print_success "Server stopped"
        ;;
    5)
        print_info "Exiting..."
        exit 0
        ;;
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac
