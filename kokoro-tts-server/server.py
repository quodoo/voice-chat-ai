#!/usr/bin/env python3
"""
Kokoro PyTorch TTS Server with Multi-language voice support
Compatible with OpenAI TTS API format
Uses Kokoro-82M model from ComfyUI
Supports: English (American, British), Japanese, Chinese, Spanish, French, Hindi, Portuguese
"""

import os
import sys
import torch
import numpy as np
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
import uvicorn
import io
import wave
from kokoro import KPipeline

# Global pipeline and device
pipeline = None
device = None

def load_pipeline():
    """Initialize Kokoro pipeline"""
    global pipeline, device
    
    # Detect device
    if torch.backends.mps.is_available():
        device = "mps"
    elif torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    
    print(f"Using device: {device}")
    
    # Initialize pipeline (default American English)
    pipeline = KPipeline(lang_code='a')
    print("✅ Kokoro pipeline initialized!")
    
    return pipeline

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    load_pipeline()
    yield
    # Shutdown
    global pipeline, device
    if pipeline is not None:
        pipeline = None
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    print("🛑 Kokoro pipeline shutdown")

app = FastAPI(title="Kokoro TTS Server - Multi-language", lifespan=lifespan)

# Model paths
MODEL_DIR = "/Users/quangtv/ComfyUI/models/Kokorotts/Kokoro-82M"
MODEL_FILE = os.path.join(MODEL_DIR, "kokoro-v1_0.pth")
VOICES_DIR = os.path.join(MODEL_DIR, "voices")

# Voice language mapping - curated selection of best voices
SPEAKER_LANG_MAPPING = {
    "a": [  # American English (2 female + 2 male, curated)
        "af_nova",      # Female - natural, warm, recommended
        "af_bella",     # Female - clear, professional, recommended
        "am_adam",      # Male - neutral, friendly, recommended
        "am_echo",      # Male - strong, confident, recommended
    ],
    "b": [  # British English (2 female + 2 male, curated)
        "bf_emma",      # Female - elegant, clear, recommended
        "bf_alice",     # Female - friendly, natural, recommended
        "bm_daniel",    # Male - professional, deep, recommended
        "bm_fable",     # Male - smooth, warm, recommended
    ],
    "e": [  # European Spanish
        "ef_dora",
        "em_alex", "em_santa"
    ],
    "f": [  # French
        "ff_siwis"
    ],
    "h": [  # Hindi
        "hf_alpha", "hf_beta",
        "hm_omega", "hm_psi"
    ],
    "j": [  # Japanese
        "jf_alpha", "jf_gongitsune", "jf_nezumi", "jf_tebukuro",
        "jm_kumo"
    ],
    "p": [  # Portuguese / Brazilian Portuguese
        "pf_dora",
        "pm_alex", "pm_santa"
    ],
    "z": [  # Chinese
        "zf_xiaobei", "zf_xiaoni", "zf_xiaoxiao", "zf_xiaoyi",
        "zm_yunjian", "zm_yunxi", "zm_yunxia", "zm_yunyang"
    ]
}

# Get all available speakers
all_speakers = []
for speakers in SPEAKER_LANG_MAPPING.values():
    all_speakers.extend(speakers)

# Global pipeline
pipeline = None
device = None

def load_pipeline():
    """Initialize Kokoro pipeline"""
    global pipeline, device
    
    # Detect device
    if torch.backends.mps.is_available():
        device = "mps"
    elif torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    
    print(f"Using device: {device}")
    
    # Initialize pipeline (default American English)
    pipeline = KPipeline(lang_code='a')
    print("✅ Kokoro pipeline initialized!")
    
    return pipeline

def get_available_voices():
    """List all available voice files from disk"""
    voices = []
    if os.path.exists(VOICES_DIR):
        for file in os.listdir(VOICES_DIR):
            if file.endswith('.pt'):
                voices.append(file.replace('.pt', ''))
    return sorted(voices)

class TTSRequest(BaseModel):
    model: str = "kokoro"
    input: str
    voice: str = "am_adam"  # Default to American English male
    speed: float = 1.0
    response_format: str = "wav"

@app.get("/")
async def root():
    return {
        "status": "Kokoro TTS Server is running",
        "port": 8880,
        "model": "Kokoro-82M PyTorch",
        "device": str(device),
        "available_voices": len(get_available_voices()),
        "supported_languages": [
            "American English (a)",
            "British English (b)",
            "Spanish (e)",
            "French (f)",
            "Hindi (h)",
            "Japanese (j)",
            "Portuguese (p)",
            "Chinese (z)"
        ]
    }

@app.get("/v1/audio/voices")
async def list_voices():
    """List all available voices grouped by language"""
    voices = get_available_voices()
    
    # Organize voices by language
    organized_voices = []
    language_names = {
        'a': 'American English',
        'b': 'British English',
        'e': 'European Spanish',
        'f': 'French',
        'h': 'Hindi',
        'j': 'Japanese',
        'p': 'Portuguese',
        'z': 'Chinese'
    }
    
    # Add voices organized by language
    for lang_code in sorted(SPEAKER_LANG_MAPPING.keys()):
        lang_voices = SPEAKER_LANG_MAPPING[lang_code]
        # Add separator
        organized_voices.append(f"--- {language_names.get(lang_code, f'Language {lang_code}')} ---")
        # Add voices for this language
        for voice in lang_voices:
            if voice in voices:  # Only include voices that exist on disk
                organized_voices.append(voice)
    
    return {"voices": organized_voices, "count": len(voices)}

@app.post("/v1/audio/speech")
async def text_to_speech(request: TTSRequest):
    """Generate speech from text using Kokoro TTS"""
    try:
        # Check if voice file exists
        voice_file = os.path.join(VOICES_DIR, f"{request.voice}.pt")
        if not os.path.exists(voice_file):
            available = get_available_voices()
            raise HTTPException(
                status_code=404,
                detail=f"Voice '{request.voice}' not found. Available voices: {', '.join(available[:10])}..."
            )
        
        # Detect language from voice prefix (first character)
        lang_code = 'a'  # default American English
        if request.voice.startswith('b'):
            lang_code = 'b'  # British English
        elif request.voice.startswith('e'):
            lang_code = 'e'  # Spanish
        elif request.voice.startswith('f'):
            lang_code = 'f'  # French
        elif request.voice.startswith('h'):
            lang_code = 'h'  # Hindi
        elif request.voice.startswith('j'):
            lang_code = 'j'  # Japanese
        elif request.voice.startswith('p'):
            lang_code = 'p'  # Portuguese
        elif request.voice.startswith('z'):
            lang_code = 'z'  # Chinese
        
        # Create pipeline for specific language
        lang_pipeline = KPipeline(lang_code=lang_code, repo_id=None)
        
        # Generate audio - returns a generator that yields (graphemes, phonemes, audio_chunk)
        # Pass the voice name (without .pt extension)
        generator = lang_pipeline(
            request.input,
            voice=request.voice,
            speed=request.speed,
            split_pattern=r"\n+"
        )
        
        # Collect all audio chunks
        audio_chunks = []
        for i, (graphemes, phonemes, audio_data) in enumerate(generator):
            audio_chunks.append(audio_data)
        
        # Concatenate all chunks
        if len(audio_chunks) == 0:
            raise HTTPException(status_code=500, detail="No audio generated")
        
        audio = np.concatenate(audio_chunks, axis=0)
        
        # Kokoro always uses 24kHz sample rate
        sample_rate = 24000
        
        # Convert to 16-bit PCM WAV
        audio_int16 = (audio * 32767).astype(np.int16)
        
        # Create WAV buffer
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_int16.tobytes())
        
        wav_buffer.seek(0)
        
        return Response(
            content=wav_buffer.read(),
            media_type="audio/wav"
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🎤 Kokoro TTS Server - Multi-language Edition")
    print(f"📂 Model: {MODEL_FILE}")
    print(f"🔊 Voices: {VOICES_DIR}")
    print("🌍 Supported Languages:")
    print("   • American English (a_) - 20 voices")
    print("   • British English (b_) - 8 voices")
    print("   • Spanish (e_) - 3 voices")
    print("   • French (f_) - 1 voice")
    print("   • Hindi (h_) - 4 voices")
    print("   • Japanese (j_) - 5 voices")
    print("   • Portuguese (p_) - 3 voices")
    print("   • Chinese (z_) - 8 voices")
    print("🚀 Starting server on http://localhost:8880")
    print("\nAPI Endpoints:")
    print("   GET  / - Server status")
    print("   GET  /v1/audio/voices - List available voices")
    print("   POST /v1/audio/speech - Generate speech")
    print("\nPress CTRL+C to stop\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8880, log_level="info")
