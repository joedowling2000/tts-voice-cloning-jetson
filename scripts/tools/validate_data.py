#!/usr/bin/env python3
"""
TTS Training Data Validation Script
Validates audio files and metadata for training readiness
"""

import os
import pandas as pd
import soundfile as sf
import numpy as np
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
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 50}")
    print(f"📊 {title}")
    print(f"{'=' * 50}{Colors.END}")

def validate_metadata(metadata_path):
    """Validate metadata.csv file"""
    print_section("Validating Metadata File")
    
    if not os.path.exists(metadata_path):
        print_colored("❌ metadata.csv not found!", Colors.RED)
        return False, None
    
    try:
        df = pd.read_csv(metadata_path, delimiter='|', header=None, names=['filename', 'transcript'])
        print_colored(f"✅ Metadata file loaded successfully", Colors.GREEN)
        print_colored(f"📄 Total entries: {len(df)}", Colors.BLUE)
        
        # Check for empty transcripts
        empty_transcripts = df[df['transcript'].isna() | (df['transcript'].str.strip() == '')]
        if len(empty_transcripts) > 0:
            print_colored(f"⚠️  Warning: {len(empty_transcripts)} entries have empty transcripts", Colors.YELLOW)
        
        # Check transcript lengths
        transcript_lengths = df['transcript'].str.len()
        print_colored(f"📊 Transcript length stats:", Colors.BLUE)
        print_colored(f"   Average: {transcript_lengths.mean():.1f} characters", Colors.BLUE)
        print_colored(f"   Min: {transcript_lengths.min()} characters", Colors.BLUE)
        print_colored(f"   Max: {transcript_lengths.max()} characters", Colors.BLUE)
        
        return True, df
    except Exception as e:
        print_colored(f"❌ Error reading metadata: {str(e)}", Colors.RED)
        return False, None

def validate_audio_files(df, audio_dir):
    """Validate audio files"""
    print_section("Validating Audio Files")
    
    if not os.path.exists(audio_dir):
        print_colored(f"❌ Audio directory not found: {audio_dir}", Colors.RED)
        return False
    
    audio_files = list(Path(audio_dir).glob("*.wav"))
    print_colored(f"📁 Found {len(audio_files)} audio files", Colors.BLUE)
    
    missing_files = []
    invalid_files = []
    durations = []
    sample_rates = []
    
    for idx, row in df.iterrows():
        filename = row['filename']
        audio_path = os.path.join(audio_dir, filename)
        
        if not os.path.exists(audio_path):
            missing_files.append(filename)
            continue
        
        try:
            # Load audio file and check properties
            data, sr = sf.read(audio_path)
            duration = len(data) / sr
            durations.append(duration)
            sample_rates.append(sr)
            
            # Check for extremely short or long files
            if duration < 1.0:
                print_colored(f"⚠️  Warning: {filename} is very short ({duration:.2f}s)", Colors.YELLOW)
            elif duration > 15.0:
                print_colored(f"⚠️  Warning: {filename} is very long ({duration:.2f}s)", Colors.YELLOW)
                
        except Exception as e:
            invalid_files.append((filename, str(e)))
    
    # Report results
    if missing_files:
        print_colored(f"❌ Missing audio files ({len(missing_files)}):", Colors.RED)
        for f in missing_files[:5]:  # Show first 5
            print_colored(f"   - {f}", Colors.RED)
        if len(missing_files) > 5:
            print_colored(f"   ... and {len(missing_files) - 5} more", Colors.RED)
    
    if invalid_files:
        print_colored(f"❌ Invalid audio files ({len(invalid_files)}):", Colors.RED)
        for f, error in invalid_files[:5]:  # Show first 5
            print_colored(f"   - {f}: {error}", Colors.RED)
    
    if durations:
        print_colored(f"📊 Audio duration stats:", Colors.BLUE)
        print_colored(f"   Total duration: {sum(durations)/60:.1f} minutes", Colors.BLUE)
        print_colored(f"   Average: {np.mean(durations):.2f} seconds", Colors.BLUE)
        print_colored(f"   Min: {min(durations):.2f} seconds", Colors.BLUE)
        print_colored(f"   Max: {max(durations):.2f} seconds", Colors.BLUE)
        
        # Check sample rates
        unique_srs = set(sample_rates)
        if len(unique_srs) == 1:
            print_colored(f"✅ All files have consistent sample rate: {list(unique_srs)[0]} Hz", Colors.GREEN)
        else:
            print_colored(f"⚠️  Warning: Multiple sample rates found: {unique_srs}", Colors.YELLOW)
    
    success = len(missing_files) == 0 and len(invalid_files) == 0
    return success

def validate_training_readiness(df, audio_dir):
    """Check if data is ready for training"""
    print_section("Training Readiness Assessment")
    
    issues = []
    warnings = []
    
    # Check minimum data requirements
    if len(df) < 50:
        issues.append(f"Insufficient data: {len(df)} samples (recommend 100+ for good results)")
    elif len(df) < 100:
        warnings.append(f"Limited data: {len(df)} samples (more data = better results)")
    else:
        print_colored(f"✅ Good data volume: {len(df)} samples", Colors.GREEN)
    
    # Check audio quality requirements
    audio_files = list(Path(audio_dir).glob("*.wav"))
    if len(audio_files) == len(df):
        print_colored("✅ All metadata entries have corresponding audio files", Colors.GREEN)
    else:
        issues.append(f"Mismatch: {len(df)} metadata entries vs {len(audio_files)} audio files")
    
    # Check for duplicate transcripts (might indicate poor data quality)
    duplicate_transcripts = df[df.duplicated('transcript', keep=False)]
    if len(duplicate_transcripts) > 0:
        warnings.append(f"{len(duplicate_transcripts)} duplicate transcripts found")
    
    # Report final assessment
    if issues:
        print_colored("❌ Training readiness: NOT READY", Colors.RED)
        for issue in issues:
            print_colored(f"   - {issue}", Colors.RED)
    elif warnings:
        print_colored("⚠️  Training readiness: READY WITH WARNINGS", Colors.YELLOW)
        for warning in warnings:
            print_colored(f"   - {warning}", Colors.YELLOW)
    else:
        print_colored("✅ Training readiness: READY TO TRAIN!", Colors.GREEN)
    
    return len(issues) == 0

def main():
    print_colored(f"{Colors.BOLD}🔍 TTS Training Data Validation", Colors.CYAN)
    print_colored(f"Validating data for Coqui TTS training", Colors.CYAN)
    
    # Paths
    project_dir = "/ssd/tts_project"
    metadata_path = os.path.join(project_dir, "voice_data", "metadata.csv")
    audio_dir = os.path.join(project_dir, "voice_data", "processed_audio")
    
    # Validate metadata
    metadata_valid, df = validate_metadata(metadata_path)
    if not metadata_valid:
        print_colored("\n❌ Validation failed at metadata stage", Colors.RED)
        return False
    
    # Validate audio files
    audio_valid = validate_audio_files(df, audio_dir)
    if not audio_valid:
        print_colored("\n❌ Validation failed at audio stage", Colors.RED)
        return False
    
    # Check training readiness
    ready_to_train = validate_training_readiness(df, audio_dir)
    
    print_section("Validation Summary")
    if ready_to_train:
        print_colored("🎉 All validation checks passed!", Colors.GREEN)
        print_colored("Your data is ready for TTS model training!", Colors.GREEN)
    else:
        print_colored("⚠️  Some issues need to be addressed before training", Colors.YELLOW)
    
    return ready_to_train

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)