"""
Training Module - TTS Voice Cloning Framework
==============================================

Core training functionality for voice cloning models.

This module provides:
- Training loop management
- Configuration handling
- Checkpoint management
- Progress monitoring
- Loss calculation and optimization

Classes:
    VoiceTrainer: Main training coordinator
    TrainingConfig: Configuration management
    CheckpointManager: Model checkpoint handling
"""

from .trainer import VoiceTrainer
from .config import TrainingConfig
from .checkpoints import CheckpointManager

__all__ = ['VoiceTrainer', 'TrainingConfig', 'CheckpointManager']