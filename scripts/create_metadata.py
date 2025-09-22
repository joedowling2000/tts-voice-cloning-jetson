#!/usr/bin/env python3
"""
Create metadata.csv from training.json and audio files
"""

import json
import os
from pathlib import Path

def create_metadata_from_json():
    """
    Extract transcripts from training.json and match with audio files
    """
    print("📝 Creating metadata file from training.json...")
    
    # Paths
    project_root = Path("/ssd/tts_project")
    json_file = project_root / "training.json"
    audio_dir = project_root / "voice_data" / "raw_audio"
    output_file = project_root / "voice_data" / "metadata.csv"
    
    # Load JSON file
    with open(json_file, 'r', encoding='utf-8') as f:
        training_data = json.load(f)
    
    # Extract training_data array
    entries = training_data['training_data']
    print(f"📝 Found {len(entries)} entries in training.json")
    
    # Get audio files that exist
    audio_files = sorted(list(audio_dir.glob("*.wav")))
    print(f"📁 Found {len(audio_files)} audio files")
    
    # Create a mapping of filename to transcript for the first 80 entries
    filename_to_text = {}
    for entry in entries[:80]:  # Only first 80 since that's what was recorded
        filename_to_text[entry['filename']] = entry['text']
    
    print(f"📝 Created mapping for {len(filename_to_text)} transcripts")
    
    # Create metadata.csv
    matched_count = 0
    with open(output_file, 'w', encoding='utf-8') as f:
        for audio_file in audio_files:
            filename = audio_file.name
            if filename in filename_to_text:
                transcript = filename_to_text[filename]
                # Clean up transcript
                transcript = transcript.replace('\n', ' ').replace('\r', ' ')
                transcript = ' '.join(transcript.split())  # Remove extra spaces
                
                f.write(f"{filename}|{transcript}\n")
                matched_count += 1
            else:
                print(f"⚠️  No transcript found for {filename}")
    
    print(f"✅ Created metadata.csv with {matched_count} entries")
    print(f"📁 Saved to: {output_file}")
    
    # Show first few entries
    print("\n📋 First 5 entries:")
    with open(output_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i < 5:
                filename, transcript = line.strip().split('|', 1)
                print(f"  {filename}: {transcript[:60]}...")
    
    return True

if __name__ == "__main__":
    create_metadata_from_json()