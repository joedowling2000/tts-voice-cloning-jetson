#!/bin/bash
"""
Simple Training Progress Commands
Quick ways to check training status
"""

echo "🎤 TTS TRAINING PROGRESS CHECKER"
echo "=================================="

echo ""
echo "📊 TRAINING PROCESS STATUS:"
ps aux | grep train_tts | grep -v grep

echo ""
echo "📈 LATEST TRAINING LOG (last 10 lines):"
tail -10 /ssd/tts_project/training_progress.log

echo ""
echo "🏃 CURRENT TRAINING STEP/EPOCH:"
grep -E "(EPOCH|STEP)" /ssd/tts_project/training_progress.log | tail -3

echo ""
echo "📉 RECENT LOSS VALUES:"
grep -i "loss" /ssd/tts_project/training_progress.log | tail -5

echo ""
echo "📁 TRAINING OUTPUT FILES:"
ls -la /ssd/tts_project/arm_max_quality_output/henry_voice_arm_max_quality*/

echo ""
echo "💾 CHECKPOINT FILES:"
find /ssd/tts_project/arm_max_quality_output -name "*.pth" | wc -l
echo "checkpoint files created"

echo ""
echo "🔄 TO CONTINUE MONITORING:"
echo "   tail -f /ssd/tts_project/training_progress.log"
echo "   python3 /ssd/tts_project/scripts/monitor_training.py"