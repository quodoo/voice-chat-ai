#!/bin/bash

# Voice Chat AI - macOS Installation Script
# Cài đặt tự động toàn bộ ứng dụng trên macOS

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   Voice Chat AI - macOS Installation                     ║"
echo "║   Auto setup script for Apple Silicon & Intel Macs       ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check Python version
echo -e "${YELLOW}1️⃣  Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found!${NC}"
    echo "Install Python 3.11+:"
    echo "  brew install python@3.11"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

# Check if already in virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${YELLOW}2️⃣  Creating virtual environment...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    echo -e "${GREEN}✓ Virtual environment created and activated${NC}"
else
    echo -e "${GREEN}✓ Already in virtual environment${NC}"
fi

# Upgrade pip
echo -e "${YELLOW}3️⃣  Upgrading pip...${NC}"
pip install --quiet --upgrade pip setuptools wheel
echo -e "${GREEN}✓ Pip upgraded${NC}"

# Install dependencies
echo -e "${YELLOW}4️⃣  Installing Python dependencies...${NC}"
if [ -f "requirements.txt" ]; then
    pip install --quiet -r requirements.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${RED}❌ requirements.txt not found${NC}"
    exit 1
fi

# Create Kokoro directories
echo -e "${YELLOW}5️⃣  Setting up Kokoro TTS directories...${NC}"
KOKORO_DIR="$HOME/ComfyUI/models/Kokorotts/Kokoro-82M/voices"
mkdir -p "$KOKORO_DIR"
echo -e "${GREEN}✓ Created: $KOKORO_DIR${NC}"

# Download English voices
echo -e "${YELLOW}6️⃣  Downloading Kokoro English voices...${NC}"
if [ -f "kokoro-tts-server/download_english_voices.sh" ]; then
    chmod +x kokoro-tts-server/download_english_voices.sh
    ./kokoro-tts-server/download_english_voices.sh
    echo -e "${GREEN}✓ English voices downloaded${NC}"
else
    echo -e "${YELLOW}⚠️  Voice download script not found (optional)${NC}"
fi

# Create .env file if not exists
echo -e "${YELLOW}7️⃣  Creating environment configuration...${NC}"
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# Language: en (English) or ja (Japanese)
LANGUAGE_CODE=en

# LLM Model Provider: ollama, openai, anthropic, xai
MODEL_PROVIDER=ollama
CHARACTER_NAME=bigfoot

# Ollama Configuration
OLLAMA_MODEL=qwen2:7b
OLLAMA_BASE_URL=http://localhost:11434/v1

# TTS Configuration
TTS_PROVIDER=Kokoro-TTS
KOKORO_TTS_VOICE=af_nova
KOKORO_BASE_URL=http://localhost:8880/v1

# Whisper/Transcription
FASTER_WHISPER_LOCAL=true

# Optional: OpenAI API
# OPENAI_API_KEY=your-key-here
# OPENAI_MODEL=gpt-4o-mini

# Optional: Anthropic API
# ANTHROPIC_API_KEY=your-key-here
EOF
    echo -e "${GREEN}✓ Created .env file (edit to customize)${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Make scripts executable
echo -e "${YELLOW}8️⃣  Setting up executable scripts...${NC}"
chmod +x start_server.sh 2>/dev/null || true
chmod +x kokoro-tts-server/download_english_voices.sh 2>/dev/null || true
echo -e "${GREEN}✓ Scripts made executable${NC}"

# Installation complete
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗"
echo "║   ✅ Installation Complete!                              ║"
echo "╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo ""
echo "1️⃣  Install Ollama (if not already installed):"
echo "   Download from: https://ollama.ai/"
echo "   Or: brew install ollama"
echo ""
echo "2️⃣  Download your first model:"
echo "   ollama pull qwen2:7b"
echo ""
echo "3️⃣  Start all servers:"
echo "   ./start_server.sh"
echo ""
echo "4️⃣  Open in browser:"
echo "   http://localhost:8000"
echo ""
echo -e "${YELLOW}📝 Important:${NC}"
echo "  • Make sure Ollama is running before starting the app"
echo "  • Edit .env file to configure models and settings"
echo "  • Check SETUP_MAC.md for detailed documentation"
echo ""
echo -e "${GREEN}Happy Voice Chatting! 🎉${NC}"
echo ""
