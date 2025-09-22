#!/usr/bin/env python3
"""
Process raw audio files for TTS training
"""

import librosa
import soundfile as sf
import numpy as np
from pathlib import Path
import os

def process_audio_files():
    """
    Process raw audio files:
    - Normalize volume
    - Resample to 22050 Hz
    - Remove silence
    - Save to processed_audio folder
    """
    print("🎵 Processing Audio Files for TTS Training")
    print("=" * 50)
    
    # Paths
    project_root = Path("/ssd/tts_project")
    raw_audio_dir = project_root / "voice_data" / "raw_audio"
    processed_audio_dir = project_root / "voice_data" / "processed_audio"
    
    # Create processed audio directory
    processed_audio_dir.mkdir(exist_ok=True)
    
    # Get all wav files
    audio_files = sorted(list(raw_audio_dir.glob("*.wav")))
    print(f"📁 Found {len(audio_files)} audio files to process")
    
    target_sample_rate = 22050  # Standard for TTS
    
    total_duration = 0
    
    for i, audio_file in enumerate(audio_files):
        print(f"🎧 Processing {i+1}/{len(audio_files)}: {audio_file.name}")
        
        try:
            # Load audio
            audio, original_sr = librosa.load(audio_file, sr=None)
            
            # Resample to target sample rate
            if original_sr != target_sample_rate:
                audio = librosa.resample(audio, orig_sr=original_sr, target_sr=target_sample_rate)
            
            # Trim silence from beginning and end
            audio, _ = librosa.effects.trim(audio, top_db=20)
            
            # Normalize audio to -3dB peak
            peak = np.abs(audio).max()
            if peak > 0:
                audio = audio * (0.707 / peak)  # -3dB normalization
            
            # Save processed audio
            output_file = processed_audio_dir / audio_file.name
            sf.write(output_file, audio, target_sample_rate, subtype='PCM_16')
            
            # Show info
            duration = len(audio) / target_sample_rate
            total_duration += duration
            print(f"   ✅ Duration: {duration:.2f}s, Sample Rate: {target_sample_rate}Hz")
            
        except Exception as e:
            print(f"   ❌ Error processing {audio_file.name}: {e}")
    
    print(f"\n🎉 Audio processing complete!")
    print(f"📁 Processed files saved to: {processed_audio_dir}")
    print(f"⏱️  Total audio duration: {total_duration/60:.1f} minutes")
    print(f"📊 Average file duration: {total_duration/len(audio_files):.1f} seconds")

if __name__ == "__main__":
    process_audio_files()