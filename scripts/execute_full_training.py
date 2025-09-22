#!/usr/bin/env python3
"""
Execute Full High-Quality Training
8+ hour training process using all 80 samples for maximum quality
"""

import os
import sys
import time
import subprocess
import json
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
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 70}")
    print(f"🎯 {title}")
    print(f"{'=' * 70}{Colors.END}")

def validate_environment():
    """Validate training environment is ready"""
    print_section("Validating Training Environment")
    
    checks = [
        ("/ssd/tts_project/coqui_env", "Coqui environment"),
        ("/ssd/tts_project/voice_data/metadata_train.csv", "Training metadata"),
        ("/ssd/tts_project/voice_data/metadata_val.csv", "Validation metadata"),
        ("/ssd/tts_project/voice_data/processed_audio", "Processed audio files"),
        ("/ssd/tts_project/full_training_config.json", "Training configuration")
    ]
    
    all_good = True
    for path, description in checks:
        if os.path.exists(path):
            print_colored(f"✅ {description}: Found", Colors.GREEN)
        else:
            print_colored(f"❌ {description}: Missing at {path}", Colors.RED)
            all_good = False
    
    if not all_good:
        print_colored("❌ Environment validation failed!", Colors.RED)
        return False
    
    # Check GPU/CUDA availability
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            print_colored(f"✅ GPU: {gpu_name}", Colors.GREEN)
        else:
            print_colored("⚠️  GPU: Not available (will use CPU - slower)", Colors.YELLOW)
    except ImportError:
        print_colored("⚠️  PyTorch: Not available", Colors.YELLOW)
    
    print_colored("✅ Environment validation passed!", Colors.GREEN)
    return True

def create_monitoring_script():
    """Create a monitoring script to track training progress"""
    monitoring_script = """#!/bin/bash
# Training Monitor Script

echo "🔍 TTS Training Monitor"
echo "======================="
echo ""

while true; do
    clear
    echo "🎤 Henry's Voice Training Monitor - $(date)"
    echo "============================================"
    echo ""
    
    if [ -d "/ssd/tts_project/full_training_output" ]; then
        echo "📁 Training Output Directory:"
        ls -la /ssd/tts_project/full_training_output/ | tail -10
        echo ""
        
        echo "📊 Latest Checkpoints:"
        find /ssd/tts_project/full_training_output -name "checkpoint_*.pth" -type f -exec ls -la {} \\; | tail -5
        echo ""
        
        echo "📈 Training Logs (last 10 lines):"
        if [ -f "/ssd/tts_project/full_training_output/train.log" ]; then
            tail -10 /ssd/tts_project/full_training_output/train.log
        else
            echo "No training log found yet..."
        fi
        echo ""
        
        echo "💾 Disk Usage:"
        du -sh /ssd/tts_project/full_training_output/
        echo ""
    else
        echo "⏳ Waiting for training to start..."
    fi
    
    echo "🔄 Updating in 30 seconds... (Ctrl+C to stop)"
    sleep 30
done
"""
    
    monitor_path = "/ssd/tts_project/monitor_training.sh"
    with open(monitor_path, 'w') as f:
        f.write(monitoring_script)
    
    os.chmod(monitor_path, 0o755)
    print_colored(f"✅ Monitoring script created: {monitor_path}", Colors.GREEN)
    print_colored("📋 Run in another terminal: ./monitor_training.sh", Colors.CYAN)

def start_training():
    """Start the high-quality training process"""
    print_section("Starting High-Quality Training")
    
    config_path = "/ssd/tts_project/full_training_config.json"
    output_dir = "/ssd/tts_project/full_training_output"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    print_colored("🎯 TRAINING CONFIGURATION:", Colors.BLUE)
    print_colored(f"   Config: {config_path}", Colors.BLUE)
    print_colored(f"   Output: {output_dir}", Colors.BLUE)
    print_colored(f"   Data: ALL 80 samples (70 train + 10 validation)", Colors.BLUE)
    print_colored(f"   Duration: 8-12 hours", Colors.BLUE)
    print_colored(f"   Quality: Production-ready", Colors.BLUE)
    
    print_colored("\n⏱️  TIMELINE:", Colors.YELLOW)
    print_colored("   First 1-2 hours: Basic pattern learning", Colors.YELLOW)
    print_colored("   Hours 2-4: Voice characteristics emerge", Colors.YELLOW)
    print_colored("   Hours 4-6: High-quality speech develops", Colors.YELLOW)
    print_colored("   Hours 6-8: Fine-tuning and polish", Colors.YELLOW)
    print_colored("   Hours 8+: Production-ready quality", Colors.YELLOW)
    
    print_colored("\n📊 WHAT YOU'LL SEE:", Colors.CYAN)
    print_colored("   • Decreasing loss values (good progress)", Colors.CYAN)
    print_colored("   • Checkpoints saved every 1000 steps", Colors.CYAN)
    print_colored("   • Audio samples generated periodically", Colors.CYAN)
    print_colored("   • Validation metrics every 500 steps", Colors.CYAN)
    
    print_colored("\n🔍 MONITORING:", Colors.GREEN)
    print_colored("   • Real-time progress in this terminal", Colors.GREEN)
    print_colored("   • Run ./monitor_training.sh in another terminal", Colors.GREEN)
    print_colored("   • TensorBoard: tensorboard --logdir full_training_output", Colors.GREEN)
    
    # Confirm before starting
    print_colored(f"\n{Colors.BOLD}⚠️  This will take 8-12 hours!{Colors.END}", Colors.YELLOW)
    print_colored("Make sure your Jetson Nano has adequate cooling and power.", Colors.YELLOW)
    print_colored("Training can be safely interrupted and resumed from checkpoints.", Colors.YELLOW)
    
    response = input(f"\n{Colors.BOLD}Start high-quality training? (yes/no): {Colors.END}").strip().lower()
    
    if response not in ['yes', 'y']:
        print_colored("Training cancelled.", Colors.YELLOW)
        return False
    
    # Build training command
    cmd = [
        "python3", "-m", "TTS.bin.train_tts",
        "--config_path", config_path,
        "--coqpit.output_path", output_dir,
        "--coqpit.datasets.0.path", "/ssd/tts_project/voice_data",
        "--coqpit.audio.sample_rate", "22050"
    ]
    
    print_colored(f"\n🚀 STARTING TRAINING...", Colors.GREEN)
    print_colored(f"Command: {' '.join(cmd)}", Colors.CYAN)
    print_colored(f"=" * 70, Colors.GREEN)
    
    # Start training process
    try:
        # Change to project directory
        os.chdir("/ssd/tts_project")
        
        # Activate virtual environment and run training
        env = os.environ.copy()
        env['PATH'] = f"/ssd/tts_project/coqui_env/bin:{env['PATH']}"
        env['VIRTUAL_ENV'] = "/ssd/tts_project/coqui_env"
        
        process = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        print_colored("🎯 Training started! Output below:", Colors.GREEN)
        print_colored("=" * 70, Colors.GREEN)
        
        # Stream output in real-time
        for line in process.stdout:
            print(line.rstrip())
            
            # Log to file as well
            with open(os.path.join(output_dir, "train.log"), "a") as log_file:
                log_file.write(line)
        
        process.wait()
        
        if process.returncode == 0:
            print_colored(f"\n🎉 TRAINING COMPLETED SUCCESSFULLY!", Colors.GREEN)
            print_colored(f"📁 Model saved in: {output_dir}", Colors.BLUE)
            return True
        else:
            print_colored(f"\n❌ Training failed with return code: {process.returncode}", Colors.RED)
            return False
            
    except KeyboardInterrupt:
        print_colored(f"\n⚠️  Training interrupted by user", Colors.YELLOW)
        print_colored("Training can be resumed from the latest checkpoint", Colors.YELLOW)
        return False
    except Exception as e:
        print_colored(f"\n❌ Training error: {e}", Colors.RED)
        return False

def show_next_steps():
    """Show what to do after training completes"""
    print_section("Next Steps After Training")
    
    print_colored("🎉 AFTER TRAINING COMPLETES:", Colors.GREEN)
    print_colored("   1. Test the trained model quality", Colors.GREEN)
    print_colored("   2. Compare with voice cloning results", Colors.GREEN)
    print_colored("   3. Generate speech samples", Colors.GREEN)
    print_colored("   4. Use interactive mode for custom text", Colors.GREEN)
    
    print_colored("\n📋 TESTING COMMANDS:", Colors.CYAN)
    print_colored("   # Test the trained model", Colors.CYAN)
    print_colored("   python3 scripts/test_model.py --checkpoint full_training_output/best_model.pth", Colors.CYAN)
    print_colored("   ", Colors.CYAN)
    print_colored("   # Interactive mode", Colors.CYAN)
    print_colored("   python3 scripts/test_model.py --interactive", Colors.CYAN)
    
    print_colored("\n🔄 IF TRAINING STOPS:", Colors.YELLOW)
    print_colored("   # Resume from latest checkpoint", Colors.YELLOW)
    print_colored("   python3 scripts/execute_full_training.py --resume", Colors.YELLOW)

def main():
    print_colored(f"{Colors.BOLD}🎤 HIGH-QUALITY TRAINING EXECUTION", Colors.CYAN)
    print_colored("Training Henry's voice with ALL 80 samples for maximum quality", Colors.BLUE)
    
    # Validate environment
    if not validate_environment():
        return False
    
    # Create monitoring tools
    create_monitoring_script()
    
    # Show next steps info
    show_next_steps()
    
    # Start training
    success = start_training()
    
    if success:
        print_section("Training Complete!")
        print_colored("🎉 HIGH-QUALITY TRAINING FINISHED!", Colors.GREEN)
        print_colored("Your production-ready Henry voice model is ready!", Colors.GREEN)
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)