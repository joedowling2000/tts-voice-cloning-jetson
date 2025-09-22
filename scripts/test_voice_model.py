#!/usr/bin/env python3
"""
Quick Test of Trained Henry Voice Model
Generate sample speech to test quality
"""

import os
import sys
from datetime import datetime

# Add the project root to Python path
sys.path.append('/ssd/tts_project')

def test_trained_model():
    """Test the trained Henry voice model"""
    
    print("🎤 TESTING TRAINED HENRY VOICE MODEL")
    print("=" * 50)
    
    # Model paths
    model_path = "/ssd/tts_project/arm_max_quality_output/henry_voice_arm_max_quality-September-21-2025_09+38PM-0000000/best_model.pth"
    config_path = "/ssd/tts_project/arm_max_quality_output/henry_voice_arm_max_quality-September-21-2025_09+38PM-0000000/config.json"
    
    # Check if files exist
    if not os.path.exists(model_path):
        print(f"❌ Model file not found: {model_path}")
        return False
        
    if not os.path.exists(config_path):
        print(f"❌ Config file not found: {config_path}")
        return False
    
    print(f"✅ Model file found: {os.path.basename(model_path)}")
    print(f"✅ Config file found: {os.path.basename(config_path)}")
    print(f"📊 Model size: {os.path.getsize(model_path) / (1024*1024):.1f} MB")
    
    # Test sentences
    test_sentences = [
        "Hello, this is Henry speaking with the new high-quality voice model.",
        "The training was successful and now I can generate speech.",
        "Science and technology continue to advance at an incredible pace.",
        "Thank you for helping me create this custom voice model."
    ]
    
    try:
        # Import TTS
        print("\n🔧 Loading TTS library...")
        from TTS.api import TTS
        
        # Initialize TTS with trained model
        print("🔧 Loading trained model...")
        tts = TTS(model_path=model_path, config_path=config_path)
        print("✅ Model loaded successfully!")
        
        # Create output directory
        output_dir = "/ssd/tts_project/test_outputs"
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\n🎵 GENERATING SPEECH SAMPLES")
        print(f"Output directory: {output_dir}")
        print("-" * 40)
        
        # Generate speech for each test sentence
        for i, text in enumerate(test_sentences, 1):
            output_file = f"{output_dir}/henry_sample_{i}.wav"
            
            print(f"\n📝 Sample {i}: {text[:50]}...")
            print(f"🎵 Generating: {os.path.basename(output_file)}")
            
            # Generate speech
            tts.tts_to_file(text=text, file_path=output_file)
            
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                print(f"✅ Generated: {file_size:,} bytes")
            else:
                print(f"❌ Failed to generate audio file")
        
        print(f"\n🎉 SUCCESS! Generated {len(test_sentences)} speech samples")
        print(f"📁 Output location: {output_dir}")
        print(f"🎧 You can now listen to the generated Henry voice samples!")
        
        # List generated files
        print(f"\n📋 Generated Files:")
        if os.path.exists(output_dir):
            for file in sorted(os.listdir(output_dir)):
                if file.endswith('.wav'):
                    file_path = os.path.join(output_dir, file)
                    size = os.path.getsize(file_path)
                    print(f"   🎵 {file} ({size:,} bytes)")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're using the ARM TTS environment:")
        print("   source /ssd/tts_project/tts_arm_env/bin/activate")
        return False
        
    except Exception as e:
        print(f"❌ Error during model testing: {e}")
        print(f"🔍 Error type: {type(e).__name__}")
        return False

def main():
    success = test_trained_model()
    
    if success:
        print(f"\n🎊 MODEL TEST COMPLETED SUCCESSFULLY!")
        print(f"🎤 Your Henry voice model is working and ready to use!")
    else:
        print(f"\n💥 Model test failed. Check the errors above.")
        
if __name__ == "__main__":
    main()