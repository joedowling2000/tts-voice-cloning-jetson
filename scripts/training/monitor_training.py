#!/usr/bin/env python3
"""
Real-time TTS Training Monitor
Shows training progress, loss, and status
"""

import os
import time
import subprocess
import json
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_colored(message, color):
    print(f"{color}{message}{Colors.END}")

def print_header(title):
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * 60}")
    print(f"📊 {title}")
    print(f"{'=' * 60}{Colors.END}")

def check_training_process():
    """Check if training process is running"""
    try:
        result = subprocess.run(
            ["ps", "aux"], 
            capture_output=True, 
            text=True
        )
        
        training_lines = [line for line in result.stdout.split('\n') 
                         if 'train_tts' in line and 'python' in line]
        
        return len(training_lines) > 0, training_lines
    except:
        return False, []

def get_latest_log_output():
    """Get the latest training log output"""
    # Check for different possible log files
    log_files = [
        "/ssd/tts_project/training_proper.log",
        "/ssd/tts_project/training_current.log",
        "/ssd/tts_project/training_output_no_ssim.log",
        "/ssd/tts_project/training_output_fixed.log", 
        "/ssd/tts_project/training_output.log",
        "/ssd/tts_project/training_progress.log"
    ]
    
    latest_log = None
    latest_time = 0
    
    # Find the most recently modified log file
    for log_file in log_files:
        if os.path.exists(log_file):
            mtime = os.path.getmtime(log_file)
            if mtime > latest_time:
                latest_time = mtime
                latest_log = log_file
    
    if not latest_log:
        return "No log file found yet..."
    
    try:
        # Get last 20 lines for better context
        result = subprocess.run(
            ["tail", "-20", latest_log],
            capture_output=True,
            text=True
        )
        
        # Get file size and modification time
        size = os.path.getsize(latest_log)
        mtime = datetime.fromtimestamp(os.path.getmtime(latest_log))
        
        header = f"📁 Reading from: {os.path.basename(latest_log)}\n"
        header += f"📊 Size: {size:,} bytes | Last modified: {mtime.strftime('%H:%M:%S')}\n"
        header += "─" * 60 + "\n"
        
        return header + result.stdout
    except Exception as e:
        return f"Error reading log file: {e}"

def parse_training_metrics(log_content):
    """Parse training metrics from log output"""
    lines = log_content.split('\n')
    
    metrics = {
        'epoch': 'N/A',
        'step': 'N/A', 
        'total_steps': 'N/A',
        'loss': 'N/A',
        'lr': 'N/A',
        'step_time': 'N/A',
        'grad_norm': 'N/A',
        'last_update': 'N/A'
    }
    
    for line in lines:
        line = line.strip()
        
        # Look for EPOCH info
        if 'EPOCH:' in line:
            try:
                epoch_part = line.split('EPOCH:')[1].split()[0]
                metrics['epoch'] = epoch_part
            except:
                pass
        
        # Look for STEP info (format: --> STEP: 15/19 -- GLOBAL_STEP: 815)
        elif '-- GLOBAL_STEP:' in line:
            try:
                if 'STEP:' in line:
                    step_part = line.split('STEP:')[1].split('--')[0].strip()
                    if '/' in step_part:
                        current_step, total_steps = step_part.split('/')
                        metrics['step'] = current_step.strip()
                        metrics['total_steps'] = total_steps.strip()
                    
                if 'GLOBAL_STEP:' in line:
                    global_step = line.split('GLOBAL_STEP:')[1].strip()
                    metrics['global_step'] = global_step
            except:
                pass
        
        # Look for step metrics (format: | > loss: 5.17512  (5.17512))
        elif '| >' in line and ':' in line:
            try:
                parts = line.split('| >')[1].strip()
                if parts.startswith('loss:'):
                    loss_val = parts.split(':')[1].split()[0]
                    metrics['loss'] = loss_val
                elif parts.startswith('current_lr:'):
                    lr_val = parts.split(':')[1].strip()
                    metrics['lr'] = lr_val
                elif parts.startswith('step_time:'):
                    time_val = parts.split(':')[1].split()[0]
                    metrics['step_time'] = f"{time_val}s"
                elif parts.startswith('grad_norm:'):
                    grad_val = parts.split(':')[1].split()[0]
                    metrics['grad_norm'] = grad_val
            except:
                pass
        
        # Look for TRAINING timestamps
        elif 'TRAINING (' in line:
            try:
                timestamp_part = line.split('TRAINING (')[1].split(')')[0]
                metrics['last_update'] = timestamp_part.split()[1]  # Just the time part
            except:
                pass
    
    return metrics

def get_system_stats():
    """Get system resource usage"""
    try:
        # CPU usage
        cpu_result = subprocess.run(
            ["grep", "cpu ", "/proc/stat"],
            capture_output=True,
            text=True
        )
        
        # Memory usage
        mem_result = subprocess.run(
            ["free", "-h"],
            capture_output=True,
            text=True
        )
        
        # Disk usage for training directory
        disk_result = subprocess.run(
            ["df", "-h", "/ssd/tts_project"],
            capture_output=True,
            text=True
        )
        
        stats = "🖥️  SYSTEM RESOURCES:\n"
        
        # Memory info
        if mem_result.returncode == 0:
            mem_lines = mem_result.stdout.split('\n')
            if len(mem_lines) > 1:
                mem_parts = mem_lines[1].split()
                if len(mem_parts) >= 3:
                    total_mem = mem_parts[1]
                    used_mem = mem_parts[2]
                    stats += f"   💾 Memory: {used_mem} / {total_mem}\n"
        
        # Disk info
        if disk_result.returncode == 0:
            disk_lines = disk_result.stdout.split('\n')
            if len(disk_lines) > 1:
                disk_parts = disk_lines[1].split()
                if len(disk_parts) >= 5:
                    total_disk = disk_parts[1]
                    used_disk = disk_parts[2]
                    stats += f"   💿 Storage: {used_disk} / {total_disk}\n"
        
        return stats
        
    except Exception as e:
        return f"Error getting system stats: {e}"

def get_training_files_info():
    """Get info about training output files"""
    output_dir = "/ssd/tts_project/arm_max_quality_output"
    
    if not os.path.exists(output_dir):
        return "No training output directory found"
    
    try:
        # Find the latest training run directory
        run_dirs = [d for d in os.listdir(output_dir) 
                   if os.path.isdir(os.path.join(output_dir, d)) and 'custom_voice' in d]
        
        if not run_dirs:
            return "No training run directories found"
        
        latest_run = sorted(run_dirs)[-1]
        run_path = os.path.join(output_dir, latest_run)
        
        # Check for checkpoint files
        checkpoints = []
        config_files = []
        log_files = []
        
        if os.path.exists(run_path):
            for item in os.listdir(run_path):
                if item.endswith('.pth'):
                    checkpoints.append(item)
                elif item.endswith('.json'):
                    config_files.append(item)
                elif 'log' in item or 'events' in item:
                    log_files.append(item)
        
        info = f"📂 Training Run: {latest_run}\n"
        info += f"🎯 Checkpoints: {len(checkpoints)} files\n"
        info += f"⚙️  Config files: {len(config_files)} files\n"
        info += f"📋 Log files: {len(log_files)} files\n"
        
        if checkpoints:
            info += f"📄 Latest checkpoint: {sorted(checkpoints)[-1]}\n"
        else:
            info += f"⏳ No checkpoints yet (saves every 1000 steps)\n"
            
        # Get directory size
        try:
            result = subprocess.run(
                ["du", "-sh", run_path],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                size = result.stdout.split()[0]
                info += f"💾 Directory size: {size}\n"
        except:
            pass
        
        return info
        
    except Exception as e:
        return f"Error getting training info: {e}"

def monitor_training():
    """Main monitoring loop"""
    print_colored("🎤 TTS TRAINING MONITOR", Colors.MAGENTA)
    print_colored("Real-time monitoring of ARM maximum quality training", Colors.CYAN)
    print_colored("Press Ctrl+C to exit monitor (training will continue)", Colors.YELLOW)
    print_colored("=" * 70, Colors.CYAN)
    
    refresh_interval = 10  # seconds
    
    try:
        while True:
            # Clear screen for better readability
            os.system('clear')
            
            print_colored("🎤 TTS TRAINING MONITOR", Colors.MAGENTA)
            print_header("TTS TRAINING STATUS")
            print_colored(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", Colors.BLUE)
            print_colored(f"Refresh: Every {refresh_interval} seconds", Colors.BLUE)
            
            # Check if training is running
            is_running, process_lines = check_training_process()
            
            if is_running:
                print_colored("✅ Training Process: RUNNING", Colors.GREEN)
                print_colored(f"   Active processes: {len(process_lines)}", Colors.GREEN)
                # Show first process with CPU usage
                if process_lines:
                    first_process = process_lines[0]
                    parts = first_process.split()
                    if len(parts) >= 3:
                        cpu_usage = parts[2]
                        mem_usage = parts[3]
                        print_colored(f"   CPU: {cpu_usage}% | Memory: {mem_usage}%", Colors.GREEN)
            else:
                print_colored("❌ Training Process: NOT DETECTED", Colors.RED)
                print_colored("   Check if training has completed or crashed", Colors.YELLOW)
            
            print_header("LATEST TRAINING OUTPUT")
            
            # Get latest log output
            log_output = get_latest_log_output()
            
            # Parse metrics
            metrics = parse_training_metrics(log_output)
            
            print_colored(f"📊 CURRENT METRICS:", Colors.CYAN)
            print_colored(f"   🔢 Epoch: {metrics['epoch']}", Colors.YELLOW)
            print_colored(f"   📈 Step: {metrics['step']} / {metrics['total_steps']}", Colors.YELLOW)
            print_colored(f"   🌐 Global Step: {metrics.get('global_step', 'N/A')}", Colors.YELLOW)
            print_colored(f"   💥 Loss: {metrics['loss']}", Colors.YELLOW)
            print_colored(f"   🎛️  Learning Rate: {metrics['lr']}", Colors.YELLOW)
            print_colored(f"   ⏱️  Step Time: {metrics['step_time']}", Colors.YELLOW)
            print_colored(f"   📊 Grad Norm: {metrics['grad_norm']}", Colors.YELLOW)
            print_colored(f"   🕐 Last Update: {metrics['last_update']}", Colors.BLUE)
            
            print_header("RECENT LOG OUTPUT")
            
            # Show log output with color coding
            log_lines = log_output.split('\n')
            display_lines = log_lines[-12:]  # Show last 12 lines
            
            for line in display_lines:
                if line.strip():
                    if 'error' in line.lower() or 'exception' in line.lower() or 'traceback' in line.lower():
                        print_colored(f"   {line}", Colors.RED)
                    elif 'epoch' in line.lower() or '-- GLOBAL_STEP:' in line:
                        print_colored(f"   {line}", Colors.GREEN)
                    elif 'loss' in line.lower() or '| >' in line:
                        print_colored(f"   {line}", Colors.YELLOW)
                    elif 'warning' in line.lower():
                        print_colored(f"   {line}", Colors.YELLOW)
                    else:
                        print_colored(f"   {line}", Colors.BLUE)
            
            print_header("TRAINING FILES & SYSTEM")
            files_info = get_training_files_info()
            print_colored(files_info, Colors.CYAN)
            
            system_stats = get_system_stats()
            print_colored(system_stats, Colors.BLUE)
            
            print_colored(f"\n🔄 Next refresh in {refresh_interval} seconds... (Ctrl+C to exit)", Colors.MAGENTA)
            print_colored("=" * 70, Colors.CYAN)
            
            # Wait for next refresh
            time.sleep(refresh_interval)
            
    except KeyboardInterrupt:
        print_colored(f"\n👋 Monitor stopped. Training continues in background!", Colors.GREEN)
        print_colored(f"You can restart the monitor anytime with:", Colors.CYAN)
        print_colored(f"   cd /ssd/tts_project && python3 scripts/monitor_training.py", Colors.BLUE)

def main():
    monitor_training()

if __name__ == "__main__":
    main()