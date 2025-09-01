# 🎯 Transcription GOAT - Universal Audio/Video Transcriber

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Whisper](https://img.shields.io/badge/Whisper-OpenAI-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**The ultimate offline transcription tool that handles ANY media format with perfect timestamps and intelligent duplicate detection.**

## ✨ Features

- 🎬 **Universal Format Support**: MP3, MP4, WAV, M4A, OPUS, OGG, FLAC, AVI, MOV, MKV, WEBM, and 15+ more formats
- 🎯 **High Accuracy**: Uses OpenAI's Whisper medium model for exceptional transcription quality
- ⏱️ **Precise Timestamps**: Every segment includes start and end timestamps
- 🌍 **Multi-Language**: Auto-detects and transcribes in any language
- 🔄 **Smart Duplicate Detection**: Never transcribes the same file twice (uses file hashing)
- 📊 **Batch Processing**: Drop multiple files and transcribe them all at once
- 💻 **100% Offline**: No internet required, your data stays private
- 📝 **Beautiful Output**: Well-formatted transcripts with metadata and timestamps

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- macOS, Linux, or Windows
- 8GB RAM recommended for medium model

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/pavangupta352/Transcription-GOAT.git
cd Transcription-GOAT
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Install FFmpeg** (if not already installed)

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## 📖 Usage

1. **Add your media files** to the `Input/` folder
   - Supports single or multiple files
   - Mix different formats (mp3, mp4, opus, etc.)

2. **Run the script**
```bash
python3 main.py
```

3. **Find your transcripts** in `Output/transcripts/`
   - Each file gets its own transcript with timestamps
   - Files are named: `[original_name]_transcript.txt`

## 📁 Project Structure

```
Transcription-GOAT/
├── main.py                 # Main script
├── requirements.txt        # Python dependencies
├── Input/                  # Place your media files here
├── Output/                 # Transcripts appear here
│   ├── transcripts/        # All transcript files
│   └── transcription_history.json  # Tracks processed files
└── README.md
```

## 🎥 Supported Formats

| Audio Formats | Video Formats |
|--------------|---------------|
| MP3, M4A | MP4, AVI |
| WAV, FLAC | MOV, MKV |
| OGG, OPUS | WEBM, WMV |
| AAC, WMA | MPG, FLV |
| M4B | 3GP |

## 📋 Sample Output

```
════════════════════════════════════════════════════════════════════════════════
TRANSCRIPT: interview.mp4
Date: 2025-09-01 08:01:16
Language: EN
════════════════════════════════════════════════════════════════════════════════

[00:00.000 → 00:05.919]
Welcome to today's interview. Let's discuss the future of AI.

[00:05.919 → 00:16.559]
Artificial intelligence is transforming how we work and live...

[00:16.559 → 00:23.920]
The key challenges we face include privacy, ethics, and accessibility.

--------------------------------------------------------------------------------
FULL TEXT (WITHOUT TIMESTAMPS):
--------------------------------------------------------------------------------
Welcome to today's interview. Let's discuss the future of AI. Artificial 
intelligence is transforming how we work and live. The key challenges we 
face include privacy, ethics, and accessibility...
```

## ⚙️ Configuration

### Change Whisper Model Size

Edit `main.py` line 14:
```python
MODEL_NAME = "medium"  # Options: tiny, base, small, medium, large
```

**Model Comparison:**
- `tiny`: Fastest, least accurate (39M parameters)
- `base`: Fast, good for English (74M)
- `small`: Balanced speed/accuracy (244M)
- `medium`: Best balance (769M) **[DEFAULT]**
- `large`: Most accurate, slowest (1550M)

## 🔍 How It Works

1. **File Detection**: Scans the Input folder for supported media files
2. **Duplicate Check**: Uses MD5 hashing to skip already-processed files
3. **Transcription**: Whisper model processes audio with automatic language detection
4. **Formatting**: Adds timestamps and organizes text into readable segments
5. **Output**: Saves formatted transcript with metadata to Output folder

## 🐛 Troubleshooting

### "No module named 'whisper'"
```bash
pip install --upgrade openai-whisper
```

### "ffmpeg: command not found"
Install FFmpeg using the instructions above for your OS

### Out of Memory Error
Try using a smaller model:
```python
MODEL_NAME = "small"  # or "base" or "tiny"
```

### macOS "Externally Managed Environment" Error
```bash
pip install --break-system-packages -r requirements.txt
# OR use a virtual environment:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🚀 Advanced Features

### Transcription History
- Located at `Output/transcription_history.json`
- Tracks all processed files with hash, date, language, and duration
- Delete entries to re-transcribe specific files

### Batch Processing Tips
- Process hundreds of files at once
- Mix different formats freely
- Progress shown for each file
- Summary statistics at the end

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

MIT License - feel free to use this in your own projects!

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for the amazing transcription model
- FFmpeg for media processing

## 💬 Support

Having issues? [Open an issue](https://github.com/pavangupta352/Transcription-GOAT/issues)

---

**Made with ❤️ for the transcription community**

*Star ⭐ this repo if you find it useful!*