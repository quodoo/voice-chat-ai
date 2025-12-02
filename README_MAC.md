# 🍎 Voice Chat AI - macOS Quick Start

**Voice Chat AI** là ứng dụng hội thoại AI thông qua giọng nói, tối ưu hóa cho macOS (Apple Silicon & Intel).

## ⚡ Quick Installation (5 phút)

### Bước 1: Chuẩn bị

```bash
# Cài Homebrew (nếu chưa có)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Cài Python 3.11+
brew install python@3.11 ffmpeg portaudio

# Cài Ollama
brew install ollama
# Hoặc download từ https://ollama.ai/
```

### Bước 2: Clone & Install

```bash
# Clone project
git clone https://github.com/your-repo/voice-chat-ai.git
cd voice-chat-ai

# Chạy auto installer
chmod +x install_mac.sh
./install_mac.sh
```

### Bước 3: Run

**Terminal 1 - Ollama:**
```bash
ollama serve
```

**Terminal 2 - Voice Chat AI:**
```bash
cd voice-chat-ai
source venv/bin/activate
./start_server.sh
```

**Browser:**
```
http://localhost:8000
```

Done! 🎉

---

## 📖 Full Documentation

Xem file `SETUP_MAC.md` để có hướng dẫn chi tiết:
- Advanced configuration
- Troubleshooting
- Performance optimization
- Multiple model setup

---

## 🎯 Features

✅ Voice input/output (English & Japanese)
✅ 30+ AI characters
✅ Multiple LLM providers (Ollama, OpenAI, Anthropic)
✅ Text-to-speech (Kokoro TTS, ElevenLabs, OpenAI)
✅ Speech-to-text (Whisper)
✅ Web UI + API

---

## 🛠️ System Requirements

- **macOS 12+** (Monterey or later)
- **Python 3.10+**
- **4GB RAM** (8GB recommended)
- **5GB disk space** (for models)

**Supported Macs:**
- Apple Silicon (M1, M2, M3, etc.) ⭐ Optimized
- Intel Macs (with MPS fallback)

---

## ⚙️ Configuration

Edit `.env` file:

```bash
# Language
LANGUAGE_CODE=en  # or ja

# AI Model
MODEL_PROVIDER=ollama
OLLAMA_MODEL=qwen2:7b

# TTS Voice
TTS_PROVIDER=Kokoro-TTS
KOKORO_TTS_VOICE=af_nova  # American English Female

# Character
CHARACTER_NAME=bigfoot
```

---

## 🚀 Recommended Models

### LLM Models (Ollama)
```bash
ollama pull qwen2:7b      # 7B - Fast & good quality
ollama pull mistral       # 7B - Alternative
ollama pull neural-chat   # 13B - Better quality
```

### TTS Voices
- **English (American)**: af_nova, af_bella, am_adam, am_echo
- **English (British)**: bf_emma, bf_alice, bm_daniel, bm_fable
- **Japanese**: jf_alpha, jm_kumo
- **Other**: Spanish, French, Hindi, Chinese

---

## 🎤 Usage Examples

### Via Web UI
1. Select character
2. Select language
3. Click "Start" button
4. Speak into microphone
5. AI responds with voice

### Via API
```bash
# Start conversation
curl -X POST http://localhost:8000/start_conversation

# Send text message
curl -X POST http://localhost:8000/ws
```

---

## 📊 Performance (M1/M2 Mac)

| Model | Speed | CPU | Memory | Quality |
|-------|-------|-----|--------|---------|
| tiny.en | ⚡⚡⚡ | 20% | 400MB | Good |
| small | ⚡⚡ | 40% | 600MB | Good |
| medium.en | ⚡ | 70% | 1GB | Very Good |
| qwen2:7b | ⚡⚡⚡ | 60% | 4GB | Good |

---

## 🐛 Troubleshooting

### "Port 8000 already in use"
```bash
lsof -i :8000
kill -9 <PID>
```

### "Ollama not found"
```bash
# Restart Ollama
brew services restart ollama

# Or manually:
ollama serve
```

### "Kokoro voices not found"
```bash
ls ~/ComfyUI/models/Kokorotts/Kokoro-82M/voices/
./kokoro-tts-server/download_english_voices.sh
```

### High CPU usage
Edit `app/transcription.py`:
```python
model_size = "tiny.en"  # Smaller model = less CPU
```

---

## 📞 Support & Links

- **GitHub**: [voice-chat-ai](https://github.com/your-repo)
- **Ollama**: [ollama.ai](https://ollama.ai)
- **Kokoro TTS**: [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)
- **Issues**: Create GitHub issue

---

## 📜 License

MIT License - See LICENSE file

---

**Made with ❤️ for macOS**
