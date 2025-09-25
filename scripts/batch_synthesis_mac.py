#!/usr/bin/env python3
"""
Batch synthesis script for multiple texts
"""

import os
import sys
from pathlib import Path

try:
    from TTS.utils.synthesizer import Synthesizer
except ImportError:
    print("❌ TTS not found. Please install: pip install TTS>=0.13.0")
    sys.exit(1)

def batch_synthesize(text_file="sample_texts.txt", output_dir="batch_output"):
    """Process multiple texts from a file"""
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Load model
    print("🚀 Loading model...")
    synthesizer = Synthesizer(
        model_path="models/best_model.pth",
        config_path="models/config.json",
        use_cuda=False
    )
    
    # Read texts
    if not os.path.exists(text_file):
        print(f"❌ Text file not found: {text_file}")
        return False
    
    with open(text_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print(f"📝 Processing {len(lines)} texts...")
    
    # Process each text
    for i, text in enumerate(lines, 1):
        print(f"\n🎵 {i}/{len(lines)}: {text[:50]}...")
        
        try:
            outputs = synthesizer.tts(text)
            output_file = os.path.join(output_dir, f"sample_{i:03d}.wav")
            synthesizer.save_wav(outputs["wav"], output_file)
            print(f"✅ Saved: {output_file}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n🎉 Batch processing complete! Check {output_dir}/ folder")
    return True

if __name__ == "__main__":
    batch_synthesize()