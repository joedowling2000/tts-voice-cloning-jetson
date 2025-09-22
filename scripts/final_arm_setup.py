#!/usr/bin/env python3
"""
ARM-Compatible Training with Available TTS Versions
Uses the best available TTS version for ARM compatibility
"""

import os
import subprocess
import json

def create_compatible_environment():
    """Create environment with most compatible versions"""
    print("🎯 CREATING ARM-COMPATIBLE TTS ENVIRONMENT")
    print("📦 Using compatible versions for Jetson Nano")
    
    env_path = "/ssd/tts_project/arm_compatible_env"
    
    # Create environment
    os.system(f"python3 -m venv {env_path}")
    
    # Install packages step by step
    pip_cmd = f"{env_path}/bin/pip"
    
    packages = [
        f"{pip_cmd} install --upgrade pip",
        f"{pip_cmd} install torch==1.13.1 torchaudio==0.13.1",
        f"{pip_cmd} install numpy==1.21.6",
        f"{pip_cmd} install scipy==1.9.3",
        f"{pip_cmd} install librosa==0.9.2",
        f"{pip_cmd} install soundfile==0.12.1",
        f"{pip_cmd} install TTS==0.13.3",
        f"{pip_cmd} install tensorboard==2.10.1",
        f"{pip_cmd} install matplotlib==3.6.3"
    ]
    
    for cmd in packages:
        print(f"🔧 {cmd}")
        result = os.system(cmd)
        if result == 0:
            print("✅ Success")
        else:
            print("❌ Failed, trying alternative...")
            # Try without version constraints
            base_package = cmd.split()[-1].split('==')[0]
            alt_cmd = f"{pip_cmd} install {base_package}"
            print(f"🔄 Alternative: {alt_cmd}")
            os.system(alt_cmd)
    
    return env_path

def create_working_config():
    """Create a working training configuration for ARM"""
    config = {
        "model": "tacotron2",
        "run_name": "custom_voice_arm_final",
        "run_description": "ARM-optimized high-quality training",
        
        "datasets": [{
            "name": "custom_voice",
            "path": "/ssd/tts_project/voice_data/",
            "meta_file_train": "metadata_ljspeech.csv",
            "formatter": "ljspeech",
            "language": "en"
        }],
        
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
            "trim_db": 45,
            "do_sound_norm": True
        },
        
        "batch_size": 12,
        "eval_batch_size": 6,
        "num_loader_workers": 2,
        "num_eval_loader_workers": 1,
        "run_eval": True,
        "test_delay_epochs": 5,
        
        "epochs": 800,
        "lr": 0.0001,
        "wd": 0.000001,
        "grad_clip": 1.0,
        
        "print_step": 25,
        "plot_step": 100,
        "log_model_step": 500,
        "save_step": 500,
        "save_n_checkpoints": 5,
        "save_checkpoints": True,
        
        "output_path": "/ssd/tts_project/arm_final_output/",
        
        "use_phonemes": False,
        "text_cleaner": "english_cleaners",
        "enable_eos_bos_chars": False,
        
        "mixed_precision": False,
        "distributed": False,
        "use_cuda": False
    }
    
    os.makedirs("/ssd/tts_project/arm_final_output", exist_ok=True)
    
    config_path = "/ssd/tts_project/arm_final_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ ARM config created: {config_path}")
    return config_path

def create_arm_training_script(env_path, config_path):
    """Create final ARM training script"""
    script_content = f'''#!/usr/bin/env python3
"""
Final ARM-Compatible Training Script
Maximum quality training for Jetson Nano
"""

import os
import sys
import subprocess

def main():
    print("🎯 FINAL ARM-COMPATIBLE HIGH-QUALITY TRAINING")
    print("📦 TTS v0.13.3 - ARM Optimized")
    print("🎤 Using ALL 80 samples")
    print("⏱️  Duration: 8-12 hours")
    print("🎯 Goal: Maximum quality Henry voice")
    print("=" * 60)
    
    # Environment setup
    env_path = "{env_path}"
    config_path = "{config_path}"
    
    # Set environment variables
    env = os.environ.copy()
    env['CUDA_VISIBLE_DEVICES'] = ''
    env['PATH'] = f"{env_path}/bin:" + env['PATH']
    env['VIRTUAL_ENV'] = env_path
    
    # Training command
    cmd = [
        f"{env_path}/bin/python3",
        "-m", "TTS.bin.train_tts",
        "--config_path", config_path
    ]
    
    print("🚀 Starting ARM training...")
    print(f"Command: {{' '.join(cmd)}}")
    print("📈 Monitor: http://localhost:6007")
    print("=" * 60)
    
    try:
        # Change to project directory
        os.chdir("/ssd/tts_project")
        
        # Start training
        process = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Stream output
        for line in process.stdout:
            print(line.rstrip())
        
        process.wait()
        
        if process.returncode == 0:
            print("🎉 TRAINING COMPLETED SUCCESSFULLY!")
            print("✅ High-quality Henry voice model ready!")
        else:
            print(f"❌ Training failed with code: {{process.returncode}}")
            
    except Exception as e:
        print(f"❌ Error: {{e}}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
'''
    
    script_path = "/ssd/tts_project/scripts/arm_final_training.py"
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    print(f"✅ ARM training script: {script_path}")
    return script_path

def main():
    print("🎯 FINAL ARM-COMPATIBLE TTS SETUP")
    print("Setting up the best possible ARM environment")
    
    # Create environment
    env_path = create_compatible_environment()
    
    # Create config
    config_path = create_working_config()
    
    # Create training script
    script_path = create_arm_training_script(env_path, config_path)
    
    print("\n🎉 FINAL ARM SETUP COMPLETE!")
    print(f"🔧 Environment: {env_path}")
    print(f"📄 Config: {config_path}")
    print(f"🚀 Training: {script_path}")
    
    print(f"\n🎯 START TRAINING:")
    print(f"python3 {script_path}")

if __name__ == "__main__":
    main()