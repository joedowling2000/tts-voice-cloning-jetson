#!/usr/bin/env python3
"""
Coqui TTS Training Script for Custom Voice Model
Trains a Tacotron2-DDC model using the processed voice data
"""

import os
import sys
import json
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
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 60}")
    print(f"🎯 {title}")
    print(f"{'=' * 60}{Colors.END}")

def create_training_config(project_dir, model_name="custom_voice"):
    """Create TTS training configuration"""
    print_section("Creating Training Configuration")
    
    config = {
        "model": "tacotron2_ddc",
        "run_name": model_name,
        "run_description": "Custom voice training",
        
        # Dataset configuration
        "datasets": [
            {
                "name": "voice_dataset",
                "path": os.path.join(project_dir, "voice_data"),
                "meta_file_train": "metadata.csv",
                "language": "en"
            }
        ],
        
        # Audio configuration
        "audio": {
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
            "trim_db": 60,
            "do_sound_norm": True,
            "stats_path": None
        },
        
        # Model configuration
        "model_args": {
            "r": 1,
            "gradual_training": [[0, 6, 64], [10000, 4, 32], [50000, 3, 32], [130000, 2, 32]],
            "memory_size": 5,
            "prenet_type": "original",
            "prenet_dropout": True,
            "forward_attn": True,
            "trans_agent": True,
            "forward_attn_mask": True,
            "location_attn": False,
            "attn_norm": "sigmoid",
            "double_decoder_consistency": True,
            "ddc_r": 6,
            "speakers_file": None,
            "use_speaker_embedding": False
        },
        
        # Training configuration
        "batch_size": 32,
        "eval_batch_size": 16,
        "num_loader_workers": 4,
        "num_eval_loader_workers": 2,
        "run_eval": True,
        "test_delay_epochs": 10,
        
        # Optimizer
        "epochs": 1000,
        "lr": 0.0001,
        "wd": 0.000001,
        "grad_clip": 1.0,
        "lr_scheduler": "NoamLR",
        "lr_scheduler_params": {
            "warmup_steps": 4000
        },
        
        # Loss configuration
        "loss_masking": True,
        "decoder_loss_alpha": 0.25,
        "postnet_loss_alpha": 0.25,
        "postnet_diff_spec_alpha": 0.25,
        "decoder_diff_spec_alpha": 0.25,
        "decoder_ssim_alpha": 0.25,
        "postnet_ssim_alpha": 0.25,
        
        # Logging and saving
        "print_step": 25,
        "plot_step": 100,
        "log_model_step": 1000,
        "save_step": 1000,
        "save_n_checkpoints": 5,
        "save_checkpoints": True,
        
        # Paths
        "output_path": os.path.join(project_dir, "training_output"),
        "logger_uri": None,
        "tb_model_param_stats": False,
        
        # Preprocessing
        "precompute_num_workers": 4,
        "use_phonemes": False,
        "phoneme_language": "en-us",
        "compute_input_seq_cache": True,
        "text_cleaner": "english_cleaners",
        "enable_eos_bos_chars": False,
        "test_sentences_file": "",
        "phoneme_cache_path": os.path.join(project_dir, "phoneme_cache"),
        
        # Mixed precision training (if supported)
        "mixed_precision": False,
        
        # Distributed training
        "distributed": False
    }
    
    # Create output directory
    os.makedirs(config["output_path"], exist_ok=True)
    os.makedirs(config["phoneme_cache_path"], exist_ok=True)
    
    # Save configuration
    config_path = os.path.join(project_dir, "training_config.json")
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print_colored(f"✅ Configuration saved to: {config_path}", Colors.GREEN)
    print_colored(f"📁 Training output will be saved to: {config['output_path']}", Colors.BLUE)
    
    return config_path

def run_training(config_path, resume_checkpoint=None):
    """Run the TTS training"""
    print_section("Starting TTS Model Training")
    
    # Build training command
    cmd_parts = [
        "python3", "-m", "TTS.bin.train_tts",
        "--config_path", config_path
    ]
    
    if resume_checkpoint:
        cmd_parts.extend(["--restore_path", resume_checkpoint])
        print_colored(f"🔄 Resuming training from: {resume_checkpoint}", Colors.YELLOW)
    
    # Print training information
    print_colored("🚀 Training Configuration:", Colors.BLUE)
    print_colored(f"   Config file: {config_path}", Colors.BLUE)
    print_colored(f"   Model: Tacotron2-DDC", Colors.BLUE)
    print_colored(f"   Expected duration: 2-4 hours (depending on Jetson performance)", Colors.BLUE)
    print_colored(f"   Progress monitoring: Check training_output/logs/", Colors.BLUE)
    
    print_colored(f"\n📋 Training Command:", Colors.CYAN)
    cmd_str = " ".join(cmd_parts)
    print_colored(f"   {cmd_str}", Colors.CYAN)
    
    print_colored(f"\n⚠️  Training will take a significant amount of time!", Colors.YELLOW)
    print_colored(f"   You can monitor progress in another terminal with:", Colors.YELLOW)
    print_colored(f"   tensorboard --logdir /ssd/tts_project/training_output/", Colors.YELLOW)
    
    # Ask for confirmation
    response = input(f"\n{Colors.BOLD}Start training now? (y/n): {Colors.END}")
    if response.lower() not in ['y', 'yes']:
        print_colored("Training cancelled by user", Colors.YELLOW)
        return False
    
    print_colored(f"\n🎯 Starting training... This will take 2-4 hours!", Colors.GREEN)
    
    # Execute training command
    import subprocess
    try:
        result = subprocess.run(cmd_parts, check=True, cwd="/ssd/tts_project")
        print_colored(f"✅ Training completed successfully!", Colors.GREEN)
        return True
    except subprocess.CalledProcessError as e:
        print_colored(f"❌ Training failed with error code {e.returncode}", Colors.RED)
        print_colored(f"Check the logs in training_output/ for details", Colors.RED)
        return False
    except KeyboardInterrupt:
        print_colored(f"\n⚠️  Training interrupted by user", Colors.YELLOW)
        print_colored(f"You can resume training later using the latest checkpoint", Colors.YELLOW)
        return False

def show_training_info():
    """Display training information and estimates"""
    print_section("Training Information & Time Estimates")
    
    print_colored("📊 Training Details:", Colors.BLUE)
    print_colored("   Model: Tacotron2-DDC (Text-to-Speech)", Colors.BLUE)
    print_colored("   Data: 80 audio samples (~9 minutes total)", Colors.BLUE)
    print_colored("   Target epochs: 1000 (will converge earlier)", Colors.BLUE)
    
    print_colored("\n⏱️  Time Estimates (Jetson Nano):", Colors.YELLOW)
    print_colored("   Setup & preprocessing: 5-10 minutes", Colors.YELLOW)
    print_colored("   Training (400-600 epochs): 2-4 hours", Colors.YELLOW)
    print_colored("   Model will start producing recognizable speech after ~200 epochs", Colors.YELLOW)
    print_colored("   Best quality achieved around 400-600 epochs", Colors.YELLOW)
    
    print_colored("\n📈 Progress Monitoring:", Colors.CYAN)
    print_colored("   Training logs: /ssd/tts_project/training_output/logs/", Colors.CYAN)
    print_colored("   Model checkpoints: /ssd/tts_project/training_output/", Colors.CYAN)
    print_colored("   TensorBoard: tensorboard --logdir /ssd/tts_project/training_output/", Colors.CYAN)
    
    print_colored("\n💡 Tips:", Colors.GREEN)
    print_colored("   - Training will auto-save checkpoints every 1000 steps", Colors.GREEN)
    print_colored("   - You can safely stop training and resume later", Colors.GREEN)
    print_colored("   - Monitor loss values - they should decrease over time", Colors.GREEN)
    print_colored("   - Test audio samples will be generated periodically", Colors.GREEN)

def main():
    parser = argparse.ArgumentParser(description="Train custom TTS model")
    parser.add_argument("--resume", type=str, help="Path to checkpoint to resume from")
    parser.add_argument("--info-only", action="store_true", help="Show training info without starting")
    args = parser.parse_args()
    
    print_colored(f"{Colors.BOLD}🎤 Coqui TTS Model Training", Colors.CYAN)
    print_colored(f"Training custom voice model", Colors.CYAN)
    
    project_dir = "/ssd/tts_project"
    
    # Show training information
    show_training_info()
    
    if args.info_only:
        return
    
    # Check if we're in the right environment
    if not os.path.exists(os.path.join(project_dir, "coqui_env")):
        print_colored("❌ Coqui environment not found! Make sure you're in the correct directory", Colors.RED)
        return False
    
    # Create training configuration
    config_path = create_training_config(project_dir)
    
    # Run training
    success = run_training(config_path, args.resume)
    
    if success:
        print_section("Training Complete!")
        print_colored("🎉 Your custom TTS model has been trained!", Colors.GREEN)
        print_colored("Next steps:", Colors.BLUE)
        print_colored("   1. Test the model with the testing script", Colors.BLUE)
        print_colored("   2. Generate speech samples", Colors.BLUE)
        print_colored("   3. Fine-tune if needed", Colors.BLUE)
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)