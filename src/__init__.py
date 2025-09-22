"""
TTS Voice Cloning Framework - Main Package
===========================================

A comprehensive Text-to-Speech voice cloning framework optimized for ARM/Jetson hardware.

This package provides:
- Training utilities and configurations
- Audio processing pipelines  
- Model management and deployment
- Monitoring and validation tools

Usage:
    from tts_framework import training, audio, utils
    
    # Initialize training configuration
    config = training.load_config('configs/voice_config.json')
    
    # Process audio data
    processor = audio.AudioProcessor(config)
    
    # Start training
    trainer = training.VoiceTrainer(config)
    trainer.train()

For detailed documentation, see the docs/ folder.
"""

__version__ = "1.0.0"
__author__ = "TTS Framework Contributors"
__license__ = "MIT"

# Package imports
from . import training
from . import audio  
from . import utils

__all__ = ['training', 'audio', 'utils']