#!/usr/bin/env python3
"""
Interactive TTS Synthesis for MacBook
Generate speech from custom text input
"""

import os
import sys
import time
from pathlib import Path

try:
    from TTS.utils.synthesizer import Synthesizer
except ImportError:
    print("❌ TTS not found. Please install: pip install TTS>=0.13.0")
    sys.exit(1)

class TTSSynthesizer:
    def __init__(self, model_path="models/best_model.pth", config_path="models/config.json"):
        self.model_path = model_path
        self.config_path = config_path
        self.synthesizer = None
        
    def load_model(self):
        """Load the TTS model"""
        print("🚀 Loading TTS model...")
        start_time = time.time()
        
        try:
            self.synthesizer = Synthesizer(
                model_path=self.model_path,
                config_path=self.config_path,
                use_cuda=False
            )
            load_time = time.time() - start_time
            print(f"✅ Model loaded in {load_time:.2f} seconds")
            return True
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def synthesize(self, text, output_file=None):
        """Synthesize text to speech"""
        if not self.synthesizer:
            print("❌ Model not loaded. Call load_model() first.")
            return False
        
        if not output_file:
            # Generate filename from text
            safe_text = "".join(c for c in text[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            output_file = f"output_{safe_text.replace(' ', '_')}.wav"
        
        print(f"\n🎵 Synthesizing: {text}")
        
        try:
            start_time = time.time()
            outputs = self.synthesizer.tts(text)
            synthesis_time = time.time() - start_time
            
            # Save audio
            self.synthesizer.save_wav(outputs["wav"], output_file)
            
            # Statistics
            audio_length = len(outputs["wav"]) / self.synthesizer.output_sample_rate
            rtf = synthesis_time / audio_length  # Real-time factor
            
            print(f"✅ Generated in {synthesis_time:.2f} seconds")
            print(f"💾 Saved: {output_file}")
            print(f"🎵 Audio length: {audio_length:.2f} seconds")
            print(f"⚡ Real-time factor: {rtf:.2f}x")
            
            return True
            
        except Exception as e:
            print(f"❌ Synthesis error: {e}")
            return False

def main():
    print("🍎 TTS Synthesizer - MacBook Air")
    print("=" * 40)
    
    # Initialize synthesizer
    tts = TTSSynthesizer()
    
    if not tts.load_model():
        return 1
    
    print("\n💡 Ready for synthesis!")
    print("Enter text to synthesize (or 'quit' to exit)")
    print("-" * 40)
    
    while True:
        try:
            text = input("\n📝 Enter text: ").strip()
            
            if text.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not text:
                print("Please enter some text.")
                continue
            
            # Synthesize
            tts.synthesize(text)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())