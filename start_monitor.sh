#!/bin/bash

# TTS Training Monitor Launcher
# Easy way to start the training monitor

echo "🎤 Starting TTS Training Monitor..."
echo "This will show real-time training progress in a separate terminal"
echo "Press Ctrl+C to exit the monitor (training will continue)"
echo ""

cd /ssd/tts_project
python3 scripts/monitor_training.py