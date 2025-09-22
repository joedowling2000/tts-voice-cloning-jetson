#!/usr/bin/env python3
"""
Quick ARM-Compatible TTS Setup
Uses TTS v0.6.2 - the most ARM-stable version available
"""

import os
import subprocess

def setup_simple_arm_tts():
    """Set up the most compatible TTS version"""
    print("🎯 QUICK ARM-COMPATIBLE TTS SETUP")
    print("📦 Using TTS v0.6.2 - Maximum ARM compatibility")
    print("=" * 50)
    
    # Create simple environment
    env_path = "/ssd/tts_project/simple_tts_env"
    
    commands = [
        f"python3 -m venv {env_path}",
        f"{env_path}/bin/pip install --upgrade pip",
        f"{env_path}/bin/pip install torch==1.9.0 torchaudio==0.9.0",
        f"{env_path}/bin/pip install TTS==0.6.2",
        f"{env_path}/bin/pip install numpy scipy librosa soundfile tensorboard matplotlib",
        f"{env_path}/bin/pip install inflect unidecode phonemizer"
    ]
    
    for cmd in commands:
        print(f"🔧 Running: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Success")
        else:
            print(f"❌ Error: {result.stderr}")
            
    print("\n✅ Simple ARM TTS environment ready!")
    print(f"📁 Location: {env_path}")
    
    return env_path

def create_simple_training_config():
    """Create a simple, working training configuration"""
    config = {
        "model": "tacotron2",
        "run_name": "henry_voice_simple_arm",
        
        "datasets": [{
            "name": "henry_voice",
            "path": "/ssd/tts_project/voice_data/",
            "meta_file_train": "metadata_ljspeech.csv",
            "formatter": "ljspeech"
        }],
        
        "audio": {
            "sample_rate": 22050,
            "hop_length": 256,
            "win_length": 1024,
            "n_fft": 1024,
            "n_mels": 80,
            "fmin": 0,
            "fmax": 8000
        },
        
        "batch_size": 8,
        "eval_batch_size": 4,
        "epochs": 500,
        "lr": 0.0001,
        "output_path": "/ssd/tts_project/simple_arm_output/",
        "print_step": 25,
        "save_step": 500
    }
    
    os.makedirs("/ssd/tts_project/simple_arm_output", exist_ok=True)
    
    import json
    config_path = "/ssd/tts_project/simple_arm_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Simple config created: {config_path}")
    return config_path

def create_simple_training_script():
    """Create the simplest possible training script"""
    script_content = '''#!/usr/bin/env python3
"""
Simple ARM Training Script using TTS v0.6.2
"""

import os
import sys

def main():
    print("🎯 SIMPLE ARM TRAINING")
    print("📦 Using TTS v0.6.2 for maximum compatibility")
    print("🎤 Training with all 80 samples")
    
    # Simple training command
    cmd = """
cd /ssd/tts_project
source simple_tts_env/bin/activate
export PYTHONPATH=/ssd/tts_project/simple_tts_env/lib/python3.10/site-packages:$PYTHONPATH

python3 -c "
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''

try:
    from TTS.bin.train_tts import main
    import sys
    
    # Set up args
    sys.argv = [
        'train_tts',
        '--config_path', '/ssd/tts_project/simple_arm_config.json'
    ]
    
    print('🚀 Starting simple ARM training...')
    main()
    
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
"
"""
    
    print("🚀 TRAINING COMMAND:")
    print(cmd)
    
    # Execute directly
    os.system(cmd)

if __name__ == "__main__":
    main()
'''
    
    script_path = "/ssd/tts_project/scripts/simple_arm_training.py"
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    print(f"✅ Simple training script: {script_path}")
    return script_path

def main():
    print("🎯 SETTING UP SIMPLEST ARM-COMPATIBLE TTS")
    
    # Setup environment
    env_path = setup_simple_arm_tts()
    
    # Create config
    config_path = create_simple_training_config()
    
    # Create script
    script_path = create_simple_training_script()
    
    print("\n🎉 SIMPLE ARM SETUP COMPLETE!")
    print(f"🔧 Run: python3 {script_path}")

if __name__ == "__main__":
    main()