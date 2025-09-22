#!/usr/bin/env python3
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
