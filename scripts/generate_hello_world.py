#!/usr/bin/env python3
"""
Generate Hello World message with the custom voice
"""

import os
import sys
from datetime import datetime

# Add the project root to Python path
sys.path.append('/ssd/tts_project')

def generate_hello_world():
    """Generate the Hello World message using the custom voice"""
    
    print("🎤 GENERATING HELLO WORLD WITH HENRY'S VOICE")
    print("=" * 50)
    
    # Model paths (using the successfully trained model)
    model_path = "/ssd/tts_project/arm_max_quality_output/voice_model_arm_max_quality-September-21-2025_09+38PM-0000000/best_model.pth"
    config_path = "/ssd/tts_project/arm_max_quality_output/voice_model_arm_max_quality-September-21-2025_09+38PM-0000000/config.json"
    
    # Check if files exist
    if not os.path.exists(model_path):
        print(f"❌ Model file not found: {model_path}")
        return False
        
    if not os.path.exists(config_path):
        print(f"❌ Config file not found: {config_path}")
        return False
    
    print(f"✅ Model file found: {os.path.basename(model_path)}")
    print(f"✅ Config file found: {os.path.basename(config_path)}")
    
    # Get model size
    model_size_mb = os.path.getsize(model_path) / (1024 * 1024)
    print(f"📊 Model size: {model_size_mb:.1f} MB")
    
    try:
        # Import TTS
        print("\n🔧 Loading TTS library...")
        from TTS.utils.manage import ModelManager
        from TTS.tts.configs.tacotron2_config import Tacotron2Config
        from TTS.tts.models.tacotron2 import Tacotron2
        from TTS.utils.audio import AudioProcessor
        from TTS.utils.synthesizer import Synthesizer
        
        print("🔧 Loading trained model...")
        
        # Initialize synthesizer with our trained model
        synthesizer = Synthesizer(
            tts_checkpoint=model_path,
            tts_config_path=config_path,
            use_cuda=False  # Jetson Nano might not have CUDA support for this
        )
        
        print("✅ Model loaded successfully!")
        
        # Create output directory
        output_dir = "/ssd/tts_project/hello_world_output"
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\n🎵 GENERATING HELLO WORLD MESSAGE")
        print(f"Output directory: {output_dir}")
        print("-" * 40)
        
        # The requested text
        text = "Hello World, this is the trained speaker speaking, coming to you from the AI realm"
        output_file = os.path.join(output_dir, "hello_world_voice.wav")
        
        print(f"📝 Text: {text}")
        print(f"🎵 Generating: {os.path.basename(output_file)}")
        
        # Generate speech
        start_time = datetime.now()
        wav = synthesizer.tts(text)
        end_time = datetime.now()
        
        # Save the audio
        synthesizer.save_wav(wav, output_file)
        
        # Calculate timing
        processing_time = (end_time - start_time).total_seconds()
        file_size = os.path.getsize(output_file)
        
        print(f" > Processing time: {processing_time:.2f} seconds")
        print(f"✅ Generated: {file_size:,} bytes")
        
        print(f"\n🎉 SUCCESS! Hello World message generated")
        print(f"📁 Output file: {output_file}")
        print(f"🎧 You can now listen to Henry's Hello World message!")
        
        # Show file details
        print(f"\n📋 Generated File:")
        print(f"   🎵 {os.path.basename(output_file)} ({file_size:,} bytes)")
        print(f"   📍 {output_file}")
        
        print(f"\n🎊 HELLO WORLD GENERATION COMPLETED!")
        print(f"🎤 The voice says: 'Hello World' from the AI realm!")
        
        return True
        
    except Exception as e:
        print(f"💥 Error generating speech: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = generate_hello_world()
    if not success:
        print("💥 Hello World generation failed. Check the errors above.")
        sys.exit(1)
    else:
        print("✅ Hello World generation completed successfully!")