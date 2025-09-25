# Running TTS Model on MacBook Air

This guide provides step-by-step instructions for setting up and running your trained TTS model on a MacBook Air (Apple Silicon or Intel).

## Table of Contents
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [File Transfer from Jetson](#file-transfer-from-jetson)
- [Environment Setup](#environment-setup)
- [Model Testing](#model-testing)
- [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)

## System Requirements

### MacBook Air Specifications
- **Apple Silicon (M1/M2)**: Recommended - excellent performance with PyTorch
- **Intel MacBook**: Compatible but slower
- **RAM**: 8GB minimum, 16GB+ recommended
- **Storage**: 10GB free space for environment and models
- **macOS**: 10.15+ (Catalina or later)

### Performance Expectations
- **M1/M2 MacBook Air**: ~10-50x faster inference than Jetson Nano
- **Intel MacBook Air**: ~3-10x faster inference than Jetson Nano
- **Memory Usage**: ~1-2GB during inference (much more efficient than training)

## Installation

### Step 1: Install Homebrew (if not already installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Python 3.10
```bash
# For Apple Silicon Macs
brew install python@3.10

# For Intel Macs
brew install python@3.10
```

### Step 3: Install Audio Dependencies
```bash
# Install system audio libraries
brew install portaudio
brew install ffmpeg
brew install libsndfile
```

### Step 4: Install Python Package Manager
```bash
# Upgrade pip
python3.10 -m pip install --upgrade pip
```

## File Transfer from Jetson

### Required Files to Copy
Create a folder structure and copy these files from your Jetson:

```
tts_model_package/
├── models/
│   ├── best_model.pth              # Latest best model from training
│   └── config.json                 # Model configuration
├── scripts/
│   ├── test_model_mac.py           # MacBook testing script (created below)
│   └── synthesize_text_mac.py      # Text synthesis script (created below)
├── requirements_mac.txt            # MacBook-specific requirements
└── sample_texts.txt                # Test sentences
```

### Files to Copy from Jetson
```bash
# On Jetson, create the package
cd /ssd/tts_project
mkdir -p ~/tts_model_package/{models,scripts}

# Copy the latest model and config
cp training_runs/henry_v2_stable_20250922_175831/henry_voice_v2_stable-September-22-2025_05+58PM-1d6625a/best_model*.pth ~/tts_model_package/models/best_model.pth
cp training_runs/henry_v2_stable_20250922_175831/henry_voice_v2_stable-September-22-2025_05+58PM-1d6625a/config.json ~/tts_model_package/models/

# Copy to OneDrive
cp -r ~/tts_model_package ~/OneDrive/
```

## Environment Setup

### Step 1: Create Virtual Environment
```bash
# Navigate to your downloaded model package
cd ~/Downloads/tts_model_package  # or wherever you downloaded it

# Create virtual environment
python3.10 -m venv tts_mac_env
source tts_mac_env/bin/activate
```

### Step 2: Install TTS Dependencies
Create `requirements_mac.txt`:
```text
torch>=1.13.0
torchaudio>=0.13.0
TTS>=0.13.0
numpy>=1.21.0
scipy>=1.7.0
librosa>=0.9.0
soundfile>=0.10.0
matplotlib>=3.5.0
jupyter>=1.0.0
```

Install dependencies:
```bash
# For Apple Silicon (M1/M2)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install TTS>=0.13.0

# For Intel Macs
pip install torch torchaudio
pip install TTS>=0.13.0

# Install other requirements
pip install -r requirements_mac.txt
```

### Step 3: Verify Installation
```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import TTS; print(f'TTS: {TTS.__version__}')"
python -c "import torchaudio; print('Audio support: OK')"
```

## Model Testing

### Basic Model Test Script
Create `scripts/test_model_mac.py`:
```python
#!/usr/bin/env python3
"""
TTS Model Testing Script for MacBook
Tests model loading and basic functionality
"""

import os
import sys
import torch
import time
import json
from pathlib import Path

# Add TTS to path if needed
try:
    from TTS.utils.synthesizer import Synthesizer
    from TTS.config import load_config
except ImportError:
    print("❌ TTS not found. Please install: pip install TTS>=0.13.0")
    sys.exit(1)

def test_model():
    """Test the TTS model functionality"""
    
    print("🍎 TTS Model Test - MacBook Air")
    print("=" * 50)
    
    # Paths
    model_path = "models/best_model.pth"
    config_path = "models/config.json"
    
    # Check files exist
    if not os.path.exists(model_path):
        print(f"❌ Model not found: {model_path}")
        return False
        
    if not os.path.exists(config_path):
        print(f"❌ Config not found: {config_path}")
        return False
    
    print("✅ Files found")
    print(f"📁 Model: {model_path}")
    print(f"📋 Config: {config_path}")
    
    # Load configuration
    print("\n🔧 Loading configuration...")
    try:
        config = load_config(config_path)
        print(f"✅ Config loaded - Model: {config.model}")
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False
    
    # Initialize synthesizer
    print("\n🚀 Loading model...")
    start_time = time.time()
    
    try:
        synthesizer = Synthesizer(
            model_path=model_path,
            config_path=config_path,
            use_cuda=False  # Use CPU on MacBook
        )
        load_time = time.time() - start_time
        print(f"✅ Model loaded in {load_time:.2f} seconds")
    except Exception as e:
        print(f"❌ Model loading error: {e}")
        return False
    
    # Test synthesis
    print("\n🎵 Testing synthesis...")
    test_texts = [
        "Hello, this is a test of the voice synthesis system.",
        "The MacBook Air provides excellent performance for inference.",
        "How does this voice sound compared to the original?"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Test {i}: {text}")
        
        try:
            start_time = time.time()
            outputs = synthesizer.tts(text)
            synthesis_time = time.time() - start_time
            
            # Save audio file
            output_file = f"test_output_{i}.wav"
            synthesizer.save_wav(outputs["wav"], output_file)
            
            print(f"✅ Generated in {synthesis_time:.2f} seconds")
            print(f"💾 Saved: {output_file}")
            
            # Audio info
            audio_length = len(outputs["wav"]) / synthesizer.output_sample_rate
            print(f"🎵 Audio length: {audio_length:.2f} seconds")
            print(f"📊 Sample rate: {synthesizer.output_sample_rate} Hz")
            
        except Exception as e:
            print(f"❌ Synthesis error: {e}")
            return False
    
    print("\n🎉 All tests completed successfully!")
    print("\n💡 Next steps:")
    print("1. Listen to the generated audio files")
    print("2. Compare quality with original training data")
    print("3. Use synthesize_text_mac.py for custom text")
    
    return True

if __name__ == "__main__":
    success = test_model()
    sys.exit(0 if success else 1)
```

### Interactive Text Synthesis Script
Create `scripts/synthesize_text_mac.py`:
```python
#!/usr/bin/env python3
"""
Interactive TTS Synthesis for MacBook
Generate speech from custom text input
"""

import os
import sys
import time
from pathlib import Path

try:
    from TTS.utils.synthesizer import Synthesizer
except ImportError:
    print("❌ TTS not found. Please install: pip install TTS>=0.13.0")
    sys.exit(1)

class TTSSynthesizer:
    def __init__(self, model_path="models/best_model.pth", config_path="models/config.json"):
        self.model_path = model_path
        self.config_path = config_path
        self.synthesizer = None
        
    def load_model(self):
        """Load the TTS model"""
        print("🚀 Loading TTS model...")
        start_time = time.time()
        
        try:
            self.synthesizer = Synthesizer(
                model_path=self.model_path,
                config_path=self.config_path,
                use_cuda=False
            )
            load_time = time.time() - start_time
            print(f"✅ Model loaded in {load_time:.2f} seconds")
            return True
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def synthesize(self, text, output_file=None):
        """Synthesize text to speech"""
        if not self.synthesizer:
            print("❌ Model not loaded. Call load_model() first.")
            return False
        
        if not output_file:
            # Generate filename from text
            safe_text = "".join(c for c in text[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            output_file = f"output_{safe_text.replace(' ', '_')}.wav"
        
        print(f"\n🎵 Synthesizing: {text}")
        
        try:
            start_time = time.time()
            outputs = self.synthesizer.tts(text)
            synthesis_time = time.time() - start_time
            
            # Save audio
            self.synthesizer.save_wav(outputs["wav"], output_file)
            
            # Statistics
            audio_length = len(outputs["wav"]) / self.synthesizer.output_sample_rate
            rtf = synthesis_time / audio_length  # Real-time factor
            
            print(f"✅ Generated in {synthesis_time:.2f} seconds")
            print(f"💾 Saved: {output_file}")
            print(f"🎵 Audio length: {audio_length:.2f} seconds")
            print(f"⚡ Real-time factor: {rtf:.2f}x")
            
            return True
            
        except Exception as e:
            print(f"❌ Synthesis error: {e}")
            return False

def main():
    print("🍎 TTS Synthesizer - MacBook Air")
    print("=" * 40)
    
    # Initialize synthesizer
    tts = TTSSynthesizer()
    
    if not tts.load_model():
        return 1
    
    print("\n💡 Ready for synthesis!")
    print("Enter text to synthesize (or 'quit' to exit)")
    print("-" * 40)
    
    while True:
        try:
            text = input("\n📝 Enter text: ").strip()
            
            if text.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not text:
                print("Please enter some text.")
                continue
            
            # Synthesize
            tts.synthesize(text)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### Sample Test Texts
Create `sample_texts.txt`:
```text
# Basic test sentences
Hello, this is a test of the voice synthesis system.
The quick brown fox jumps over the lazy dog.
How are you doing today? I hope everything is going well.

# Technical content
The MacBook Air M2 chip provides excellent performance for machine learning inference.
PyTorch and TensorFlow are popular frameworks for deep learning applications.
The model was trained using Tacotron2 architecture with a decoder-postnet structure.

# Challenging phonetics
She sells seashells by the seashore.
Peter Piper picked a peck of pickled peppers.
The sixth sick sheik's sixth sheep's sick.

# Questions and variations
What time is it right now?
Could you please repeat that again?
I'm excited about this new technology!

# Longer passages
The morning light filtered through the autumn leaves, creating a beautiful mosaic of colors on the forest floor. Golden and red hues painted the landscape, while a gentle breeze rustled through the trees. It was the perfect day for a peaceful walk in nature.

Good morning everyone, and welcome to today's presentation. We'll be discussing the latest developments in text-to-speech synthesis, including recent advances in neural network architectures and their practical applications.
```

## Advanced Usage

### Performance Optimization
```bash
# For Apple Silicon Macs - enable Metal Performance Shaders
export PYTORCH_ENABLE_MPS_FALLBACK=1

# Set optimal thread count
export OMP_NUM_THREADS=8  # Adjust based on your CPU cores
```

### Batch Processing Script
Create `scripts/batch_synthesis_mac.py`:
```python
#!/usr/bin/env python3
"""
Batch synthesis script for multiple texts
"""

import os
import sys
from pathlib import Path

try:
    from TTS.utils.synthesizer import Synthesizer
except ImportError:
    print("❌ TTS not found. Please install: pip install TTS>=0.13.0")
    sys.exit(1)

def batch_synthesize(text_file="sample_texts.txt", output_dir="batch_output"):
    """Process multiple texts from a file"""
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Load model
    print("🚀 Loading model...")
    synthesizer = Synthesizer(
        model_path="models/best_model.pth",
        config_path="models/config.json",
        use_cuda=False
    )
    
    # Read texts
    if not os.path.exists(text_file):
        print(f"❌ Text file not found: {text_file}")
        return False
    
    with open(text_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print(f"📝 Processing {len(lines)} texts...")
    
    # Process each text
    for i, text in enumerate(lines, 1):
        print(f"\n🎵 {i}/{len(lines)}: {text[:50]}...")
        
        try:
            outputs = synthesizer.tts(text)
            output_file = os.path.join(output_dir, f"sample_{i:03d}.wav")
            synthesizer.save_wav(outputs["wav"], output_file)
            print(f"✅ Saved: {output_file}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n🎉 Batch processing complete! Check {output_dir}/ folder")
    return True

if __name__ == "__main__":
    batch_synthesize()
```

## Usage Instructions

### Quick Start
```bash
# 1. Activate environment
source tts_mac_env/bin/activate

# 2. Test the model
python scripts/test_model_mac.py

# 3. Interactive synthesis
python scripts/synthesize_text_mac.py

# 4. Batch processing
python scripts/batch_synthesis_mac.py
```

### Command Line Usage
```bash
# Single text synthesis
python -c "
from scripts.synthesize_text_mac import TTSSynthesizer
tts = TTSSynthesizer()
tts.load_model()
tts.synthesize('Your text here', 'output.wav')
"
```

## Troubleshooting

### Common Issues

#### 1. PyTorch/TorchAudio Issues
```bash
# Reinstall PyTorch for your platform
pip uninstall torch torchaudio
# For M1/M2 Mac:
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
# For Intel Mac:
pip install torch torchaudio
```

#### 2. Audio Library Issues
```bash
# Install system dependencies
brew install portaudio libsndfile ffmpeg
pip install soundfile librosa
```

#### 3. Model Loading Errors
- Verify model file is not corrupted during transfer
- Check config.json is valid JSON
- Ensure model and config are from the same training run

#### 4. Memory Issues
```bash
# Monitor memory usage
python -c "
import psutil
print(f'Available RAM: {psutil.virtual_memory().available // (1024**3)} GB')
"
```

### Performance Tips

1. **Apple Silicon Optimization**:
   - Use CPU backend (faster than CUDA emulation)
   - Set `OMP_NUM_THREADS=8` for M1/M2

2. **Memory Management**:
   - Close other applications during synthesis
   - Use batch processing for multiple files

3. **Audio Quality**:
   - Use high-quality speakers/headphones for evaluation
   - Compare with original training audio

### Expected Performance
- **Model Loading**: 2-5 seconds
- **Short Sentence (10 words)**: 0.1-0.5 seconds
- **Long Paragraph (100 words)**: 1-3 seconds
- **Memory Usage**: 1-2 GB during inference

## Comparison with Training Environment

### Performance Improvements
- **Speed**: 10-50x faster than Jetson Nano
- **Memory**: More efficient inference
- **Quality**: Same model quality, better hardware

### File Compatibility
- Models trained on Jetson work identically on Mac
- Config files are fully compatible
- Audio output format matches training environment

---

**Note**: This setup allows you to test and evaluate your models while training continues uninterrupted on the Jetson. The same model files work identically across both platforms.