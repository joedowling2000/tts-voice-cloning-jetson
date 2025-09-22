#!/usr/bin/env python3
"""
Simple Hello World Generator for Henry's Voice
"""

import os
import sys

def generate_hello_world_simple():
    """Generate Hello World with error handling"""
    
    print("🎤 GENERATING HELLO WORLD - HENRY'S VOICE")
    print("=" * 45)
    
    try:
        # Import TTS in a try block
        from TTS.utils.synthesizer import Synthesizer
        
        # Model paths
        model_dir = "/ssd/tts_project/arm_max_quality_output/henry_voice_arm_max_quality-September-21-2025_09+38PM-0000000"
        model_path = f"{model_dir}/best_model.pth"
        config_path = f"{model_dir}/config.json"
        
        print(f"📂 Model directory: {os.path.basename(model_dir)}")
        
        # Check files exist
        if not os.path.exists(model_path):
            print(f"❌ Model not found: {model_path}")
            return False
            
        if not os.path.exists(config_path):
            print(f"❌ Config not found: {config_path}")
            return False
            
        print("✅ Model and config files found")
        
        # Create output directory
        output_dir = "/ssd/tts_project/hello_world_output"
        os.makedirs(output_dir, exist_ok=True)
        output_file = f"{output_dir}/hello_world_henry.wav"
        
        print("🔧 Loading synthesizer...")
        synthesizer = Synthesizer(
            tts_checkpoint=model_path,
            tts_config_path=config_path,
            use_cuda=False
        )
        
        print("✅ Synthesizer loaded successfully")
        
        # Text to generate
        text = "Hello World, this is Henry Dowling speaking, coming to you from the AI realm"
        print(f"📝 Text: {text}")
        
        print("🎵 Generating speech (this may take a few minutes on Jetson Nano)...")
        
        # Generate the audio
        wav = synthesizer.tts(text)
        print("✅ Audio generated successfully")
        
        print("💾 Saving audio file...")
        synthesizer.save_wav(wav, output_file)
        
        # Check if file was created and get size
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"✅ SUCCESS! File saved: {output_file}")
            print(f"📊 File size: {file_size:,} bytes")
            
            # Show full path
            abs_path = os.path.abspath(output_file)
            print(f"📍 Full path: {abs_path}")
            
            print("\n🎉 HELLO WORLD GENERATION COMPLETE!")
            print("🎧 You can now play the hello_world_henry.wav file")
            return True
        else:
            print("❌ File was not created successfully")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this in the tts_arm_env environment")
        return False
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = generate_hello_world_simple()
    if success:
        print("\n✅ Hello World generation successful!")
    else:
        print("\n💥 Hello World generation failed!")
        sys.exit(1)