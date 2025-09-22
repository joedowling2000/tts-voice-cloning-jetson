#!/usr/bin/env python3
"""
Fixed Hello World Generator with Stopnet Override
"""

import os
import sys
import numpy as np

def generate_hello_world_fixed():
    """Generate Hello World with manual stopnet control"""
    
    print("🎤 GENERATING HELLO WORLD - FIXED VERSION")
    print("=" * 45)
    
    try:
        from TTS.utils.synthesizer import Synthesizer
        from TTS.tts.configs.tacotron2_config import Tacotron2Config
        
        # Model paths
        model_dir = "/ssd/tts_project/arm_max_quality_output/voice_model_arm_max_quality-September-21-2025_09+38PM-0000000"
        model_path = f"{model_dir}/best_model.pth"
        config_path = f"{model_dir}/config.json"
        
        print(f"📂 Model directory: {os.path.basename(model_dir)}")
        
        # Load config and modify max_decoder_steps
        print("🔧 Loading and modifying config...")
        config = Tacotron2Config()
        config.load_json(config_path)
        
        # Reduce max_decoder_steps for shorter texts
        original_max_steps = config.max_decoder_steps
        config.max_decoder_steps = 2000  # Much lower limit
        
        print(f"   Original max_decoder_steps: {original_max_steps}")
        print(f"   New max_decoder_steps: {config.max_decoder_steps}")
        
        # Create output directory
        output_dir = "/ssd/tts_project/hello_world_output"
        os.makedirs(output_dir, exist_ok=True)
        
        print("🔧 Loading synthesizer with modified config...")
        synthesizer = Synthesizer(
            tts_checkpoint=model_path,
            tts_config_path=config_path,
            use_cuda=False
        )
        
        # Override the config after loading
        synthesizer.tts_model.config.max_decoder_steps = 2000
        
        print("✅ Synthesizer loaded with reduced max_decoder_steps")
        
        # Test with different texts and lengths
        test_cases = [
            ("Hello World", "hello_fixed_short.wav"),
            ("Hello World, this is Henry", "hello_fixed_medium.wav"),
            ("Hello World, this is the trained speaker speaking", "hello_fixed_long.wav"),
            ("Hello World, this is the trained speaker speaking, coming to you from the AI realm", "hello_fixed_full.wav")
        ]
        
        for text, filename in test_cases:
            print(f"\n📝 Testing: {text}")
            output_file = f"{output_dir}/{filename}"
            
            try:
                wav = synthesizer.tts(text)
                synthesizer.save_wav(wav, output_file)
                
                if os.path.exists(output_file):
                    file_size = os.path.getsize(output_file)
                    duration = len(wav) / 22050  # Sample rate is 22050
                    print(f"   ✅ Generated: {filename}")
                    print(f"   📊 Size: {file_size:,} bytes")
                    print(f"   ⏱️  Duration: {duration:.2f} seconds")
                else:
                    print(f"   ❌ Failed to create {filename}")
                    
            except Exception as e:
                print(f"   ❌ Error generating {filename}: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = generate_hello_world_fixed()
    if success:
        print("\n✅ Fixed Hello World generation completed!")
    else:
        print("\n💥 Fixed Hello World generation failed!")
        sys.exit(1)