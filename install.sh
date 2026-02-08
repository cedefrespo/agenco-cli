#!/bin/bash
# Agenco CLI Installer
# Installs Agenco CLI and adds it to PATH

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════╗"
echo "║        AGENCO CLI INSTALLER            ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: git is not installed${NC}"
    exit 1
fi

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 is not installed${NC}"
    exit 1
fi

# Installation directory
INSTALL_DIR="$HOME/agenco-cli"

echo -e "${YELLOW}Installing to: $INSTALL_DIR${NC}"

# Clone or update repository
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}Updating existing installation...${NC}"
    cd "$INSTALL_DIR"
    git pull
else
    echo -e "${YELLOW}Cloning repository...${NC}"
    git clone https://github.com/cedefrespo/agenco-cli.git "$INSTALL_DIR"
fi

# Install Python dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
cd "$INSTALL_DIR"
pip3 install -r requirements.txt --quiet

# Make executable
chmod +x "$INSTALL_DIR/agenco"

# Add to PATH
SHELL_RC=""
if [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [ -n "$SHELL_RC" ]; then
    if ! grep -q "agenco-cli" "$SHELL_RC"; then
        echo -e "${YELLOW}Adding to PATH in $SHELL_RC...${NC}"
        echo "" >> "$SHELL_RC"
        echo "# Agenco CLI" >> "$SHELL_RC"
        echo "export PATH=\"\$HOME/agenco-cli:\$PATH\"" >> "$SHELL_RC"
        
        echo -e "${GREEN}✓ Added to PATH${NC}"
        echo -e "${YELLOW}Run: source $SHELL_RC${NC}"
    else
        echo -e "${GREEN}✓ Already in PATH${NC}"
    fi
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     Installation Complete! 🎉         ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Quick Start:${NC}"
echo -e "  1. Reload your shell: ${YELLOW}source $SHELL_RC${NC}"
echo -e "  2. Run interactive mode: ${YELLOW}agenco${NC}"
echo -e "  3. Or use commands: ${YELLOW}agenco agents${NC}"
echo ""
echo -e "${BLUE}Documentation:${NC} https://agenco.dev/cli"
echo -e "${BLUE}GitHub:${NC} https://github.com/cedefrespo/agenco-cli"
echo ""
