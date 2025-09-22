#!/usr/bin/env python3
"""
Resume Henry Voice Training from Latest Checkpoint
Auto-detects the latest checkpoint and continues training
"""

import os
import sys
import logging
import glob
from datetime import datetime

# Add the project root to Python path
sys.path.append('/ssd/tts_project')

def find_latest_checkpoint():
    """Find the latest checkpoint file"""
    checkpoint_pattern = "/ssd/tts_project/training_runs/voice_v2_stable_20250922_170150/custom_voice_v2_stable-September-22-2025_05+01PM-0000000/best_model_*.pth"
    checkpoints = glob.glob(checkpoint_pattern)
    
    if not checkpoints:
        return None
    
    # Sort by modification time to get the latest
    latest_checkpoint = max(checkpoints, key=os.path.getmtime)
    return latest_checkpoint

def main():
    print("🔄 RESUMING HENRY VOICE TRAINING")
    print("=" * 50)
    
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    # Change to project directory
    os.chdir('/ssd/tts_project')
    
    # Find latest checkpoint
    latest_checkpoint = find_latest_checkpoint()
    
    if latest_checkpoint:
        print(f"📁 Found checkpoint: {os.path.basename(latest_checkpoint)}")
        logger.info(f"Resuming from checkpoint: {latest_checkpoint}")
    else:
        print("⚠️ No checkpoint found, starting fresh")
        latest_checkpoint = ""
    
    # Training configuration
    config_path = "/ssd/tts_project/training_runs/voice_v2_stable_20250922_170150/config.json"
    
    print(f"📋 Config: {config_path}")
    print(f"🎯 Target: 1000 epochs for maximum quality")
    print(f"⏰ Estimated time: ~150 hours (6 days)")
    print(f"🖥️ Working directory: {os.getcwd()}")
    print(f"🐍 Python: {sys.executable}")
    print("")
    
    # Validate files exist
    if not os.path.exists(config_path):
        logger.error(f"Config file not found: {config_path}")
        return False
    
    if latest_checkpoint and not os.path.exists(latest_checkpoint):
        logger.error(f"Checkpoint file not found: {latest_checkpoint}")
        return False
    
    print("🚀 Starting TTS training...")
    
    # Import TTS after setting up environment
    try:
        from TTS.bin.train_tts import main as train_main
        
        # Prepare arguments for TTS training
        sys.argv = [
            'train_tts',
            '--config_path', config_path,
            '--restore_path', latest_checkpoint if latest_checkpoint else '',
            '--use_cuda', 'false'
        ]
        
        # Start training
        train_main()
        
    except Exception as e:
        logger.error(f"Training failed: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("✅ Training completed successfully!")
    else:
        print("❌ Training failed!")
        sys.exit(1)