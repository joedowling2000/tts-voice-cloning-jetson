#!/usr/bin/env python3
"""
Fix metadata format for LJSpeech compatibility
"""

import re

def clean_and_normalize_text(text):
    """Clean and normalize text for TTS"""
    # Basic text cleaning
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def main():
    input_file = "/ssd/tts_project/voice_data/metadata.csv"
    output_file = "/ssd/tts_project/voice_data/metadata_ljspeech.csv"
    
    print("🔧 Converting metadata to LJSpeech format...")
    
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            line = line.strip()
            if '|' in line:
                filename, text = line.split('|', 1)
                # Remove .wav extension for LJSpeech format
                file_id = filename.replace('.wav', '')
                
                # Clean the text
                cleaned_text = clean_and_normalize_text(text)
                
                # LJSpeech format: file_id|original_text|normalized_text
                f_out.write(f"{file_id}|{cleaned_text}|{cleaned_text}\n")
    
    print(f"✅ Converted metadata saved to: {output_file}")
    
    # Show sample
    print("\n📄 Sample converted format:")
    with open(output_file, 'r') as f:
        for i, line in enumerate(f):
            if i < 3:
                print(f"   {line.strip()}")
            else:
                break

if __name__ == "__main__":
    main()