#!/usr/bin/env python3
"""
TTS Model Testing Script for MacBook
Tests model loading and basic functionality
"""

import os
import sys
import torch
import time
import json
from pathlib import Path

# Add TTS to path if needed
try:
    from TTS.utils.synthesizer import Synthesizer
    from TTS.config import load_config
except ImportError:
    print("❌ TTS not found. Please install: pip install TTS>=0.13.0")
    sys.exit(1)

def test_model():
    """Test the TTS model functionality"""
    
    print("🍎 TTS Model Test - MacBook Air")
    print("=" * 50)
    
    # Paths
    model_path = "models/best_model.pth"
    config_path = "models/config.json"
    
    # Check files exist
    if not os.path.exists(model_path):
        print(f"❌ Model not found: {model_path}")
        return False
        
    if not os.path.exists(config_path):
        print(f"❌ Config not found: {config_path}")
        return False
    
    print("✅ Files found")
    print(f"📁 Model: {model_path}")
    print(f"📋 Config: {config_path}")
    
    # Load configuration
    print("\n🔧 Loading configuration...")
    try:
        config = load_config(config_path)
        print(f"✅ Config loaded - Model: {config.model}")
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False
    
    # Initialize synthesizer
    print("\n🚀 Loading model...")
    start_time = time.time()
    
    try:
        synthesizer = Synthesizer(
            model_path=model_path,
            config_path=config_path,
            use_cuda=False  # Use CPU on MacBook
        )
        load_time = time.time() - start_time
        print(f"✅ Model loaded in {load_time:.2f} seconds")
    except Exception as e:
        print(f"❌ Model loading error: {e}")
        return False
    
    # Test synthesis
    print("\n🎵 Testing synthesis...")
    test_texts = [
        "Hello, this is a test of the voice synthesis system.",
        "The MacBook Air provides excellent performance for inference.",
        "How does this voice sound compared to the original?"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Test {i}: {text}")
        
        try:
            start_time = time.time()
            outputs = synthesizer.tts(text)
            synthesis_time = time.time() - start_time
            
            # Save audio file
            output_file = f"test_output_{i}.wav"
            synthesizer.save_wav(outputs["wav"], output_file)
            
            print(f"✅ Generated in {synthesis_time:.2f} seconds")
            print(f"💾 Saved: {output_file}")
            
            # Audio info
            audio_length = len(outputs["wav"]) / synthesizer.output_sample_rate
            print(f"🎵 Audio length: {audio_length:.2f} seconds")
            print(f"📊 Sample rate: {synthesizer.output_sample_rate} Hz")
            
        except Exception as e:
            print(f"❌ Synthesis error: {e}")
            return False
    
    print("\n🎉 All tests completed successfully!")
    print("\n💡 Next steps:")
    print("1. Listen to the generated audio files")
    print("2. Compare quality with original training data")
    print("3. Use synthesize_text_mac.py for custom text")
    
    return True

if __name__ == "__main__":
    success = test_model()
    sys.exit(0 if success else 1)