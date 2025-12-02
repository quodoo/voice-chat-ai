#!/bin/bash

# Force UTF-8 encoding for the entire session
export PYTHONIOENCODING=utf-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Print encoding settings for verification
echo "PYTHONIOENCODING: $PYTHONIOENCODING"
echo "LANG: $LANG"
echo "LC_ALL: $LC_ALL"

# Change to script directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $TTS_PID 2>/dev/null
    kill $APP_PID 2>/dev/null
    wait $TTS_PID 2>/dev/null
    wait $APP_PID 2>/dev/null
    echo "✅ All servers stopped"
    exit 0
}

# Set trap to cleanup on SIGINT (Ctrl+C)
trap cleanup SIGINT SIGTERM

# Start Kokoro TTS Server in background
echo ""
echo "🎤 Starting Kokoro TTS Server..."
/Users/quangtv/ComfyUI/.venv/bin/python kokoro-tts-server/server.py &
TTS_PID=$!

# Wait for TTS server to start (give it 3 seconds)
sleep 3

# Check if TTS server started successfully
if ! kill -0 $TTS_PID 2>/dev/null; then
    echo "❌ Failed to start TTS Server"
    exit 1
fi

echo "✅ TTS Server started (PID: $TTS_PID)"
echo ""

# Start main uvicorn server
echo "🚀 Starting Voice Chat AI Server..."
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
APP_PID=$!

echo "✅ Voice Chat AI Server started (PID: $APP_PID)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 Services Running:"
echo "   • Kokoro TTS Server: http://localhost:8880"
echo "   • Voice Chat AI:     http://localhost:8000"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for both processes
wait $TTS_PID $APP_PID