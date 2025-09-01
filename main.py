#!/usr/bin/env python3
"""
Audio/Video Transcription Script using Whisper
Transcribes all media files in Input folder and saves to Output folder
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
import whisper
import warnings
warnings.filterwarnings("ignore")

# Configuration
INPUT_DIR = Path("Input")
OUTPUT_DIR = Path("Output")
TRANSCRIPTS_DIR = OUTPUT_DIR / "transcripts"
METADATA_FILE = OUTPUT_DIR / "transcription_history.json"
MODEL_NAME = "medium"

# Supported file extensions
SUPPORTED_FORMATS = {
    '.mp3', '.mp4', '.wav', '.m4a', '.opus', '.ogg', '.flac', 
    '.avi', '.mov', '.mkv', '.webm', '.aac', '.wma', '.m4b',
    '.3gp', '.mpeg', '.mpg', '.wmv', '.flv'
}

def setup_directories():
    """Create necessary directories if they don't exist."""
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    TRANSCRIPTS_DIR.mkdir(exist_ok=True)
    print(f"✓ Directories ready: {INPUT_DIR}/, {OUTPUT_DIR}/")

def load_history():
    """Load transcription history from metadata file."""
    if METADATA_FILE.exists():
        with open(METADATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_history(history):
    """Save transcription history to metadata file."""
    with open(METADATA_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def get_file_hash(filepath):
    """Generate hash of file for duplicate detection."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def format_timestamp(seconds):
    """Convert seconds to readable timestamp format."""
    td = timedelta(seconds=seconds)
    hours = int(td.total_seconds() // 3600)
    minutes = int((td.total_seconds() % 3600) // 60)
    seconds = int(td.total_seconds() % 60)
    milliseconds = int((td.total_seconds() % 1) * 1000)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    else:
        return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

def transcribe_file(filepath, model):
    """Transcribe a single file using Whisper."""
    print(f"  🎤 Transcribing: {filepath.name}")
    
    try:
        # Transcribe with Whisper
        result = model.transcribe(
            str(filepath),
            language=None,  # Auto-detect language
            verbose=False,
            fp16=False  # Disable FP16 for better compatibility
        )
        
        # Format transcript with timestamps
        transcript_lines = []
        
        # Add header
        transcript_lines.append(f"═" * 80)
        transcript_lines.append(f"TRANSCRIPT: {filepath.name}")
        transcript_lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        transcript_lines.append(f"Language: {result.get('language', 'unknown').upper()}")
        transcript_lines.append(f"═" * 80)
        transcript_lines.append("")
        
        # Add segments with timestamps
        for segment in result['segments']:
            start_time = format_timestamp(segment['start'])
            end_time = format_timestamp(segment['end'])
            text = segment['text'].strip()
            
            transcript_lines.append(f"[{start_time} → {end_time}]")
            transcript_lines.append(f"{text}")
            transcript_lines.append("")
        
        # Add full text section
        transcript_lines.append("-" * 80)
        transcript_lines.append("FULL TEXT (WITHOUT TIMESTAMPS):")
        transcript_lines.append("-" * 80)
        transcript_lines.append(result['text'].strip())
        
        return "\n".join(transcript_lines), result
        
    except Exception as e:
        print(f"  ❌ Error transcribing {filepath.name}: {str(e)}")
        return None, None

def process_files(model):
    """Process all files in the Input directory."""
    history = load_history()
    
    # Get all files in Input directory
    files = [f for f in INPUT_DIR.iterdir() if f.is_file() and f.suffix.lower() in SUPPORTED_FORMATS]
    
    if not files:
        print("⚠️  No supported media files found in Input folder")
        print(f"   Supported formats: {', '.join(sorted(SUPPORTED_FORMATS))}")
        return
    
    print(f"\n📁 Found {len(files)} file(s) to process")
    print("-" * 50)
    
    processed_count = 0
    skipped_count = 0
    
    for i, filepath in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] Processing: {filepath.name}")
        
        # Check if already transcribed
        file_hash = get_file_hash(filepath)
        if file_hash in history:
            print(f"  ⏭️  Skipping (already transcribed on {history[file_hash]['date']})")
            skipped_count += 1
            continue
        
        # Transcribe the file
        transcript, result = transcribe_file(filepath, model)
        
        if transcript:
            # Save transcript to file
            safe_filename = "".join(c for c in filepath.stem if c.isalnum() or c in (' ', '-', '_')).rstrip()
            output_file = TRANSCRIPTS_DIR / f"{safe_filename}_transcript.txt"
            
            # Handle duplicate output filenames
            counter = 1
            while output_file.exists():
                output_file = TRANSCRIPTS_DIR / f"{safe_filename}_transcript_{counter}.txt"
                counter += 1
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(transcript)
            
            # Update history
            history[file_hash] = {
                'filename': filepath.name,
                'date': datetime.now().isoformat(),
                'output_file': str(output_file.relative_to(OUTPUT_DIR)),
                'language': result.get('language', 'unknown'),
                'duration': result.get('duration', 0)
            }
            save_history(history)
            
            print(f"  ✅ Saved to: {output_file.relative_to(Path.cwd())}")
            processed_count += 1
        else:
            print(f"  ❌ Failed to transcribe")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print(f"  • Processed: {processed_count} file(s)")
    print(f"  • Skipped: {skipped_count} file(s)")
    print(f"  • Total: {len(files)} file(s)")
    print("=" * 50)

def main():
    """Main execution function."""
    print("🎯 Audio/Video Transcription Tool")
    print("=" * 50)
    
    # Setup
    setup_directories()
    
    # Check for input files
    if not any(INPUT_DIR.iterdir()):
        print("\n⚠️  Input folder is empty!")
        print(f"   Please add media files to: {INPUT_DIR.absolute()}")
        print(f"   Supported formats: {', '.join(sorted(SUPPORTED_FORMATS))}")
        return
    
    # Load Whisper model
    print(f"\n📥 Loading Whisper model: {MODEL_NAME}")
    print("   (This may take a moment on first run...)")
    
    try:
        model = whisper.load_model(MODEL_NAME)
        print(f"✓ Model loaded successfully")
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        print("\nTip: Make sure you have whisper installed:")
        print("  pip install openai-whisper")
        return
    
    # Process files
    process_files(model)
    
    print(f"\n✨ Done! Check the {OUTPUT_DIR}/ folder for transcripts.")

if __name__ == "__main__":
    main()