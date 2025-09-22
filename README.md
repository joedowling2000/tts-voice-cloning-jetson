# Henry Voice TTS Training Project

A comprehensive Text-to-Speech (TTS) voice cloning project using Coqui TTS on ARM/Jetson Nano hardware.

## 🎯 Project Overview

This project implements high-quality voice cloning using the Tacotron2 model, specifically optimized for ARM-based systems like the Jetson Nano. The setup includes robust training scripts, monitoring tools, and production-ready configurations.

## 🛠️ Technical Stack

- **TTS Framework:** Coqui TTS v0.13.3
- **Model:** Tacotron2-DDC with guided attention
- **Hardware:** ARM/Jetson Nano optimized
- **Python:** 3.10+ with PyTorch 1.13.1
- **Monitoring:** TensorBoard integration

## 📁 Project Structure

```
tts-voice-cloning-jetson/
├── README.md                           # Main documentation
├── .gitignore                         # Privacy protection
├── configs/                           # Configuration files
│   ├── henry_voice_v2_stable.json    # Production ARM config
│   ├── arm_max_quality_config.json   # Quality-optimized settings
│   └── training_config.json          # Base training configuration
├── scripts/                          # Executable scripts
│   ├── training/                     # Training automation
│   │   ├── train_henry_v2_stable.py # Main training script
│   │   └── resume_training.py       # Resume from checkpoint
│   ├── tools/                        # Data processing utilities
│   │   ├── process_audio.py         # Audio preprocessing
│   │   ├── create_metadata.py       # Metadata generation
│   │   └── validate_data.py         # Data validation
│   └── monitoring/                   # Training monitoring
│       ├── monitor_training.py      # Real-time monitoring
│       └── quick_status.sh          # Status checking
├── shells/                           # Shell automation
│   ├── monitor_training.sh          # Training monitoring
│   └── workflow_summary.sh          # Project workflows
└── docs/                             # Documentation
    ├── training_version_control.md  # Version control guide
    └── project_structure.md         # Architecture overview
```

> **Note:** This project prioritizes clean organization and privacy protection. All voice data and trained models are excluded from version control.

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Create virtual environment
python3 -m venv tts_arm_env
source tts_arm_env/bin/activate

# Install dependencies
pip install torch==1.13.1 torchaudio==0.13.1
pip install TTS==0.13.3
pip install pydantic<2.0 inflect==5.6.0
```

### 2. Data Preparation
```bash
# Process audio files
python scripts/process_audio.py

# Create metadata
python scripts/create_metadata.py

# Validate data
python scripts/validate_data.py
```

### 3. Training
```bash
# Start training with monitoring
python scripts/train_henry_v2_stable.py

# Monitor with TensorBoard
tensorboard --logdir=training_runs --port=6006
```

## ⚙️ Configuration Features

### ARM Optimization
- **Batch Size:** Optimized for ARM memory constraints
- **CPU Threading:** Efficient multi-core utilization
- **Memory Management:** Reduced memory footprint

### Training Stability
- **Guided Attention:** Improved text-audio alignment
- **Stopnet Enhancement:** Better sequence termination
- **Learning Rate:** Stable convergence settings
- **Loss Functions:** Balanced multi-objective training

### Quality Features
- **High Sample Rate:** 22050 Hz for clarity
- **Mel Spectrograms:** 80-channel feature extraction
- **Audio Processing:** Advanced normalization and trimming
- **Validation:** Real-time quality monitoring

## 📊 Monitoring

### TensorBoard Metrics
- Training/validation loss curves
- Audio sample generation
- Attention alignment visualization
- Learning rate scheduling

### Log Analysis
- Detailed training logs
- Performance metrics
- Error tracking
- Progress indicators

## 🔧 Advanced Features

### Version Control
- Automated run naming with timestamps
- Git integration for reproducibility
- Checkpoint management
- Configuration versioning

### Robustness
- Background training with nohup
- Automatic error recovery
- Resource monitoring
- Graceful interruption handling

## 📈 Expected Results

### Training Progression
- **Epoch 50-100:** Basic intelligible speech
- **Epoch 200:** Clear, recognizable voice
- **Epoch 500:** Natural-sounding speech
- **Epoch 800+:** Professional-grade voice cloning

### Performance Targets
- **Total Loss:** < 1.0 for production quality
- **Alignment Error:** < 0.2 for stable generation
- **Training Time:** ~150 hours for 1000 epochs on Jetson Nano

## 🛡️ Privacy & Security

This repository contains only:
- ✅ Configuration files
- ✅ Training scripts
- ✅ Documentation
- ✅ Utility tools

**Excluded for privacy:**
- ❌ Voice recordings
- ❌ Trained models
- ❌ Personal audio data
- ❌ Training outputs

## 📝 License

This project is for educational and research purposes. Please respect voice cloning ethics and obtain proper consent for any voice data used.

## 🤝 Contributing

Feel free to contribute improvements to:
- ARM optimization techniques
- Training efficiency
- Configuration management
- Documentation

## 📞 Support

For issues related to:
- Jetson Nano setup: Check hardware compatibility
- Training problems: Review logs and configurations
- Performance: Monitor system resources

---

**Note:** This is a privacy-conscious repository. No personal voice data or trained models are included.