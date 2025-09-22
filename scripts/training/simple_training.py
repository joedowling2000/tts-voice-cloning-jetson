#!/usr/bin/env python3
"""
Simple High-Quality Training Script
Uses LJSpeech formatter and all 80 samples for maximum quality
"""

import os
import sys
import subprocess

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
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 70}")
    print(f"🎯 {title}")
    print(f"{'=' * 70}{Colors.END}")

def start_simple_training():
    """Start training with direct TTS command"""
    print_section("HIGH-QUALITY TRAINING - DIRECT APPROACH")
    
    print_colored("🎯 TRAINING SETUP:", Colors.BLUE)
    print_colored("   Model: Tacotron2-DDC", Colors.BLUE)
    print_colored("   Data: ALL 80 samples", Colors.BLUE)
    print_colored("   Format: LJSpeech compatible", Colors.BLUE)
    print_colored("   Duration: 4-8 hours", Colors.BLUE)
    print_colored("   TensorBoard: http://localhost:6006", Colors.BLUE)
    
    # Create output directory
    output_dir = "/ssd/tts_project/training_output_v2"
    os.makedirs(output_dir, exist_ok=True)
    
    # Build command using TTS CLI with proper parameters
    cmd = [
        "/ssd/tts_project/coqui_env/bin/tts",
        "--model_name", "tts_models/en/ljspeech/tacotron2-DDC",
        "--dataset_path", "/ssd/tts_project/voice_data",
        "--dataset_name", "ljspeech", 
        "--output_path", output_dir,
        "--run_name", "custom_voice_v2",
        "--epochs", "400",
        "--batch_size", "16",
        "--lr", "0.0001",
        "--save_step", "1000",
        "--eval_step", "1000",
        "--print_step", "50"
    ]
    
    print_colored(f"\n🚀 STARTING TRAINING:", Colors.GREEN)
    print_colored(f"Output: {output_dir}", Colors.CYAN)
    print_colored(f"Command: {' '.join(cmd[:4])}...", Colors.CYAN)
    print_colored("=" * 70, Colors.GREEN)
    
    try:
        # Change to project directory
        os.chdir("/ssd/tts_project")
        
        # Set up environment
        env = os.environ.copy()
        env['PATH'] = f"/ssd/tts_project/coqui_env/bin:{env['PATH']}"
        
        # Start training
        process = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Stream output
        log_path = os.path.join(output_dir, "training.log")
        with open(log_path, "w") as log_file:
            for line in process.stdout:
                print(line.rstrip())
                log_file.write(line)
                log_file.flush()
        
        process.wait()
        
        if process.returncode == 0:
            print_colored(f"\n🎉 TRAINING COMPLETED!", Colors.GREEN)
            return True
        else:
            print_colored(f"\n❌ Training failed: {process.returncode}", Colors.RED)
            return False
            
    except Exception as e:
        print_colored(f"❌ Error: {e}", Colors.RED)
        return False

def main():
    print_colored(f"{Colors.BOLD}🎤 HIGH-QUALITY TRAINING (SIMPLIFIED)", Colors.CYAN)
    print_colored("Training with ALL 80 samples for maximum quality", Colors.BLUE)
    
    success = start_simple_training()
    
    if success:
        print_section("Training Complete!")
        print_colored("🎉 High-quality model ready for testing!", Colors.GREEN)
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)