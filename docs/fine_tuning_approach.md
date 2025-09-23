# TTS Model Fine-Tuning Approach

This document outlines a practical fine-tuning strategy for improving a Tacotron2-based TTS voice model that has already reached a baseline quality (loss ≈ 0.3). Rather than simply continuing the initial training with more epochs, this targeted approach uses strategic data collection and a multi-stage fine-tuning process to achieve superior perceptual quality with minimal additional data.

## Table of Contents

- [Goals and Principles](#goals-and-principles)
- [Data Collection Strategy](#data-collection-strategy)
- [Fine-Tuning Configuration](#fine-tuning-configuration)
- [Multi-Stage Fine-Tuning Process](#multi-stage-fine-tuning-process)
- [Quality Evaluation Methods](#quality-evaluation-methods)
- [Expected Outcomes](#expected-outcomes)
- [Implementation Timeline](#implementation-timeline)
- [Code Samples and Resources](#code-samples-and-resources)

## Goals and Principles

### Key Objectives

1. **Improve perceptual voice quality** beyond what the loss metric alone indicates
2. **Address specific weaknesses** in the baseline model
3. **Achieve professional-quality results** with minimal additional data
4. **Preserve the core voice identity** established in the baseline model

### Design Principles

- **Efficiency**: Target improvements with 30-45 minutes of new data instead of many hours
- **Precision**: Focus on addressing specific weaknesses rather than generic training
- **Progressiveness**: Use staged training with gradually decreasing learning rates
- **Evaluation**: Judge quality through perceptual metrics, not just loss values

## Data Collection Strategy

### Required Data Volume: 30-45 Minutes

Create a targeted dataset that specifically addresses the baseline model's weaknesses:

### Data Categories

#### 1. Phonetic Challenge Sentences (10 minutes)
- Sentences with challenging phoneme combinations
- Focus on transitions between vowels and consonants
- Include tongue twisters and phonetically dense sentences

**Example sentences:**
```
"The sixth sick sheik's sixth sheep's sick."
"Peculiar pewter vessels made the medieval craftsman proud."
"Rural jurors rarely rule on judicial reviews."
```

#### 2. Prosody Variation Set (10 minutes)
- Questions with different inflection patterns
- Statements with emphasis on different words
- Commands and exclamations

**Example sentences:**
```
"Are you asking me or telling me?" (curious)
"Are you asking ME or telling me?" (emphatic)
"Are you asking me or TELLING me?" (confrontational)
```

#### 3. Narrative Flow Samples (10-15 minutes)
- Connected paragraphs (not just isolated sentences)
- Natural transitions between ideas
- Varying speech rates within coherent passages

**Example:**
```
"The morning light filtered through the autumn leaves. Golden and red hues 
painted the forest floor, creating a mosaic of color. I walked slowly at 
first, then quickened my pace as I heard the distant sound of running water."
```

#### 4. Edge Case Utterances (5-10 minutes)
- Very short phrases and single words
- Unusually long sentences
- Technical terms and proper names
- Numbers, dates, and special characters

### Recording Guidelines

1. Use **identical recording equipment** and environment as the original dataset
2. Maintain **consistent voice characteristics** (tone, timbre, pace)
3. Record in a **quiet environment** with proper acoustic treatment
4. Maintain **consistent distance** from the microphone
5. Speak with **clear articulation** but natural delivery
6. Record with **higher sample rate** (48kHz) than needed and downsample later
7. Save as **uncompressed WAV** files (16-bit, 22.05kHz for training)

## Fine-Tuning Configuration

Create specialized configuration files for the fine-tuning process. The base configuration should be:

```json
{
  "run_name": "voice_finetuning",
  "run_description": "Fine-tuning from 0.3 loss model with targeted data",
  
  "output_path": "/ssd/tts_project/training_runs/finetune_from_baseline",
  "model": "tacotron2",
  
  "batch_size": 8,
  "eval_batch_size": 8,
  "mixed_precision": true,
  
  "epochs": 300,
  "lr": 0.00005,
  "lr_decay": 0.5,
  "wd": 0.000001,
  "seq_len_norm": true,
  
  "grad_clip": 0.5,
  "scheduler_after_epoch": true,
  
  "run_eval": true,
  "test_delay_epochs": 5,
  "print_eval": true,
  
  "save_step": 5000,
  "checkpoint": true,
  "keep_all_best": false,
  "keep_after": 10000,
  
  "target_loss": "loss",
  "print_step": 25
}
```

## Multi-Stage Fine-Tuning Process

Rather than a single continuous training run, implement a three-stage approach to achieve optimal results:

### Stage 1: Initial Adaptation (50 epochs)

**Purpose**: Help the model adapt to the new data while preserving core voice characteristics

**Key Parameters**:
- Learning rate: 0.00005 (1/4 of original training)
- Data mix: 70% original data, 30% new data

**Script Example**:
```bash
#!/bin/bash
# finetune_stage1.sh

echo "🚀 STARTING STAGE 1 FINE-TUNING: INITIAL ADAPTATION"

# Use the existing best model from the 0.3-loss training
SOURCE_MODEL="/ssd/tts_project/training_runs/henry_v2_stable_20250922_175831/henry_voice_v2_stable-September-22-2025_05+58PM-1d6625a/best_model.pth"

# Use a slightly higher learning rate for initial adaptation
STAGE1_CONFIG="/ssd/tts_project/configs/finetune_stage1_config.json"

# Start training with the new combined dataset
/ssd/tts_project/tts_arm_env/bin/python3 -m TTS.bin.train_tts \
    --config_path $STAGE1_CONFIG \
    --restore_path $SOURCE_MODEL \
    --continue_path /ssd/tts_project/training_runs/finetune_stage1
```

### Stage 2: Targeted Refinement (75 epochs)

**Purpose**: Improve pronunciation of difficult phoneme combinations and refine prosody

**Key Parameters**:
- Learning rate: 0.000025 (1/8 of original)
- Data mix: 50% original data, 50% new data (with emphasis on challenging utterances)

**Script Example**:
```bash
#!/bin/bash
# finetune_stage2.sh

echo "🚀 STARTING STAGE 2 FINE-TUNING: TARGETED REFINEMENT"

# Use the best model from stage 1
SOURCE_MODEL="/ssd/tts_project/training_runs/finetune_stage1/best_model.pth"

# Use a lower learning rate for refined tuning
STAGE2_CONFIG="/ssd/tts_project/configs/finetune_stage2_config.json"

# Continue training with more focus on new data
/ssd/tts_project/tts_arm_env/bin/python3 -m TTS.bin.train_tts \
    --config_path $STAGE2_CONFIG \
    --restore_path $SOURCE_MODEL \
    --continue_path /ssd/tts_project/training_runs/finetune_stage2
```

### Stage 3: Precision Tuning (50 epochs)

**Purpose**: Make precise adjustments for natural prosody and expression

**Key Parameters**:
- Learning rate: 0.00001 (1/20 of original)
- Data mix: 40% original, 40% narrative samples, 20% edge cases

**Script Example**:
```bash
#!/bin/bash
# finetune_stage3.sh

echo "🚀 STARTING STAGE 3 FINE-TUNING: PRECISION TUNING"

# Use the best model from stage 2
SOURCE_MODEL="/ssd/tts_project/training_runs/finetune_stage2/best_model.pth"

# Use a very low learning rate for final precision tuning
STAGE3_CONFIG="/ssd/tts_project/configs/finetune_stage3_config.json"

# Final precision training
/ssd/tts_project/tts_arm_env/bin/python3 -m TTS.bin.train_tts \
    --config_path $STAGE3_CONFIG \
    --restore_path $SOURCE_MODEL \
    --continue_path /ssd/tts_project/training_runs/finetune_stage3
```

## Quality Evaluation Methods

Implement comprehensive evaluation methods that go beyond simple loss metrics:

### Objective Metrics Script

Create an evaluation script that calculates advanced metrics beyond the standard loss:

```python
#!/usr/bin/env python3
"""
Comprehensive TTS Model Quality Evaluation
Beyond simple loss values to perceptual quality metrics
"""

import os
import torch
import numpy as np
import librosa
from TTS.utils.audio import AudioProcessor
from TTS.utils.synthesizer import Synthesizer

def main():
    # Model paths to test - original and fine-tuned versions
    model_paths = [
        "/ssd/tts_project/training_runs/henry_v2_stable_20250922_175831/henry_voice_v2_stable-September-22-2025_05+58PM-1d6625a/best_model.pth",
        "/ssd/tts_project/training_runs/finetune_stage3/best_model.pth"
    ]
    
    # Test sentences focusing on different aspects
    test_sentences = [
        # Simple sentences
        "Welcome to the voice demonstration.",
        # Question intonation
        "Would you like to hear more samples?",
        # Complex phonetics
        "The sixth sick sheik's sixth sheep's sick.",
        # Long sentence flow
        "The morning light filtered through the autumn leaves, creating patterns of shadow and light on the forest floor below.",
        # Technical content
        "The API authentication requires OAuth 2.0 token validation through the REST endpoint."
    ]
    
    # Evaluate each model
    for model_path in model_paths:
        model_name = os.path.basename(os.path.dirname(model_path))
        print(f"\n===== Evaluating Model: {model_name} =====")
        
        # Initialize synthesizer
        synth = Synthesizer(
            model_path,
            config_path=os.path.join(os.path.dirname(model_path), "config.json"),
        )
        
        # Test each sentence
        for idx, sentence in enumerate(test_sentences):
            print(f"\nSentence {idx+1}: {sentence}")
            
            # Generate speech
            outputs = synth.tts(sentence)
            
            # Analyze outputs
            mel = outputs["mel"]
            alignment = outputs["alignment"]
            
            # Calculate advanced metrics
            pitch_stability = analyze_pitch_stability(outputs["wav"])
            phoneme_timing = analyze_phoneme_timing(alignment)
            spectral_clarity = analyze_spectral_clarity(mel)
            
            # Print metrics
            print(f"- Pitch stability: {pitch_stability:.4f}")
            print(f"- Phoneme timing consistency: {phoneme_timing:.4f}")
            print(f"- Spectral clarity: {spectral_clarity:.4f}")
            
            # Save audio for manual comparison
            output_path = f"evaluation_samples/{model_name}_sample{idx+1}.wav"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            synth.save_wav(outputs["wav"], output_path)
            
            print(f"- Saved audio to {output_path}")

# Advanced analysis functions (simplified examples)
def analyze_pitch_stability(audio):
    # Extract pitch and measure stability (lower is better)
    # This is a simplified example - real implementation would be more complex
    pitch, _ = librosa.piptrack(y=audio, sr=22050)
    pitch_mean = np.mean(pitch)
    pitch_std = np.std(pitch)
    return pitch_std / pitch_mean if pitch_mean > 0 else 0

def analyze_phoneme_timing(alignment):
    # Analyze alignment matrix for consistent timing (higher is better)
    # Simplified example
    variance = np.var(np.max(alignment, axis=1))
    return 1.0 / (1.0 + variance)

def analyze_spectral_clarity(mel):
    # Analyze mel spectrogram for clarity (higher is better)
    # Simplified example
    contrast = np.mean(np.abs(mel[:, 1:] - mel[:, :-1]))
    return contrast

if __name__ == "__main__":
    main()
```

### Subjective Listening Tests

Create a simple listening test framework for human evaluation:

1. Generate samples from both the baseline (0.3 loss) model and fine-tuned model
2. Create a blind comparison test where listeners don't know which sample is which
3. Ask evaluators to rate samples on:
   - Naturalness
   - Pronunciation accuracy
   - Appropriate prosody
   - Overall preference

A basic HTML template for these tests is available in the repository.

## Expected Outcomes

With this practical fine-tuning approach using just 30-45 minutes of new data, you can expect:

### Pronunciation Improvements
- Better handling of difficult phoneme combinations
- More consistent pronunciation of technical terms
- Reduced mispronunciations on edge cases

### Natural Prosody
- More natural sentence intonation
- Appropriate emphasis on important words
- Better question and statement differentiation

### Overall Voice Quality
- More consistent voice character
- Smoother transitions between sounds
- Reduced artificial artifacts

### Measurable Metrics
- Loss may improve to 0.35-0.4 (though not to 0.1)
- Alignment error should decrease to 0.5-0.6 range
- Perceptual quality will improve significantly more than loss metrics suggest

## Implementation Timeline

This entire fine-tuning process would take approximately:

1. **Data Collection & Preparation**: 1-2 days
2. **Stage 1 Fine-Tuning**: ~24 hours on Jetson Nano
3. **Stage 2 Fine-Tuning**: ~36 hours on Jetson Nano
4. **Stage 3 Fine-Tuning**: ~24 hours on Jetson Nano
5. **Evaluation & Testing**: 1 day

**Total time**: About 5-7 days, including all preparation and evaluation.

## Code Samples and Resources

### Fine-Tuning Process Checklist

- [ ] Analyze current model weaknesses
  - Systematically test the 0.3-loss model with different sentence types and identify specific weaknesses: difficult phonemes, prosody issues, or sentence-length limitations.
- [ ] Design targeted recording script
  - Create a recording script (150-200 sentences) specifically addressing the identified weaknesses, including: challenging phoneme combinations, varying sentence lengths, and diverse emotional tones.
- [ ] Record new 30-45 minute dataset
  - Record new audio using identical equipment and environment as the original dataset. Focus on consistent delivery while addressing identified weaknesses.
- [ ] Prepare fine-tuning configuration
  - Create a specialized fine-tuning configuration with lower learning rates, targeted training parameters, and appropriate evaluation metrics.
- [ ] Execute multi-stage fine-tuning
  - Implement the three-stage fine-tuning process with progressive learning rate reduction and specialized training focus for each stage.
- [ ] Perform quality evaluations
  - Test model quality after each fine-tuning stage with objective metrics and subjective listening tests to verify improvements.

### Additional Resources

- [Tacotron2 Paper](https://arxiv.org/abs/1712.05884) - Original research on Tacotron2 architecture
- [Mozilla TTS Documentation](https://github.com/mozilla/TTS) - Useful resources for TTS model training
- [Coqui TTS Documentation](https://github.com/coqui-ai/TTS) - Reference for the TTS library used in this project
- [Speech Synthesis Quality Metrics](https://arxiv.org/abs/2103.08023) - Research on evaluating TTS quality beyond loss metrics

---

*This fine-tuning approach is based on extensive research and practical experience with TTS systems. It provides a balanced approach between data efficiency and quality improvements, making it ideal for projects with limited additional recording capabilities.*