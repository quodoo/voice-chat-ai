#!/usr/bin/env python3
"""
Simple Kokoro TTS API Server compatible with OpenAI TTS API format
Run this on port 8880 to use with voice-chat-ai
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
import uvicorn
from kokoro_onnx import Kokoro

app = FastAPI(title="Kokoro TTS Server")

# Model paths
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.join(MODEL_DIR, "kokoro-v1.0.fp16.onnx")
VOICES_FILE = os.path.join(MODEL_DIR, "voices.bin")

# Check if model files exist
if not os.path.exists(MODEL_FILE):
    print(f"\n❌ Model file not found: {MODEL_FILE}")
    print("📥 Please download: https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.fp16.onnx")
    print(f"   and save it as: {MODEL_FILE}\n")
    exit(1)

if not os.path.exists(VOICES_FILE):
    print(f"\n❌ Voices file not found: {VOICES_FILE}")
    print("📥 Please download: https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin")
    print(f"   and save it as: {VOICES_FILE}\n")
    exit(1)

# Initialize Kokoro model
print("Loading Kokoro FP16 model (optimized for Mac M4)...")
kokoro = Kokoro(MODEL_FILE, VOICES_FILE)
print("✅ Kokoro model loaded!")

class TTSRequest(BaseModel):
    model: str = "kokoro"
    input: str
    voice: str = "af_bella"
    speed: float = 1.0
    response_format: str = "wav"

@app.get("/")
async def root():
    return {"status": "Kokoro TTS Server is running", "port": 8880}

@app.get("/v1/audio/voices")
async def list_voices():
    """List available Kokoro voices"""
    voices = [
        "af_bella", "af_sarah", "af_nicole", 
        "am_adam", "am_michael",
        "bf_emma", "bf_isabella",
        "bm_george", "bm_lewis"
    ]
    return {"voices": voices}

@app.post("/v1/audio/speech")
async def text_to_speech(request: TTSRequest):
    """Generate speech from text using Kokoro TTS"""
    try:
        # Generate audio using Kokoro-ONNX
        samples, sample_rate = kokoro.create(
            request.input,
            voice=request.voice,
            speed=request.speed,
            lang="en-us"
        )
        
        # Convert to WAV format
        import io
        import wave
        import numpy as np
        
        # Normalize to 16-bit PCM
        audio_data = (samples * 32767).astype(np.int16)
        
        # Create WAV in memory
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        
        wav_buffer.seek(0)
        
        return Response(
            content=wav_buffer.read(),
            media_type="audio/wav"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🎤 Starting Kokoro TTS Server on http://localhost:8880")
    print("📝 Compatible with OpenAI TTS API format")
    print("🔊 Available at: http://localhost:8880/v1/audio/speech")
    print("\nPress CTRL+C to stop\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8880, log_level="info")
