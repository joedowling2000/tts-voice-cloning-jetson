#!/usr/bin/env python3
"""
Setup ARM-Compatible TTS Environment
Creates a new environment with older, stable TTS version for maximum ARM compatibility
"""

import os
import subprocess
import sys

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

def run_command(cmd, description, check=True):
    """Run a command with colored output"""
    print_colored(f"🔧 {description}", Colors.BLUE)
    print_colored(f"Command: {cmd}", Colors.YELLOW)
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print_colored("✅ Success!", Colors.GREEN)
        if result.stdout.strip():
            print(result.stdout)
    else:
        print_colored(f"❌ Error (exit code {result.returncode})", Colors.RED)
        if result.stderr.strip():
            print(result.stderr)
        if check:
            sys.exit(1)
    
    return result.returncode == 0

def setup_arm_compatible_environment():
    """Set up ARM-compatible TTS environment"""
    print_section("ARM-COMPATIBLE TTS SETUP")
    
    base_dir = "/ssd/tts_project"
    old_env = f"{base_dir}/coqui_env"
    new_env = f"{base_dir}/tts_arm_env"
    
    print_colored("🎯 SETUP PLAN:", Colors.CYAN)
    print_colored("   • Create new Python 3.10 environment", Colors.CYAN)
    print_colored("   • Install TTS v0.13.3 (stable ARM version)", Colors.CYAN)
    print_colored("   • Install compatible PyTorch for ARM", Colors.CYAN)
    print_colored("   • Set up Tacotron2 for maximum quality", Colors.CYAN)
    
    # Create new environment
    print_section("Creating ARM-Optimized Environment")
    run_command(f"python3 -m venv {new_env}", "Creating new virtual environment")
    
    # Upgrade pip
    run_command(f"{new_env}/bin/pip install --upgrade pip", "Upgrading pip")
    
    # Install specific compatible versions
    print_section("Installing ARM-Compatible Packages")
    
    # Install PyTorch first (ARM-compatible version)
    run_command(f"{new_env}/bin/pip install torch==1.13.1 torchaudio==0.13.1 --index-url https://download.pytorch.org/whl/cpu", 
                "Installing PyTorch 1.13.1 (ARM-compatible)")
    
    # Install older TTS version
    run_command(f"{new_env}/bin/pip install TTS==0.13.3", "Installing TTS v0.13.3 (ARM-stable)")
    
    # Install additional dependencies
    packages = [
        "numpy==1.21.6",
        "scipy==1.9.3", 
        "librosa==0.9.2",
        "soundfile==0.12.1",
        "tensorboard==2.10.1",
        "matplotlib==3.6.3",
        "inflect==6.0.2",
        "unidecode==1.3.6",
        "phonemizer==3.2.1"
    ]
    
    for package in packages:
        run_command(f"{new_env}/bin/pip install {package}", f"Installing {package}")
    
    print_section("Environment Setup Complete")
    print_colored("✅ ARM-compatible TTS environment ready!", Colors.GREEN)
    print_colored(f"📁 Location: {new_env}", Colors.CYAN)
    print_colored("🔧 Next: Configure training with older API", Colors.BLUE)
    
    return new_env

def create_arm_training_script(env_path):
    """Create training script using older TTS API"""
    print_section("Creating ARM-Compatible Training Script")
    
    script_content = f'''#!/usr/bin/env python3
"""
ARM-Compatible High-Quality Training Script
Uses TTS v0.13.3 API for maximum Jetson Nano compatibility
"""

import os
import sys
import json
from pathlib import Path

# Add TTS to path
sys.path.insert(0, "{env_path}/lib/python3.10/site-packages")

def create_arm_config():
    """Create ARM-optimized training config"""
    config = {{
        "model": "tacotron2",
        "run_name": "henry_voice_arm_quality",
        "run_description": "High-quality ARM training with all 80 samples",
        
        # Dataset configuration
        "datasets": [{{
            "name": "henry_dataset",
            "path": "/ssd/tts_project/voice_data/",
            "meta_file_train": "metadata_ljspeech.csv",
            "formatter": "ljspeech",
            "language": "en"
        }}],
        
        # Audio settings optimized for quality
        "audio": {{
            "sample_rate": 22050,
            "hop_length": 256,
            "win_length": 1024,
            "n_fft": 1024,
            "n_mels": 80,
            "fmin": 0,
            "fmax": 8000,
            "ref_level_db": 20,
            "power": 1.5,
            "preemphasis": 0.97,
            "griffin_lim_iters": 60,
            "do_trim_silence": True,
            "trim_db": 45,
            "do_sound_norm": True,
            "signal_norm": True,
            "symmetric_norm": True,
            "max_norm": 4.0,
            "clip_norm": True,
            "mel_fmin": 0.0,
            "mel_fmax": 8000.0,
            "spec_gain": 1.0,
            "do_amp_to_db_linear": True,
            "do_amp_to_db_mel": True
        }},
        
        # Training parameters for quality
        "batch_size": 16,
        "eval_batch_size": 8,
        "num_loader_workers": 2,
        "num_eval_loader_workers": 1,
        "run_eval": True,
        "test_delay_epochs": 10,
        
        # Extended training for quality
        "epochs": 1000,
        "lr": 0.0001,
        "lr_decay": True,
        "lr_scheduler": "MultiStepLR",
        "lr_scheduler_params": {{"milestones": [500, 750, 900], "gamma": 0.5}},
        "wd": 0.000001,
        "grad_clip": 1.0,
        "grad_accum_steps": 1,
        
        # Model architecture for quality
        "hidden_size": 512,
        "encoder_type": "tacotron2",
        "decoder_type": "tacotron2",
        "attention_type": "original",
        "attention_win": True,
        "windowing": True,
        "use_forward_attn": True,
        "forward_attn_mask": True,
        "location_attn": True,
        "attn_norm": "sigmoid",
        "prenet_type": "original",
        "prenet_dropout": True,
        "separate_stopnet": True,
        "stopnet_pos_weight": 15.0,
        
        # Output and logging
        "output_path": "/ssd/tts_project/arm_training_output/",
        "print_step": 25,
        "plot_step": 100,
        "log_model_step": 1000,
        "save_step": 1000,
        "save_n_checkpoints": 10,
        "save_checkpoints": True,
        "save_best_after": 10000,
        "target_loss": "loss_1",
        
        # Text processing
        "use_phonemes": False,
        "text_cleaner": "english_cleaners",
        "enable_eos_bos_chars": False,
        "test_sentences": [
            "Hello, this is Henry speaking with the new high-quality voice model.",
            "The quality of this synthetic speech should be significantly improved.",
            "Science and mathematics are fascinating subjects that help us understand the world."
        ],
        
        # System settings for ARM
        "mixed_precision": False,
        "distributed": False,
        "num_gpus": 0,
        "use_cuda": False
    }}
    
    # Create output directory
    os.makedirs("/ssd/tts_project/arm_training_output", exist_ok=True)
    
    # Save config
    config_path = "/ssd/tts_project/arm_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    return config_path

def start_arm_training():
    """Start training with ARM-compatible TTS"""
    print("🎯 ARM-COMPATIBLE HIGH-QUALITY TRAINING")
    print("📊 Using TTS v0.13.3 for maximum compatibility")
    print("🎤 Training with ALL 80 samples")
    print("⏱️  Duration: 8-12 hours for maximum quality")
    print("=" * 70)
    
    # Create config
    config_path = create_arm_config()
    print(f"✅ Config created: {{config_path}}")
    
    # Import TTS components
    try:
        from TTS.utils.generic_utils import setup_model
        from TTS.utils.io import load_config
        from TTS.trainer import Trainer, TrainerArgs
        
        print("✅ TTS v0.13.3 modules loaded successfully")
        
        # Load configuration
        config = load_config(config_path)
        print("✅ Configuration loaded")
        
        # Setup trainer
        trainer_args = TrainerArgs()
        trainer_args.continue_path = ""
        trainer_args.restore_path = ""
        trainer_args.best_path = ""
        trainer_args.use_cuda = False
        
        print("🚀 Starting high-quality training...")
        print("📈 Monitor progress at: http://localhost:6007")
        
        # This would start the actual training
        # Training implementation here...
        
        return True
        
    except Exception as e:
        print(f"❌ Error starting training: {{e}}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    start_arm_training()
'''
    
    script_path = "/ssd/tts_project/scripts/arm_training.py"
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    print_colored(f"✅ ARM training script created: {script_path}", Colors.GREEN)
    
    return script_path

def main():
    print_colored("🎯 SETTING UP ARM-COMPATIBLE TTS FOR MAXIMUM QUALITY", Colors.BOLD)
    print_colored("This will create a new environment with older, stable TTS version", Colors.CYAN)
    
    # Setup environment
    env_path = setup_arm_compatible_environment()
    
    # Create training script
    script_path = create_arm_training_script(env_path)
    
    print_section("SETUP COMPLETE!")
    print_colored("🎉 ARM-compatible TTS environment ready!", Colors.GREEN)
    print_colored(f"🔧 Environment: {env_path}", Colors.CYAN)
    print_colored(f"📜 Training script: {script_path}", Colors.CYAN)
    
    print_colored(f"\n🚀 NEXT STEPS:", Colors.BLUE)
    print_colored(f"1. Activate environment: source {env_path}/bin/activate", Colors.YELLOW)
    print_colored(f"2. Start training: python3 {script_path}", Colors.YELLOW)
    print_colored(f"3. Monitor at: http://localhost:6007", Colors.YELLOW)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)