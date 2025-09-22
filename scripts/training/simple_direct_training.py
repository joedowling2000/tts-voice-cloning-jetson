#!/usr/bin/env python3
"""
Simple direct training using TTS library
Bypasses complex imports by using basic trainer
"""

import os
import json
from pathlib import Path

def create_simple_config():
    """Create minimal working config"""
    config = {
        "model": "tacotron2",
        "run_name": "custom_voice_simple",
        
        "datasets": [{
            "name": "custom_voice",
            "path": "/ssd/tts_project/voice_data/",
            "meta_file_train": "metadata_ljspeech.csv",
            "formatter": "ljspeech"
        }],
        
        "audio": {
            "sample_rate": 22050,
            "hop_length": 256,
            "win_length": 1024,
            "n_fft": 1024,
            "n_mels": 80
        },
        
        "batch_size": 8,
        "eval_batch_size": 4,
        "epochs": 200,
        "lr": 0.0001,
        "output_path": "/ssd/tts_project/simple_training/",
        "print_step": 10,
        "save_step": 100
    }
    
    os.makedirs("/ssd/tts_project/simple_training", exist_ok=True)
    config_path = "/ssd/tts_project/simple_config.json"
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    return config_path

def main():
    print("🎯 CREATING SIMPLE TRAINING SETUP")
    
    # Create config
    config_path = create_simple_config()
    print(f"✅ Config: {config_path}")
    
    # Show training command
    cmd = f"""
cd /ssd/tts_project
source coqui_env/bin/activate
export CUDA_VISIBLE_DEVICES=0
python3 -c "
import sys
sys.path.insert(0, '/ssd/tts_project/coqui_env/lib/python3.10/site-packages')

try:
    from TTS.bin.train_tts import main as train_main
    import argparse
    
    # Mock args
    class Args:
        config_path = '{config_path}'
        restore_path = None
        best_path = None
        continue_path = None
        rank = 0
        group_id = ''
    
    # Start training
    print('🚀 Starting training...')
    train_main(Args())
    
except Exception as e:
    print(f'❌ Error: {{e}}')
    import traceback
    traceback.print_exc()
"
"""
    
    print(f"\n🚀 TRAINING COMMAND:")
    print(cmd)
    
    print(f"\n📊 Or run directly:")
    print(f"cd /ssd/tts_project")
    print(f"source coqui_env/bin/activate")
    print(f"python3 -m TTS.bin.train_tts --config_path {config_path}")

if __name__ == "__main__":
    main()