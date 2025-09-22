#!/usr/bin/env python3
"""
TTS Model Testing Script
Tests the trained custom voice model by generating speech samples
"""

import os
import sys
import argparse
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
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 50}")
    print(f"🎵 {title}")
    print(f"{'=' * 50}{Colors.END}")

def find_best_checkpoint(training_output_dir):
    """Find the best checkpoint from training"""
    print_section("Finding Best Model Checkpoint")
    
    if not os.path.exists(training_output_dir):
        print_colored(f"❌ Training output directory not found: {training_output_dir}", Colors.RED)
        return None
    
    # Look for checkpoints
    checkpoint_files = list(Path(training_output_dir).glob("**/checkpoint_*.pth"))
    if not checkpoint_files:
        print_colored("❌ No checkpoints found! Make sure training has completed.", Colors.RED)
        return None
    
    # Sort by modification time to get the latest
    latest_checkpoint = max(checkpoint_files, key=lambda p: p.stat().st_mtime)
    print_colored(f"✅ Found latest checkpoint: {latest_checkpoint.name}", Colors.GREEN)
    
    return str(latest_checkpoint)

def find_config_file(training_output_dir):
    """Find the training config file"""
    config_files = list(Path(training_output_dir).glob("**/config.json"))
    if not config_files:
        # Try the project root
        project_config = "/ssd/tts_project/training_config.json"
        if os.path.exists(project_config):
            return project_config
        print_colored("❌ No config file found!", Colors.RED)
        return None
    
    return str(config_files[0])

def test_model_synthesis(checkpoint_path, config_path, test_texts=None):
    """Test the model by generating speech samples"""
    print_section("Testing Model Speech Synthesis")
    
    if test_texts is None:
        test_texts = [
            "Hello, this is the trained voice speaking.",
            "The quick brown fox jumps over the lazy dog.",
            "I hope this custom voice model sounds good!",
            "This is a test of the text to speech system.",
            "Welcome to the world of artificial intelligence."
        ]
    
    print_colored("🎯 Testing with sample texts:", Colors.BLUE)
    for i, text in enumerate(test_texts, 1):
        print_colored(f"   {i}. {text}", Colors.BLUE)
    
    output_dir = "/ssd/tts_project/test_outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    print_colored(f"\n🔊 Generated audio will be saved to: {output_dir}", Colors.CYAN)
    
    # Import TTS after we know everything is ready
    try:
        from TTS.api import TTS
        print_colored("✅ TTS library loaded successfully", Colors.GREEN)
    except ImportError as e:
        print_colored(f"❌ Error importing TTS: {e}", Colors.RED)
        return False
    
    try:
        # Initialize TTS with the trained model
        print_colored("🔄 Loading trained model...", Colors.YELLOW)
        tts = TTS(model_path=checkpoint_path, config_path=config_path)
        print_colored("✅ Model loaded successfully!", Colors.GREEN)
        
        # Generate speech for each test text
        for i, text in enumerate(test_texts, 1):
            output_file = os.path.join(output_dir, f"test_sample_{i}.wav")
            print_colored(f"🎵 Generating speech {i}/{len(test_texts)}: '{text[:30]}{'...' if len(text) > 30 else ''}'", Colors.YELLOW)
            
            tts.tts_to_file(text=text, file_path=output_file)
            print_colored(f"   ✅ Saved: {os.path.basename(output_file)}", Colors.GREEN)
        
        print_colored(f"\n🎉 All test samples generated successfully!", Colors.GREEN)
        print_colored(f"📁 Check the audio files in: {output_dir}", Colors.CYAN)
        
        return True
        
    except Exception as e:
        print_colored(f"❌ Error during speech synthesis: {e}", Colors.RED)
        print_colored(f"This might indicate the model needs more training", Colors.YELLOW)
        return False

def play_audio_sample(audio_file):
    """Play an audio sample if possible"""
    try:
        import subprocess
        # Try to play with aplay (common on Linux)
        result = subprocess.run(['aplay', audio_file], capture_output=True, text=True)
        if result.returncode == 0:
            print_colored(f"🔊 Played: {os.path.basename(audio_file)}", Colors.GREEN)
        else:
            print_colored(f"⚠️  Could not play audio (aplay not available)", Colors.YELLOW)
    except Exception:
        print_colored(f"⚠️  Audio playback not available", Colors.YELLOW)

def interactive_testing(checkpoint_path, config_path):
    """Interactive testing mode where user can input custom text"""
    print_section("Interactive Testing Mode")
    
    try:
        from TTS.api import TTS
        print_colored("🔄 Loading model for interactive testing...", Colors.YELLOW)
        tts = TTS(model_path=checkpoint_path, config_path=config_path)
        print_colored("✅ Model ready for interactive testing!", Colors.GREEN)
        
        output_dir = "/ssd/tts_project/test_outputs"
        os.makedirs(output_dir, exist_ok=True)
        
        print_colored("\n💬 Enter text to convert to speech (or 'quit' to exit):", Colors.CYAN)
        
        counter = 1
        while True:
            text = input(f"{Colors.BOLD}Text to speak: {Colors.END}").strip()
            
            if text.lower() in ['quit', 'exit', 'q']:
                break
            
            if not text:
                continue
            
            try:
                output_file = os.path.join(output_dir, f"interactive_{counter}.wav")
                print_colored(f"🎵 Generating speech...", Colors.YELLOW)
                tts.tts_to_file(text=text, file_path=output_file)
                print_colored(f"✅ Audio saved: {os.path.basename(output_file)}", Colors.GREEN)
                
                # Try to play the audio
                play_audio_sample(output_file)
                
                counter += 1
                
            except Exception as e:
                print_colored(f"❌ Error generating speech: {e}", Colors.RED)
        
        print_colored("👋 Interactive testing finished!", Colors.CYAN)
        return True
        
    except Exception as e:
        print_colored(f"❌ Error in interactive mode: {e}", Colors.RED)
        return False

def main():
    parser = argparse.ArgumentParser(description="Test trained TTS model")
    parser.add_argument("--checkpoint", type=str, help="Path to model checkpoint")
    parser.add_argument("--config", type=str, help="Path to config file")
    parser.add_argument("--interactive", action="store_true", help="Interactive testing mode")
    parser.add_argument("--text", type=str, help="Custom text to synthesize")
    args = parser.parse_args()
    
    print_colored(f"{Colors.BOLD}🎤 TTS Model Testing", Colors.CYAN)
    print_colored(f"Testing the custom voice model", Colors.CYAN)
    
    project_dir = "/ssd/tts_project"
    training_output_dir = os.path.join(project_dir, "training_output")
    
    # Find checkpoint and config
    checkpoint_path = args.checkpoint
    if not checkpoint_path:
        checkpoint_path = find_best_checkpoint(training_output_dir)
        if not checkpoint_path:
            return False
    
    config_path = args.config
    if not config_path:
        config_path = find_config_file(training_output_dir)
        if not config_path:
            return False
    
    print_colored(f"📄 Using config: {os.path.basename(config_path)}", Colors.BLUE)
    print_colored(f"🎯 Using checkpoint: {os.path.basename(checkpoint_path)}", Colors.BLUE)
    
    # Test the model
    if args.interactive:
        success = interactive_testing(checkpoint_path, config_path)
    elif args.text:
        success = test_model_synthesis(checkpoint_path, config_path, [args.text])
    else:
        success = test_model_synthesis(checkpoint_path, config_path)
    
    if success:
        print_section("Testing Complete!")
        print_colored("🎉 Model testing completed successfully!", Colors.GREEN)
        if not args.interactive:
            print_colored("Next steps:", Colors.BLUE)
            print_colored("   - Listen to the generated audio samples", Colors.BLUE)
            print_colored("   - Use --interactive mode to test custom text", Colors.BLUE)
            print_colored("   - If quality is poor, continue training", Colors.BLUE)
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)