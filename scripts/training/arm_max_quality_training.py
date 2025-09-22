#!/usr/bin/env python3
"""
ARM Maximum Quality Training Script
Uses TTS v0.13.3 for the highest possible quality with all 80 samples
Optimized specifically for Jetson Nano ARM architecture
"""

import os
import sys
import subprocess
import time
import json
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_colored(message, color):
    print(f"{color}{message}{Colors.END}")

def print_header(title):
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 80}")
    print(f"🎯 {title}")
    print(f"{'=' * 80}{Colors.END}")

def validate_environment():
    """Validate the ARM environment is ready"""
    print_header("VALIDATING ARM ENVIRONMENT")
    
    env_path = "/ssd/tts_project/tts_arm_env"
    python_path = f"{env_path}/bin/python3"
    
    # Check if environment exists
    if not os.path.exists(env_path):
        print_colored("❌ ARM environment not found!", Colors.RED)
        return False
    
    # Test TTS import
    try:
        result = subprocess.run([
            python_path, "-c", 
            "import TTS; print(f'TTS {TTS.__version__} ready'); import torch; print(f'PyTorch {torch.__version__} ready')"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print_colored("✅ ARM environment validated:", Colors.GREEN)
            for line in result.stdout.strip().split('\n'):
                print_colored(f"   {line}", Colors.GREEN)
            return True
        else:
            print_colored(f"❌ Environment test failed: {result.stderr}", Colors.RED)
            return False
            
    except Exception as e:
        print_colored(f"❌ Environment validation error: {e}", Colors.RED)
        return False

def setup_training_directories():
    """Set up all necessary directories"""
    print_header("SETTING UP TRAINING DIRECTORIES")
    
    directories = [
        "/ssd/tts_project/arm_max_quality_output",
        "/ssd/tts_project/arm_max_quality_output/logs",
        "/ssd/tts_project/arm_max_quality_output/checkpoints"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print_colored(f"✅ Created: {directory}", Colors.GREEN)
    
    return True

def validate_training_data():
    """Validate all training data is ready"""
    print_header("VALIDATING TRAINING DATA")
    
    # Check metadata file
    metadata_path = "/ssd/tts_project/voice_data/metadata_ljspeech.csv"
    if not os.path.exists(metadata_path):
        print_colored(f"❌ Metadata file not found: {metadata_path}", Colors.RED)
        return False
    
    # Count samples
    with open(metadata_path, 'r') as f:
        sample_count = len(f.readlines())
    
    print_colored(f"✅ Found {sample_count} training samples", Colors.GREEN)
    
    # Check audio directory
    audio_dir = "/ssd/tts_project/voice_data"
    wav_files = [f for f in os.listdir(audio_dir) if f.endswith('.wav')]
    print_colored(f"✅ Found {len(wav_files)} WAV files", Colors.GREEN)
    
    if sample_count != len(wav_files):
        print_colored(f"⚠️  Metadata ({sample_count}) and WAV files ({len(wav_files)}) count mismatch", Colors.YELLOW)
    
    return True

def start_tensorboard():
    """Start TensorBoard for monitoring"""
    print_header("STARTING TENSORBOARD MONITORING")
    
    log_dir = "/ssd/tts_project/arm_max_quality_output"
    
    # Kill any existing TensorBoard
    os.system("pkill -f tensorboard")
    time.sleep(2)
    
    # Start TensorBoard
    cmd = [
        "/ssd/tts_project/tts_arm_env/bin/tensorboard",
        "--logdir", log_dir,
        "--port", "6008",
        "--host", "0.0.0.0"
    ]
    
    try:
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
        print_colored("✅ TensorBoard started on http://localhost:6008", Colors.GREEN)
        return True
    except Exception as e:
        print_colored(f"⚠️  TensorBoard start failed: {e}", Colors.YELLOW)
        return False

def start_maximum_quality_training():
    """Start the maximum quality training process"""
    print_header("STARTING MAXIMUM QUALITY TRAINING")
    
    config_path = "/ssd/tts_project/arm_max_quality_config.json"
    env_path = "/ssd/tts_project/tts_arm_env"
    python_path = f"{env_path}/bin/python3"
    
    print_colored("🎯 TRAINING SPECIFICATIONS:", Colors.CYAN)
    print_colored("   Model: Tacotron2 (Maximum Quality)", Colors.CYAN)
    print_colored("   Data: ALL 80 samples", Colors.CYAN)
    print_colored("   Epochs: 1000 (extended for quality)", Colors.CYAN)
    print_colored("   Environment: TTS v0.13.3 ARM-optimized", Colors.CYAN)
    print_colored("   Expected Duration: 10-15 hours", Colors.CYAN)
    print_colored("   Goal: Professional-grade Henry voice", Colors.CYAN)
    
    # Set up environment variables
    env = os.environ.copy()
    env['CUDA_VISIBLE_DEVICES'] = ''
    env['PATH'] = f"{env_path}/bin:" + env['PATH']
    env['VIRTUAL_ENV'] = env_path
    env['PYTHONPATH'] = f"{env_path}/lib/python3.10/site-packages"
    
    # Training command
    cmd = [
        python_path,
        "-m", "TTS.bin.train_tts",
        "--config_path", config_path
    ]
    
    print_colored(f"\n🚀 LAUNCHING TRAINING:", Colors.GREEN)
    print_colored(f"Command: {' '.join(cmd)}", Colors.YELLOW)
    print_colored(f"Config: {config_path}", Colors.YELLOW)
    print_colored(f"Monitor: http://localhost:6008", Colors.YELLOW)
    print_colored(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", Colors.YELLOW)
    
    print_colored(f"🎤 MAXIMUM QUALITY TRAINING STARTING...", Colors.MAGENTA)
    print_colored(f"This will produce the highest possible quality Henry voice!", Colors.MAGENTA)
    print_colored("=" * 80, Colors.CYAN)
    
    try:
        # Change to project directory
        os.chdir("/ssd/tts_project")
        
        # Start training process
        process = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Create log file
        log_file = "/ssd/tts_project/arm_max_quality_output/training.log"
        
        # Stream output and log
        with open(log_file, 'w') as f:
            f.write(f"ARM Maximum Quality Training Log\n")
            f.write(f"Started: {datetime.now()}\n")
            f.write(f"Command: {' '.join(cmd)}\n")
            f.write("=" * 80 + "\n\n")
            
            for line in process.stdout:
                # Print to console
                print(line.rstrip())
                
                # Write to log
                f.write(line)
                f.flush()
        
        # Wait for completion
        process.wait()
        
        if process.returncode == 0:
            print_colored(f"\n🎉 MAXIMUM QUALITY TRAINING COMPLETED!", Colors.GREEN)
            print_colored("✅ Professional-grade Henry voice model ready!", Colors.GREEN)
            return True
        else:
            print_colored(f"\n❌ Training failed with exit code: {process.returncode}", Colors.RED)
            return False
            
    except KeyboardInterrupt:
        print_colored(f"\n⚠️  Training interrupted by user", Colors.YELLOW)
        process.terminate()
        return False
    except Exception as e:
        print_colored(f"\n❌ Training error: {e}", Colors.RED)
        return False

def main():
    """Main training orchestrator"""
    print_colored(f"🎤 ARM MAXIMUM QUALITY TTS TRAINING", Colors.MAGENTA)
    print_colored("Training Henry's voice for absolute maximum quality", Colors.CYAN)
    print_colored(f"Using TTS v0.13.3 ARM-optimized environment", Colors.CYAN)
    
    # Validation steps
    if not validate_environment():
        print_colored("❌ Environment validation failed", Colors.RED)
        return False
    
    if not validate_training_data():
        print_colored("❌ Training data validation failed", Colors.RED)
        return False
    
    if not setup_training_directories():
        print_colored("❌ Directory setup failed", Colors.RED)
        return False
    
    # Start monitoring
    start_tensorboard()
    
    # Start training
    success = start_maximum_quality_training()
    
    if success:
        print_header("TRAINING COMPLETED SUCCESSFULLY")
        print_colored("🎉 Maximum quality Henry voice model is ready!", Colors.GREEN)
        print_colored("📁 Model location: /ssd/tts_project/arm_max_quality_output/", Colors.CYAN)
        print_colored("📊 View training: http://localhost:6008", Colors.CYAN)
    else:
        print_header("TRAINING INCOMPLETE")
        print_colored("❌ Training did not complete successfully", Colors.RED)
        print_colored("📋 Check logs: /ssd/tts_project/arm_max_quality_output/training.log", Colors.YELLOW)
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)