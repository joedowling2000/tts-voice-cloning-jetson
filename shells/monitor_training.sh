#!/bin/bash
# Training Monitor Script

echo "🔍 TTS Training Monitor"
echo "======================="
echo ""

while true; do
    clear
    echo "🎤 Custom Voice Training Monitor - $(date)"
    echo "============================================"
    echo ""
    
    if [ -d "/ssd/tts_project/full_training_output" ]; then
        echo "📁 Training Output Directory:"
        ls -la /ssd/tts_project/full_training_output/ | tail -10
        echo ""
        
        echo "📊 Latest Checkpoints:"
        find /ssd/tts_project/full_training_output -name "checkpoint_*.pth" -type f -exec ls -la {} \; | tail -5
        echo ""
        
        echo "📈 Training Logs (last 10 lines):"
        if [ -f "/ssd/tts_project/full_training_output/train.log" ]; then
            tail -10 /ssd/tts_project/full_training_output/train.log
        else
            echo "No training log found yet..."
        fi
        echo ""
        
        echo "💾 Disk Usage:"
        du -sh /ssd/tts_project/full_training_output/
        echo ""
    else
        echo "⏳ Waiting for training to start..."
    fi
    
    echo "🔄 Updating in 30 seconds... (Ctrl+C to stop)"
    sleep 30
done
