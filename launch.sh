#!/bin/bash

# StellarForge Launch Script for Linux/Unix
# Quick launcher for StellarForge application

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  Launching StellarForge${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}✗ Virtual environment not found${NC}"
    echo -e "${YELLOW}  Please run install.sh first:${NC}"
    echo -e "    ./install.sh"
    echo ""
    exit 1
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Failed to activate virtual environment${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Launch application
echo -e "${CYAN}Starting StellarForge...${NC}"
echo ""
python main.py

# Capture exit code
EXIT_CODE=$?

# Deactivate virtual environment
deactivate

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ StellarForge closed successfully${NC}"
else
    echo -e "${RED}✗ StellarForge exited with error code: $EXIT_CODE${NC}"
fi
echo ""

exit $EXIT_CODE
