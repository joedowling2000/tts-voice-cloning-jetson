#!/bin/bash

# Quick Training Status Check
echo "🎤 TTS TRAINING STATUS CHECK"
echo "============================"

echo
echo "📊 TRAINING PROCESS:"
if ps aux | grep -q "train_tts.*python" && [ "$(ps aux | grep "train_tts.*python" | grep -v grep | wc -l)" -gt 0 ]; then
    echo "✅ Training is RUNNING"
    echo "   Processes: $(ps aux | grep "train_tts.*python" | grep -v grep | wc -l)"
else
    echo "❌ Training is NOT RUNNING"
fi

echo
echo "📁 LOG FILES:"
cd /ssd/tts_project
ls -la *.log 2>/dev/null | while read line; do
    echo "   $line"
done

echo
echo "📋 LATEST LOG OUTPUT (training_current.log):"
if [ -f "training_current.log" ]; then
    echo "   Lines: $(wc -l < training_current.log)"
    echo "   Last modified: $(stat -c %y training_current.log)"
    echo "   Recent output:"
    tail -5 training_current.log | sed 's/^/     /'
else
    echo "   ❌ training_current.log not found"
fi

echo
echo "🎯 CHECKPOINT STATUS:"
if [ -d "arm_max_quality_output" ]; then
    latest_run=$(ls -1t arm_max_quality_output/ | grep voice_model | head -1)
    if [ -n "$latest_run" ]; then
        echo "   Training run: $latest_run"
        checkpoint_count=$(ls arm_max_quality_output/$latest_run/*.pth 2>/dev/null | wc -l)
        echo "   Checkpoints: $checkpoint_count files"
        if [ $checkpoint_count -gt 0 ]; then
            latest_checkpoint=$(ls -t arm_max_quality_output/$latest_run/*.pth 2>/dev/null | head -1)
            echo "   Latest: $(basename $latest_checkpoint)"
        fi
    else
        echo "   ❌ No training runs found"
    fi
else
    echo "   ❌ No output directory found"
fi

echo
echo "💾 SYSTEM RESOURCES:"
echo "   Memory: $(free -h | awk '/^Mem:/ {print $3 "/" $2}')"
echo "   Disk (SSD): $(df -h /ssd | awk 'NR==2 {print $3 "/" $2 " (" $5 " used)"}')"