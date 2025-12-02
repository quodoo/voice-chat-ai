#!/bin/bash

# Download Kokoro English voices from Hugging Face
# This script downloads American and British English voices for Kokoro TTS
# Source: https://huggingface.co/hexgrad/Kokoro-82M/tree/main/voices

set -e

VOICES_DIR="/Users/quangtv/ComfyUI/models/Kokorotts/Kokoro-82M/voices"
HF_BASE_URL="https://huggingface.co/hexgrad/Kokoro-82M/resolve/main/voices"

# Create directory if it doesn't exist
mkdir -p "$VOICES_DIR"

echo "🎤 Downloading Kokoro English Voices from Hugging Face"
echo "═══════════════════════════════════════════════════════"
echo "Destination: $VOICES_DIR"
echo ""

download_voice() {
    local voice_name=$1
    local filename="${voice_name}.pt"
    local filepath="$VOICES_DIR/$filename"
    
    if [ -f "$filepath" ]; then
        echo "  ✓ $filename (already exists)"
    else
        echo "  📥 Downloading $filename..."
        curl -L -o "$filepath" "$HF_BASE_URL/$filename" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "  ✅ $filename downloaded"
        else
            echo "  ❌ Failed to download $filename"
            rm -f "$filepath"
            return 1
        fi
    fi
}

# American English Female voices (af_*)
echo "📥 American English Female Voices (11 voices):"
AF_VOICES=("af_alloy" "af_aoede" "af_bella" "af_heart" "af_jessica" "af_kore" "af_nicole" "af_nova" "af_river" "af_sarah" "af_sky")
for voice in "${AF_VOICES[@]}"; do
    download_voice "$voice"
done

# American English Male voices (am_*)
echo ""
echo "📥 American English Male Voices (9 voices):"
AM_VOICES=("am_adam" "am_echo" "am_eric" "am_fenrir" "am_liam" "am_michael" "am_onyx" "am_puck" "am_santa")
for voice in "${AM_VOICES[@]}"; do
    download_voice "$voice"
done

# British English Female voices (bf_*)
echo ""
echo "📥 British English Female Voices (4 voices):"
BF_VOICES=("bf_alice" "bf_emma" "bf_isabella" "bf_lily")
for voice in "${BF_VOICES[@]}"; do
    download_voice "$voice"
done

# British English Male voices (bm_*)
echo ""
echo "📥 British English Male Voices (4 voices):"
BM_VOICES=("bm_daniel" "bm_fable" "bm_george" "bm_lewis")
for voice in "${BM_VOICES[@]}"; do
    download_voice "$voice"
done

echo ""
echo "═══════════════════════════════════════════════════════"
echo "✅ English voices download complete!"
echo ""
echo "📊 Downloaded:"
echo "   • American English: 20 voices (11 female + 9 male)"
echo "   • British English: 8 voices (4 female + 4 male)"
echo "   • Total: 28 English voices"
echo ""
echo "Voice files are now ready in:"
echo "   $VOICES_DIR"
echo ""
