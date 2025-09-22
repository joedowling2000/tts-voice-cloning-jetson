#!/usr/bin/env python3
"""
TTS Training Auto-Save & Model Output Guide
Complete reference for where models are saved and formats
"""

import os
import json
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_colored(message, color):
    print(f"{color}{message}{Colors.END}")

def print_header(title):
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 80}")
    print(f"📁 {title}")
    print(f"{'=' * 80}{Colors.END}")

def show_auto_save_config():
    """Show the auto-save configuration"""
    print_header("AUTO-SAVE CONFIGURATION")
    
    config_path = "/ssd/tts_project/arm_max_quality_config.json"
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    print_colored("🔧 SAVE SETTINGS:", Colors.BLUE)
    print_colored(f"   save_step: {config.get('save_step', 'N/A')} steps", Colors.GREEN)
    print_colored(f"   save_checkpoints: {config.get('save_checkpoints', 'N/A')}", Colors.GREEN)
    print_colored(f"   save_n_checkpoints: {config.get('save_n_checkpoints', 'N/A')} files kept", Colors.GREEN)
    print_colored(f"   save_best_after: {config.get('save_best_after', 'N/A')} steps", Colors.GREEN)
    
    print_colored("\n📅 SAVE FREQUENCY:", Colors.YELLOW)
    print_colored(f"   ✅ Every {config.get('save_step', 1000)} training steps", Colors.YELLOW)
    print_colored(f"   ✅ Keep latest {config.get('save_n_checkpoints', 10)} checkpoints", Colors.YELLOW)
    print_colored(f"   ✅ Save best model after step {config.get('save_best_after', 10000)}", Colors.YELLOW)

def show_output_locations():
    """Show where models will be saved"""
    print_header("MODEL SAVE LOCATIONS")
    
    base_output = "/ssd/tts_project/arm_max_quality_output"
    
    # Find current training run
    if os.path.exists(base_output):
        run_dirs = [d for d in os.listdir(base_output) 
                   if os.path.isdir(os.path.join(base_output, d)) and 'henry_voice' in d]
        
        if run_dirs:
            current_run = sorted(run_dirs)[-1]
            run_path = os.path.join(base_output, current_run)
            
            print_colored("📂 CURRENT TRAINING RUN:", Colors.CYAN)
            print_colored(f"   {run_path}", Colors.GREEN)
            
            print_colored("\n📄 FILES IN TRAINING DIRECTORY:", Colors.BLUE)
            if os.path.exists(run_path):
                for item in sorted(os.listdir(run_path)):
                    item_path = os.path.join(run_path, item)
                    if os.path.isfile(item_path):
                        size = os.path.getsize(item_path)
                        print_colored(f"   {item} ({size:,} bytes)", Colors.GREEN)

def show_model_formats():
    """Show model file formats and naming"""
    print_header("MODEL FILE FORMATS & NAMING")
    
    print_colored("🎯 CHECKPOINT FILES (.pth):", Colors.BLUE)
    print_colored("   checkpoint_XXXXX.pth - Training checkpoints every 1000 steps", Colors.GREEN)
    print_colored("   best_model.pth - Best performing model (lowest loss)", Colors.GREEN)
    print_colored("   Format: PyTorch state dictionary", Colors.YELLOW)
    
    print_colored("\n🔧 CONFIG FILES:", Colors.BLUE)
    print_colored("   config.json - Complete training configuration", Colors.GREEN)
    print_colored("   Format: JSON", Colors.YELLOW)
    
    print_colored("\n📊 TRAINING LOGS:", Colors.BLUE)
    print_colored("   trainer_0_log.txt - Training progress log", Colors.GREEN)
    print_colored("   events.out.tfevents.* - TensorBoard logs", Colors.GREEN)
    print_colored("   Format: Text / TensorBoard binary", Colors.YELLOW)
    
    print_colored("\n🎤 FINAL MODEL FILES:", Colors.MAGENTA)
    print_colored("   best_model.pth - Main model file (PyTorch)", Colors.GREEN)
    print_colored("   config.json - Model configuration", Colors.GREEN)
    print_colored("   speakers.json - Speaker info (if applicable)", Colors.GREEN)

def show_usage_info():
    """Show how to use the trained models"""
    print_header("USING THE TRAINED MODELS")
    
    print_colored("🚀 LOADING TRAINED MODEL:", Colors.BLUE)
    
    usage_code = '''
# Load the trained Henry voice model
from TTS.api import TTS

# Path to your trained model
model_path = "/ssd/tts_project/arm_max_quality_output/henry_voice_arm_max_quality-September-21-2025_08+24PM-0000000/best_model.pth"
config_path = "/ssd/tts_project/arm_max_quality_output/henry_voice_arm_max_quality-September-21-2025_08+24PM-0000000/config.json"

# Initialize TTS with your model
tts = TTS(model_path=model_path, config_path=config_path)

# Generate speech
text = "Hello, this is Henry speaking with the new high-quality voice model."
tts.tts_to_file(text=text, file_path="henry_output.wav")
'''
    
    print_colored(usage_code, Colors.GREEN)
    
    print_colored("\n📁 FILE STRUCTURE AFTER TRAINING:", Colors.YELLOW)
    structure = '''
/ssd/tts_project/arm_max_quality_output/
└── henry_voice_arm_max_quality-September-21-2025_08+24PM-0000000/
    ├── best_model.pth          # 🎯 MAIN MODEL FILE
    ├── checkpoint_1000.pth     # Checkpoint at step 1000
    ├── checkpoint_2000.pth     # Checkpoint at step 2000
    ├── checkpoint_3000.pth     # Checkpoint at step 3000
    ├── ...                     # More checkpoints
    ├── config.json             # 🔧 MODEL CONFIGURATION
    ├── trainer_0_log.txt       # 📋 Training log
    └── events.out.tfevents.*   # 📊 TensorBoard data
'''
    print_colored(structure, Colors.CYAN)

def check_current_progress():
    """Check current training progress and files"""
    print_header("CURRENT TRAINING STATUS")
    
    base_output = "/ssd/tts_project/arm_max_quality_output"
    
    if os.path.exists(base_output):
        run_dirs = [d for d in os.listdir(base_output) 
                   if os.path.isdir(os.path.join(base_output, d)) and 'henry_voice' in d]
        
        if run_dirs:
            current_run = sorted(run_dirs)[-1]
            run_path = os.path.join(base_output, current_run)
            
            # Check for model files
            checkpoints = [f for f in os.listdir(run_path) if f.endswith('.pth')]
            
            print_colored(f"📂 Training Directory: {current_run}", Colors.CYAN)
            print_colored(f"🔢 Checkpoint Files: {len(checkpoints)}", Colors.GREEN)
            
            if checkpoints:
                print_colored("📄 Current Checkpoints:", Colors.BLUE)
                for cp in sorted(checkpoints):
                    cp_path = os.path.join(run_path, cp)
                    size = os.path.getsize(cp_path)
                    mtime = datetime.fromtimestamp(os.path.getmtime(cp_path))
                    print_colored(f"   {cp} ({size:,} bytes) - {mtime}", Colors.GREEN)
            else:
                print_colored("⏳ No checkpoints yet (saves every 1000 steps)", Colors.YELLOW)

def main():
    print_colored("🎤 TTS TRAINING AUTO-SAVE & MODEL OUTPUT GUIDE", Colors.MAGENTA)
    
    show_auto_save_config()
    show_output_locations()
    show_model_formats()
    show_usage_info()
    check_current_progress()
    
    print_header("SUMMARY")
    print_colored("✅ Models auto-save every 1000 steps", Colors.GREEN)
    print_colored("✅ Best model saved as 'best_model.pth'", Colors.GREEN)
    print_colored("✅ Format: PyTorch (.pth) + JSON config", Colors.GREEN)
    print_colored("✅ Location: /ssd/tts_project/arm_max_quality_output/", Colors.GREEN)
    print_colored("✅ Ready to use with TTS.api for speech synthesis", Colors.GREEN)

if __name__ == "__main__":
    main()