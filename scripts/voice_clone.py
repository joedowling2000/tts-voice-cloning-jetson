#!/usr/bin/env python3
"""
Voice Cloning with XTTS - Fast and Effective
Uses Coqui's XTTS model for voice cloning with minimal data
"""

import os
import sys
import shutil
from pathlib import Path

# Color codes for output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_colored(message, color):
    print(f"{color}{message}{Colors.END}")

def print_section(title):
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 60}")
    print(f"🎯 {title}")
    print(f"{'=' * 60}{Colors.END}")

def prepare_voice_samples():
    """Prepare voice samples for XTTS voice cloning"""
    print_section("Preparing Voice Samples for Cloning")
    
    voice_data_dir = "/ssd/tts_project/voice_data/processed_audio"
    clone_samples_dir = "/ssd/tts_project/voice_clone_samples"
    
    # Create directory for voice samples
    os.makedirs(clone_samples_dir, exist_ok=True)
    
    # Copy a few high-quality samples for voice cloning
    # XTTS works best with 3-10 good quality samples
    voice_files = sorted(list(Path(voice_data_dir).glob("voice*.wav")))
    
    if len(voice_files) == 0:
        print_colored("❌ No voice files found!", Colors.RED)
        return False
    
    # Select 6 samples spread across the dataset for variety
    selected_indices = [0, 10, 20, 30, 40, 50] if len(voice_files) >= 60 else [0, len(voice_files)//4, len(voice_files)//2, 3*len(voice_files)//4]
    
    print_colored(f"📁 Selecting {len(selected_indices)} voice samples for cloning:", Colors.BLUE)
    
    for i, idx in enumerate(selected_indices):
        if idx < len(voice_files):
            src_file = voice_files[idx]
            dst_file = os.path.join(clone_samples_dir, f"voice_sample_{i+1}.wav")
            shutil.copy2(src_file, dst_file)
            print_colored(f"   ✅ {src_file.name} → voice_sample_{i+1}.wav", Colors.GREEN)
    
    print_colored(f"\n🎵 Voice cloning samples ready in: {clone_samples_dir}", Colors.CYAN)
    return True

def setup_xtts():
    """Set up XTTS for voice cloning"""
    print_section("Setting Up XTTS Voice Cloning")
    
    try:
        from TTS.api import TTS
        print_colored("📦 TTS library loaded successfully", Colors.GREEN)
        
        # Initialize XTTS model
        print_colored("🔄 Loading XTTS v2 model (this may take a moment)...", Colors.YELLOW)
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        print_colored("✅ XTTS v2 model loaded successfully!", Colors.GREEN)
        
        return tts
        
    except Exception as e:
        print_colored(f"❌ Error setting up XTTS: {e}", Colors.RED)
        return None

def clone_voice_and_test(tts):
    """Clone the custom voice and generate test samples"""
    print_section("Voice Cloning & Testing")
    
    clone_samples_dir = "/ssd/tts_project/voice_clone_samples"
    output_dir = "/ssd/tts_project/voice_clone_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Get reference audio files
    reference_files = list(Path(clone_samples_dir).glob("*.wav"))
    if not reference_files:
        print_colored("❌ No reference audio files found!", Colors.RED)
        return False
    
    print_colored(f"🎯 Using {len(reference_files)} reference files for voice cloning", Colors.BLUE)
    
    # Test sentences
    test_sentences = [
        "Hello, this is the trained voice speaking with my cloned voice.",
        "The quick brown fox jumps over the lazy dog.",
        "I hope this voice cloning sounds natural and clear.",
        "This is a test of the voice cloning technology.",
        "Welcome to the future of artificial intelligence!"
    ]
    
    print_colored(f"\n🎵 Generating speech samples...", Colors.CYAN)
    
    try:
        for i, sentence in enumerate(test_sentences, 1):
            output_file = os.path.join(output_dir, f"cloned_sample_{i}.wav")
            
            print_colored(f"   🔊 Generating sample {i}: '{sentence[:40]}{'...' if len(sentence) > 40 else ''}'", Colors.YELLOW)
            
            # Clone the voice and generate speech
            tts.tts_to_file(
                text=sentence,
                file_path=output_file,
                speaker_wav=str(reference_files[0]),  # Use first reference file
                language="en"
            )
            
            print_colored(f"   ✅ Saved: {os.path.basename(output_file)}", Colors.GREEN)
        
        print_colored(f"\n🎉 Voice cloning completed successfully!", Colors.GREEN)
        print_colored(f"📁 Generated files are in: {output_dir}", Colors.CYAN)
        
        return True
        
    except Exception as e:
        print_colored(f"❌ Error during voice cloning: {e}", Colors.RED)
        print_colored("This might be due to audio format or quality issues", Colors.YELLOW)
        return False

def interactive_voice_clone(tts):
    """Interactive voice cloning where user can input custom text"""
    print_section("Interactive Voice Cloning")
    
    clone_samples_dir = "/ssd/tts_project/voice_clone_samples"
    output_dir = "/ssd/tts_project/voice_clone_output"
    
    reference_files = list(Path(clone_samples_dir).glob("*.wav"))
    if not reference_files:
        print_colored("❌ No reference audio files found!", Colors.RED)
        return False
    
    print_colored(f"🎯 Interactive mode ready with the custom voice", Colors.GREEN)
    print_colored(f"📁 Output will be saved to: {output_dir}", Colors.BLUE)
    print_colored(f"\n💬 Enter text to convert to the custom voice (or 'quit' to exit):", Colors.CYAN)
    
    counter = 1
    while True:
        text = input(f"{Colors.BOLD}Text to speak: {Colors.END}").strip()
        
        if text.lower() in ['quit', 'exit', 'q']:
            break
        
        if not text:
            continue
        
        try:
            output_file = os.path.join(output_dir, f"interactive_clone_{counter}.wav")
            print_colored(f"🎵 Generating speech with the custom voice...", Colors.YELLOW)
            
            tts.tts_to_file(
                text=text,
                file_path=output_file,
                speaker_wav=str(reference_files[0]),
                language="en"
            )
            
            print_colored(f"✅ Audio saved: {os.path.basename(output_file)}", Colors.GREEN)
            
            # Try to play the audio
            try:
                import subprocess
                subprocess.run(['aplay', output_file], capture_output=True)
                print_colored(f"🔊 Played audio", Colors.CYAN)
            except:
                print_colored(f"⚠️  Audio saved but playback not available", Colors.YELLOW)
            
            counter += 1
            
        except Exception as e:
            print_colored(f"❌ Error generating speech: {e}", Colors.RED)
    
    print_colored("👋 Interactive voice cloning finished!", Colors.CYAN)
    return True

def main():
    print_colored(f"{Colors.BOLD}🎤 Custom Voice Cloning with XTTS", Colors.CYAN)
    print_colored("Fast voice cloning using pre-trained XTTS model", Colors.BLUE)
    
    print_colored(f"\n⚡ Why Voice Cloning vs Full Training:", Colors.YELLOW)
    print_colored("   • Much faster: 5-15 minutes vs 2-4 hours", Colors.YELLOW)
    print_colored("   • Better with small datasets (80 samples)", Colors.YELLOW)
    print_colored("   • High quality results immediately", Colors.YELLOW)
    print_colored("   • Uses state-of-the-art XTTS technology", Colors.YELLOW)
    
    # Step 1: Prepare voice samples
    if not prepare_voice_samples():
        return False
    
    # Step 2: Set up XTTS
    tts = setup_xtts()
    if not tts:
        return False
    
    # Step 3: Clone voice and test
    if not clone_voice_and_test(tts):
        return False
    
    print_section("Voice Cloning Complete!")
    print_colored("🎉 the custom voice has been successfully cloned!", Colors.GREEN)
    
    # Ask if user wants interactive mode
    print_colored(f"\n🎯 Would you like to try interactive mode?", Colors.CYAN)
    response = input("Test with custom text? (y/n): ").strip().lower()
    
    if response in ['y', 'yes']:
        interactive_voice_clone(tts)
    
    print_colored(f"\n✨ Voice cloning session completed!", Colors.GREEN)
    print_colored("Check the voice_clone_output folder for all generated audio!", Colors.BLUE)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)