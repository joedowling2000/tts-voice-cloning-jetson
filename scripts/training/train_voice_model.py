#!/usr/bin/env python3
"""
Voice Training V2 - Stable Version
Improved training script with comprehensive error handling and logging
"""

import os
import sys
import json
import logging
import shutil
from datetime import datetime
from pathlib import Path

def setup_logging(run_dir):
    """Setup comprehensive logging"""
    log_file = os.path.join(run_dir, "training_v2.log")
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def validate_environment():
    """Validate training environment and dependencies"""
    logger = logging.getLogger(__name__)
    
    # Check TTS installation
    try:
        import TTS
        logger.info(f"✅ TTS version: {TTS.__version__}")
    except ImportError:
        logger.error("❌ TTS not installed")
        return False
    
    # Check data files
    data_path = "/ssd/tts_project/voice_data/processed_audio/"
    if not os.path.exists(data_path):
        logger.error(f"❌ Data path not found: {data_path}")
        return False
    
    # Check metadata
    metadata_file = os.path.join(data_path, "metadata_ljspeech.csv")
    if not os.path.exists(metadata_file):
        logger.error(f"❌ Metadata file not found: {metadata_file}")
        return False
    
    # Count audio files
    wav_files = list(Path(data_path).glob("**/*.wav"))
    logger.info(f"✅ Found {len(wav_files)} audio files")
    
    if len(wav_files) < 50:
        logger.warning(f"⚠️ Only {len(wav_files)} audio files found (recommended: 80+)")
    
    return True

def create_run_directory():
    """Create versioned run directory"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = f"voice_v2_stable_{timestamp}"
    run_dir = f"/ssd/tts_project/training_runs/{run_name}"
    
    os.makedirs(run_dir, exist_ok=True)
    os.makedirs(f"{run_dir}/logs", exist_ok=True)
    os.makedirs(f"{run_dir}/checkpoints", exist_ok=True)
    os.makedirs(f"{run_dir}/plots", exist_ok=True)
    
    return run_dir, run_name

def prepare_config(run_dir):
    """Prepare training configuration"""
    config_template = "/ssd/tts_project/configs/custom_voice_v2_stable.json"
    config_file = os.path.join(run_dir, "config.json")
    
    # Load and modify config
    with open(config_template, 'r') as f:
        config = json.load(f)
    
    # Update output path to use this run directory
    config["output_path"] = run_dir + "/"
    
    # Save config to run directory
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    return config_file

def main():
    """Main training function"""
    print("🎤 HENRY VOICE TRAINING V2 - STABLE")
    print("=" * 50)
    
    # Create run directory
    run_dir, run_name = create_run_directory()
    logger = setup_logging(run_dir)
    
    logger.info(f"🚀 Starting training run: {run_name}")
    logger.info(f"📁 Run directory: {run_dir}")
    
    # Validate environment
    if not validate_environment():
        logger.error("💥 Environment validation failed")
        sys.exit(1)
    
    # Prepare configuration
    config_file = prepare_config(run_dir)
    logger.info(f"📋 Config file: {config_file}")
    
    # Log system info
    logger.info(f"🖥️ Working directory: {os.getcwd()}")
    logger.info(f"🐍 Python version: {sys.version}")
    logger.info(f"📊 CPU count: {os.cpu_count()}")
    
    try:
        # Import TTS after validation
        import torch
        from TTS.bin.train_tts import main as train_main
        
        logger.info(f"🔥 PyTorch version: {torch.__version__}")
        logger.info(f"🎯 CUDA available: {torch.cuda.is_available()}")
        
        # Prepare training arguments
        sys.argv = [
            "train_tts",
            "--config_path", config_file,
            "--restore_path", "",  # Start fresh
            "--use_cuda", "false"  # Jetson Nano compatibility
        ]
        
        logger.info("🏃 Starting TTS training...")
        logger.info(f"📝 Command: {' '.join(sys.argv)}")
        
        # Start training
        train_main()
        
        logger.info("🎉 Training completed successfully!")
        
    except KeyboardInterrupt:
        logger.info("⚠️ Training interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"💥 Training failed: {str(e)}")
        import traceback
        logger.error(f"📋 Traceback: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    main()