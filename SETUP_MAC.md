# Voice Chat AI - macOS Setup Guide

Hướng dẫn cài đặt toàn bộ **Voice Chat AI** trên macOS (Apple Silicon & Intel)

## 📋 Yêu cầu hệ thống

- **macOS 12+** (Monterey hoặc mới hơn)
- **Python 3.10+**
- **Homebrew** (package manager cho macOS)
- **3GB+ RAM** (tối thiểu)
- **5GB+ dung lượng ổ cứng** (cho models)

---

## 🚀 Installation Steps

### 1️⃣ Chuẩn bị môi trường

#### Cài đặt Homebrew (nếu chưa có)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Cài đặt Python 3.11+
```bash
brew install python@3.11
brew link python@3.11
python3 --version
```

#### Cài đặt các công cụ cần thiết
```bash
brew install git ffmpeg portaudio
```

---

### 2️⃣ Clone & Setup Project

```bash
# Clone repository
git clone https://github.com/your-repo/voice-chat-ai.git
cd voice-chat-ai

# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

---

### 3️⃣ Cài đặt Python Dependencies

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Nếu gặp lỗi pyaudio, cài từ Homebrew trước
brew install portaudio
pip install pyaudio
```

---

### 4️⃣ Tải Whisper Models (Faster-Whisper)

Models sẽ tự động download lúc chạy lần đầu, hoặc tải sẵn:

```bash
# Models sẽ lưu ở: ~/.cache/huggingface/hub/

# Bạn có thể tải trước (tùy chọn):
python3 -c "from faster_whisper import WhisperModel; WhisperModel('tiny.en')"
python3 -c "from faster_whisper import WhisperModel; WhisperModel('medium')"
```

---

### 5️⃣ Tải Kokoro TTS Voices

#### A. Tạo thư mục cho Kokoro models
```bash
mkdir -p ~/ComfyUI/models/Kokorotts/Kokoro-82M/voices
```

#### B. Download English voices từ Hugging Face
```bash
cd voice-chat-ai
chmod +x ./kokoro-tts-server/download_english_voices.sh
./kokoro-tts-server/download_english_voices.sh
```

#### C. (Tùy chọn) Download Japanese & Other Language Voices
```bash
# Từ: https://huggingface.co/hexgrad/Kokoro-82M/tree/main/voices
# Tải các file .pt cho ngôn ngữ khác vào:
# ~/ComfyUI/models/Kokorotts/Kokoro-82M/voices/
```

---

### 6️⃣ Cấu hình Environment Variables

Tạo file `.env` trong thư mục project:

```bash
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
```

---

### 7️⃣ Cài đặt & Chạy Ollama (LLM Model)

```bash
# Download Ollama từ: https://ollama.ai/
# Hoặc cài bằng Homebrew:
brew install ollama

# Pull một model (ví dụ: qwen2:7b)
ollama pull qwen2:7b

# Chạy Ollama server (trong terminal riêng)
ollama serve
```

---

### 8️⃣ Chạy Application

#### Terminal 1: Ollama (nếu chưa chạy)
```bash
ollama serve
```

#### Terminal 2: Kokoro TTS Server
```bash
cd voice-chat-ai
source venv/bin/activate
/path/to/python kokoro-tts-server/server.py
```

Hoặc nếu dùng ComfyUI Python:
```bash
~/ComfyUI/.venv/bin/python kokoro-tts-server/server.py
```

#### Terminal 3: Voice Chat AI App
```bash
cd voice-chat-ai
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Hoặc cùng lúc:**
```bash
cd voice-chat-ai
chmod +x start_server.sh
./start_server.sh
```

---

### 9️⃣ Truy cập Application

Mở browser và truy cập:
- **Web UI**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🛠️ Troubleshooting

### ❌ "ModuleNotFoundError: No module named 'kokoro'"
```bash
# Cài đặt kokoro
pip install git+https://github.com/hexgrad/kokoro.git
```

### ❌ "pyaudio" installation error
```bash
# macOS specific fix
brew install portaudio
pip install --no-cache-dir pyaudio
```

### ❌ "torch" issues on Apple Silicon
```bash
# For M1/M2/M3 Macs:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### ❌ Port already in use
```bash
# Tìm process dùng port 8000
lsof -i :8000

# Kill process (replace PID)
kill -9 <PID>
```

### ❌ Kokoro server not found
```bash
# Kiểm tra voices
ls -la ~/ComfyUI/models/Kokorotts/Kokoro-82M/voices/

# Tải lại voices
./kokoro-tts-server/download_english_voices.sh
```

---

## 📊 Performance Tips

### Giảm CPU Usage
Sửa trong `app/transcription.py`:
```python
model_size = "tiny.en"  # Thay vì "medium.en"
```

### Giảm Memory Usage
```bash
# Sử dụng quantized models
pip install bitsandbytes
```

### Apple Silicon Optimization
Đã được optimize tự động. Để kiểm tra:
```python
import torch
print(torch.backends.mps.is_available())  # True = tối ưu hóa MPS
```

---

## 📦 Quick Install Script (Optional)

Nếu muốn, tạo file `install_mac.sh`:

```bash
#!/bin/bash
set -e

echo "🚀 Installing Voice Chat AI on macOS..."

# Check Python
python3 --version || { echo "❌ Python 3.10+ required"; exit 1; }

# Create venv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Setup directories
mkdir -p ~/ComfyUI/models/Kokorotts/Kokoro-82M/voices

# Download voices
chmod +x ./kokoro-tts-server/download_english_voices.sh
./kokoro-tts-server/download_english_voices.sh

echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Set up .env file with your configuration"
echo "2. Start Ollama: ollama serve"
echo "3. Run: ./start_server.sh"
```

Chạy:
```bash
chmod +x install_mac.sh
./install_mac.sh
```

---

## 🎯 Supported Models

### LLM Models (Ollama)
- `qwen2:7b` ⭐ Recommended (fast, good quality)
- `qwen2:latest` (larger, better quality)
- `mistral:latest`
- `neural-chat:latest`

### TTS Voices
- **American English**: af_nova, af_bella, am_adam, am_echo
- **British English**: bf_emma, bf_alice, bm_daniel, bm_fable
- **Japanese**: jf_alpha, jf_gongitsune, jm_kumo (+ more)
- **Other**: Spanish, French, Hindi, Portuguese, Chinese

---

## 📝 Environment Variables Reference

```bash
LANGUAGE_CODE          # en, ja, es, fr, de, hi, it, ko, pl, ru, zh
CHARACTER_NAME         # Character folder name
MODEL_PROVIDER         # ollama, openai, anthropic, xai
OLLAMA_MODEL          # Model name for Ollama
TTS_PROVIDER          # Kokoro-TTS, OpenAI, ElevenLabs
FASTER_WHISPER_LOCAL  # true/false
```

---

## ✅ Testing

```bash
# Test Ollama
curl http://localhost:11434/api/generate -d '{"model":"qwen2:7b","prompt":"Hello"}'

# Test TTS Server
curl http://localhost:8880/

# Test Web UI
open http://localhost:8000
```

---

## 📞 Support

Gặp vấn đề? Kiểm tra:
1. Logs từ mỗi terminal
2. Network connections (ports 8000, 8880, 11434)
3. Model downloads (disk space)
4. Python version compatibility

---

**Happy Voice Chatting! 🎉**
