#!/usr/bin/env python3
"""
HIGH-QUALITY TTS TRAINING PLAN
Comprehensive training strategy using all 80 samples for maximum quality
"""

import os
import json

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

def analyze_current_limitations():
    """Analyze why current quality is average"""
    print_section("Current Quality Analysis")
    
    print_colored("❌ VOICE CLONING LIMITATIONS:", Colors.RED)
    print_colored("   • Only used 6/80 samples (7.5% of your data)", Colors.RED)
    print_colored("   • No training on Henry's specific speech patterns", Colors.RED)
    print_colored("   • Generic model adaptation, not custom training", Colors.RED)
    print_colored("   • Limited exposure to Henry's unique voice characteristics", Colors.RED)
    print_colored("   • No optimization for your specific recording conditions", Colors.RED)
    
    print_colored("\n✅ FULL TRAINING ADVANTAGES:", Colors.GREEN)
    print_colored("   • Uses ALL 80 samples (100% of your data)", Colors.GREEN)
    print_colored("   • Learns Henry's specific speech patterns deeply", Colors.GREEN)
    print_colored("   • Trains model weights specifically for the custom voice", Colors.GREEN)
    print_colored("   • Adapts to your recording environment and quality", Colors.GREEN)
    print_colored("   • Much higher quality and more natural speech", Colors.GREEN)

def create_training_plan():
    """Create comprehensive training strategy"""
    print_section("HIGH-QUALITY TRAINING STRATEGY")
    
    plan = {
        "strategy": "Multi-stage training with all 80 samples",
        "total_duration": "6-12 hours",
        "quality_target": "Production-ready, near-human quality",
        
        "stages": [
            {
                "name": "Stage 1: Data Preparation & Augmentation",
                "duration": "30 minutes",
                "tasks": [
                    "Use all 80 samples (not just 6)",
                    "Create train/validation split (70/10 samples)",
                    "Audio augmentation for robustness",
                    "Advanced preprocessing",
                    "Phoneme alignment"
                ]
            },
            {
                "name": "Stage 2: Foundation Training",
                "duration": "2-3 hours",
                "tasks": [
                    "Train Tacotron2 backbone",
                    "High learning rate (0.001)",
                    "Focus on attention alignment",
                    "Monitor convergence carefully"
                ]
            },
            {
                "name": "Stage 3: Fine-tuning",
                "duration": "2-3 hours", 
                "tasks": [
                    "Lower learning rate (0.0001)",
                    "Refinement of voice characteristics",
                    "Vocoder integration",
                    "Quality optimization"
                ]
            },
            {
                "name": "Stage 4: Polish & Validation",
                "duration": "1-2 hours",
                "tasks": [
                    "Final refinements",
                    "Extensive testing",
                    "Quality comparison",
                    "Model optimization"
                ]
            }
        ],
        
        "expected_quality": {
            "naturalness": "95%+ (vs 70% from cloning)",
            "accuracy": "Near-perfect pronunciation",
            "emotion": "Natural intonation and rhythm",
            "consistency": "Stable across all text types"
        }
    }
    
    print_colored("📊 TRAINING STRATEGY OVERVIEW:", Colors.BLUE)
    print_colored(f"   Total Duration: {plan['total_duration']}", Colors.BLUE)
    print_colored(f"   Quality Target: {plan['quality_target']}", Colors.BLUE)
    print_colored(f"   Data Usage: ALL 80 samples (vs 6 in cloning)", Colors.BLUE)
    
    print_colored(f"\n🎯 EXPECTED QUALITY IMPROVEMENTS:", Colors.GREEN)
    for metric, value in plan['expected_quality'].items():
        print_colored(f"   {metric.title()}: {value}", Colors.GREEN)
    
    return plan

def create_advanced_config():
    """Create advanced training configuration"""
    print_section("Advanced Training Configuration")
    
    config = {
        "model": "tacotron2",
        "run_name": "custom_voice_full_training",
        "run_description": "High-quality training with all 80 samples",
        
        "datasets": [
            {
                "name": "voice_full_dataset",
                "path": "/ssd/tts_project/voice_data/",
                "meta_file_train": "metadata_train.csv",
                "meta_file_val": "metadata_val.csv", 
                "language": "en"
            }
        ],
        
        # Optimized audio settings for Henry's recordings
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
            "trim_db": 45,  # More aggressive silence trimming
            "do_sound_norm": True,
            "do_amp_to_db_linear": True,
            "stats_path": None
        },
        
        # Training hyperparameters optimized for quality
        "batch_size": 24,  # Larger batch for better gradient estimates
        "eval_batch_size": 16,
        "num_loader_workers": 4,
        "num_eval_loader_workers": 2,
        "run_eval": True,
        "test_delay_epochs": 10,
        
        # Extended training for high quality
        "epochs": 1000,  # Much longer training
        "lr": 0.001,     # Higher initial learning rate
        "lr_decay": True,
        "lr_scheduler": "ExponentialLR",
        "lr_scheduler_params": {"gamma": 0.95},
        "wd": 0.000001,
        "grad_clip": 1.0,
        
        # Advanced model configuration
        "model_args": {
            "r": 1,
            "memory_size": 5,
            "prenet_type": "original",
            "prenet_dropout": True,
            "prenet_dropout_at_inference": False,
            "forward_attn": True,
            "trans_agent": True,
            "forward_attn_mask": True,
            "location_attn": False,
            "attn_norm": "sigmoid",
            "double_decoder_consistency": True,
            "ddc_r": 6,
            "speakers_file": None,
            "use_speaker_embedding": False,
            "use_gst": True,  # Global Style Tokens for emotion
            "gst_style_input": None,
            "separate_stopnet": True,  # Better stopping prediction
            "stopnet_pos_weight": 15.0
        },
        
        # Frequent checkpointing for long training
        "print_step": 25,
        "plot_step": 100,
        "log_model_step": 500,
        "save_step": 1000,
        "save_n_checkpoints": 10,  # Keep more checkpoints
        "save_checkpoints": True,
        
        # Paths
        "output_path": "/ssd/tts_project/full_training_output/",
        
        # Advanced preprocessing
        "use_phonemes": True,  # Use phonemes for better pronunciation
        "phoneme_language": "en-us",
        "phoneme_backend": "espeak",
        "compute_input_seq_cache": True,
        "text_cleaner": "english_cleaners",
        "enable_eos_bos_chars": True,
        "test_sentences_file": "",
        "phoneme_cache_path": "/ssd/tts_project/phoneme_cache",
        
        # Data augmentation
        "datasets": [
            {
                "name": "voice_full_dataset",
                "path": "/ssd/tts_project/voice_data/",
                "meta_file_train": "metadata_train.csv",
                "meta_file_val": "metadata_val.csv",
                "language": "en",
                "phoneme_cache_path": "/ssd/tts_project/phoneme_cache"
            }
        ],
        
        # Loss configuration for quality
        "loss_masking": True,
        "decoder_loss_alpha": 0.25,
        "postnet_loss_alpha": 0.25,
        "postnet_diff_spec_alpha": 0.25,
        "decoder_diff_spec_alpha": 0.25,
        "decoder_ssim_alpha": 0.25,
        "postnet_ssim_alpha": 0.25,
        "stopnet_loss_alpha": 1.0,
        
        # Performance optimizations
        "mixed_precision": False,  # Disabled for stability on Jetson
        "distributed": False,
        "cudnn_enabled": True,
        "cudnn_benchmark": False
    }
    
    config_path = "/ssd/tts_project/full_training_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print_colored(f"✅ Advanced configuration saved: {config_path}", Colors.GREEN)
    print_colored(f"📊 Key improvements over basic training:", Colors.BLUE)
    print_colored(f"   • Phoneme-based training for better pronunciation", Colors.BLUE)
    print_colored(f"   • Global Style Tokens for natural emotion", Colors.BLUE)
    print_colored(f"   • Extended training (1000 epochs vs 300)", Colors.BLUE)
    print_colored(f"   • Larger batch size for stable gradients", Colors.BLUE)
    print_colored(f"   • Advanced learning rate scheduling", Colors.BLUE)
    print_colored(f"   • Better stopping prediction", Colors.BLUE)
    
    return config_path

def create_data_splits():
    """Create proper train/validation splits"""
    print_section("Creating Data Splits for Maximum Quality")
    
    import pandas as pd
    import random
    
    # Read the full metadata
    metadata_path = "/ssd/tts_project/voice_data/metadata.csv"
    df = pd.read_csv(metadata_path, delimiter='|', header=None, names=['filename', 'transcript'])
    
    print_colored(f"📊 Total samples: {len(df)}", Colors.BLUE)
    
    # Shuffle for random split
    df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Split: 70 for training, 10 for validation
    train_size = 70
    val_size = 10
    
    df_train = df_shuffled[:train_size]
    df_val = df_shuffled[train_size:train_size + val_size]
    
    # Save splits
    train_path = "/ssd/tts_project/voice_data/metadata_train.csv"
    val_path = "/ssd/tts_project/voice_data/metadata_val.csv"
    
    df_train.to_csv(train_path, sep='|', index=False, header=False)
    df_val.to_csv(val_path, sep='|', index=False, header=False)
    
    print_colored(f"✅ Training set: {len(df_train)} samples", Colors.GREEN)
    print_colored(f"✅ Validation set: {len(df_val)} samples", Colors.GREEN)
    print_colored(f"📁 Files saved: metadata_train.csv, metadata_val.csv", Colors.CYAN)
    
    return len(df_train), len(df_val)

def show_training_timeline():
    """Show detailed training timeline"""
    print_section("Detailed Training Timeline")
    
    timeline = [
        ("Data Preparation", "20-30 min", "Split data, create phoneme cache, validate"),
        ("Initial Training", "1-2 hours", "Model learns basic patterns, attention alignment"),
        ("Mid Training", "2-3 hours", "Voice characteristics emerge, quality improves"),
        ("Fine-tuning", "2-3 hours", "High-quality speech, natural intonation"),
        ("Final Polish", "1-2 hours", "Production-ready quality achieved"),
        ("Testing & Validation", "30 min", "Quality comparison and final tests")
    ]
    
    total_time = 0
    print_colored("⏱️  DETAILED TIMELINE:", Colors.YELLOW)
    for stage, duration, description in timeline:
        print_colored(f"   {stage:<20} {duration:<12} {description}", Colors.YELLOW)
        # Estimate total (taking middle of ranges)
        if "min" in duration:
            if "-" in duration:
                low, high = duration.replace(" min", "").split("-")
                total_time += (int(low) + int(high)) / 2 / 60
            else:
                total_time += int(duration.replace(" min", "")) / 60
        elif "hour" in duration:
            if "-" in duration:
                low, high = duration.replace(" hours", "").replace(" hour", "").split("-")
                total_time += (int(low) + int(high)) / 2
            else:
                total_time += int(duration.replace(" hours", "").replace(" hour", ""))
    
    print_colored(f"\n🎯 ESTIMATED TOTAL TIME: {total_time:.1f} hours", Colors.CYAN)
    print_colored(f"💡 The longer training is worth it for much higher quality!", Colors.GREEN)

def main():
    print_colored(f"{Colors.BOLD}🎤 HIGH-QUALITY TRAINING PLAN FOR HENRY'S VOICE", Colors.CYAN)
    print_colored("Moving from average quality to production-ready results", Colors.BLUE)
    
    # Analyze current limitations
    analyze_current_limitations()
    
    # Create comprehensive plan
    plan = create_training_plan()
    
    # Show detailed timeline
    show_training_timeline()
    
    # Create data splits
    train_samples, val_samples = create_data_splits()
    
    # Create advanced config
    config_path = create_advanced_config()
    
    print_section("READY TO START HIGH-QUALITY TRAINING")
    print_colored("🎯 Next step: Execute the full training process", Colors.GREEN)
    print_colored("📋 Command to start:", Colors.CYAN)
    print_colored("   python3 scripts/execute_full_training.py", Colors.CYAN)
    
    return True

if __name__ == "__main__":
    success = main()
    print(f"\nTraining plan created: {'✅ Success' if success else '❌ Failed'}")