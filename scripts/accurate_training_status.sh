#!/bin/bash

# Accurate Training Status Check
echo "🎤 TTS TRAINING STATUS CHECK"
echo "============================"

# Get current time
current_time=$(date +%s)
current_readable=$(date)

echo "Current time: $current_readable"
echo

echo "📊 TRAINING PROCESSES:"
if ps aux | grep -q "train_tts.*python" && [ "$(ps aux | grep "train_tts.*python" | grep -v grep | wc -l)" -gt 0 ]; then
    echo "✅ Training is RUNNING"
    echo "   Active processes: $(ps aux | grep "train_tts.*python" | grep -v grep | wc -l)"
    
    # Get the most recent training process
    latest_pid=$(ps aux | grep "train_tts.*python" | grep -v grep | sort -k2 | tail -1 | awk '{print $2}')
    if [ -n "$latest_pid" ]; then
        # Get process start time using stat on /proc/pid
        if [ -d "/proc/$latest_pid" ]; then
            process_start_epoch=$(stat -c %Y /proc/$latest_pid)
            process_start_readable=$(ps -o lstart= -p $latest_pid)
            
            # Calculate actual running time
            running_seconds=$((current_time - process_start_epoch))
            running_hours=$((running_seconds / 3600))
            running_minutes=$(((running_seconds % 3600) / 60))
            
            echo "   Latest process PID: $latest_pid"
            echo "   Started: $process_start_readable"
            echo "   Running time: ${running_hours}h ${running_minutes}m"
        fi
    fi
else
    echo "❌ Training is NOT RUNNING"
fi

echo
echo "📁 LOG FILES:"
cd /ssd/tts_project
if ls *.log 1> /dev/null 2>&1; then
    for logfile in *.log; do
        size=$(du -h "$logfile" | cut -f1)
        modified=$(stat -c %y "$logfile")
        echo "   $logfile ($size) - $modified"
    done
else
    echo "   No log files found"
fi

echo
echo "📋 LATEST TRAINING OUTPUT:"
if [ -f "training_current.log" ]; then
    lines=$(wc -l < training_current.log)
    echo "   File: training_current.log ($lines lines)"
    echo "   Last 5 lines:"
    tail -5 training_current.log | sed 's/^/     /'
elif [ -f "training_proper.log" ]; then
    lines=$(wc -l < training_proper.log)
    echo "   File: training_proper.log ($lines lines)"
    echo "   Last 5 lines:"
    tail -5 training_proper.log | sed 's/^/     /'
else
    echo "   ❌ No current training log found"
fi

echo
echo "🎯 CHECKPOINT STATUS:"
if [ -d "arm_max_quality_output" ]; then
    latest_run=$(ls -1t arm_max_quality_output/ | grep henry_voice | head -1)
    if [ -n "$latest_run" ]; then
        echo "   Training run: $latest_run"
        checkpoint_count=$(ls arm_max_quality_output/$latest_run/*.pth 2>/dev/null | wc -l)
        echo "   Checkpoints: $checkpoint_count files"
        if [ $checkpoint_count -gt 0 ]; then
            latest_checkpoint=$(ls -t arm_max_quality_output/$latest_run/*.pth 2>/dev/null | head -1)
            checkpoint_time=$(stat -c %y "$latest_checkpoint")
            echo "   Latest: $(basename $latest_checkpoint)"
            echo "   Modified: $checkpoint_time"
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
echo "   CPU Load: $(uptime | awk -F'load average:' '{ print $2 }' | xargs)"
echo "   Disk (SSD): $(df -h /ssd | awk 'NR==2 {print $3 "/" $2 " (" $5 " used)"}')"

echo
echo "⏰ TRAINING TIMELINE:"
echo "   Current session started: ~06:48 AM (latest process)"
echo "   Actual running time: ~$(((current_time - $(stat -c %Y /proc/$(ps aux | grep "train_tts.*python" | grep -v grep | tail -1 | awk '{print $2}') 2>/dev/null)) / 60)) minutes"