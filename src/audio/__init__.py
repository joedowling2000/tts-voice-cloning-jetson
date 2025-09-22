"""
Audio Processing Module - TTS Voice Cloning Framework
======================================================

Audio processing and feature extraction utilities.

This module provides:
- Audio preprocessing and normalization
- Mel spectrogram generation
- Audio format conversion
- Quality validation
- Feature extraction for training

Classes:
    AudioProcessor: Main audio processing pipeline
    SpectrogramGenerator: Mel spectrogram creation
    AudioValidator: Quality checking utilities
"""

from .processor import AudioProcessor
from .spectrograms import SpectrogramGenerator
from .validator import AudioValidator

__all__ = ['AudioProcessor', 'SpectrogramGenerator', 'AudioValidator']