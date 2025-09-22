# Version Control System for TTS Training Runs

## Overview
This document defines the version control process for Henry Voice TTS training runs to ensure clear organization, tracking, and reproducibility.

## Directory Structure
```
/ssd/tts_project/
├── training_runs/
│   ├── henry_v2_stable_YYYYMMDD_HHMMSS/
│   │   ├── config.json              # Training configuration
│   │   ├── training_v2.log          # Comprehensive training log
│   │   ├── checkpoints/             # Model checkpoints
│   │   ├── plots/                   # Training plots and visualizations
│   │   ├── logs/                    # Additional logs
│   │   └── README.md                # Run-specific documentation
│   └── archive/                     # Completed/failed runs
├── configs/                         # Configuration templates
├── scripts/                         # Training scripts
└── voice_data/                      # Source audio data
```

## Naming Convention

### Training Runs
Format: `henry_v{MAJOR}_{VARIANT}_{TIMESTAMP}`

Examples:
- `henry_v2_stable_20250922_164500` - Version 2, stable variant
- `henry_v2_experimental_20250922_170000` - Version 2, experimental features
- `henry_v3_production_20250923_090000` - Version 3, production ready

### Version Numbers
- **Major Version (v1, v2, v3)**: Significant architecture or approach changes
- **Variant**: 
  - `stable` - Proven configuration with known good results
  - `experimental` - Testing new features or hyperparameters
  - `production` - Final optimized version for deployment
  - `debug` - Debugging specific issues

## Configuration Management

### Config Files
- Store in `/ssd/tts_project/configs/`
- Name format: `henry_voice_v{MAJOR}_{VARIANT}.json`
- Each run gets its own copy in the run directory

### Required Fields
All configs must include:
```json
{
  "model": "tacotron2",
  "run_name": "henry_voice_v2_stable",
  "run_description": "Detailed description of this run's purpose and changes",
  "version": "2.0",
  "variant": "stable",
  "output_path": "/ssd/tts_project/training_runs/{RUN_NAME}/",
  ...
}
```

## Logging Standards

### Log Files
- **training_v2.log**: Main training log with timestamps and levels
- **tensorboard/**: TensorBoard event files
- **checkpoints/**: Model checkpoints with step numbers
- **plots/**: Training progress visualizations

### Log Levels
- `INFO`: Normal training progress, checkpoints, evaluations
- `WARNING`: Non-critical issues, deprecation warnings
- `ERROR`: Recoverable errors, failed evaluations
- `CRITICAL`: Fatal errors that stop training

## Run Management

### Starting a New Run
1. Use the training script: `python3 scripts/train_henry_v2_stable.py`
2. Script automatically creates timestamped directory
3. Copies config to run directory
4. Sets up logging and monitoring

### During Training
- Monitor logs: `tail -f training_runs/{RUN_NAME}/training_v2.log`
- Check TensorBoard: `tensorboard --logdir training_runs/{RUN_NAME}/`
- Checkpoint frequency: Every 500 steps

### After Training
1. **Success**: Move to `training_runs/` (keep as-is)
2. **Failure**: Move to `training_runs/archive/failed/`
3. **Incomplete**: Move to `training_runs/archive/incomplete/`

### Cleanup Commands
```bash
# Archive old runs
./scripts/archive_training_runs.sh

# Clean up failed runs
./scripts/cleanup_failed_runs.sh

# Full reset (BE CAREFUL!)
./scripts/reset_all_training.sh
```

## Quality Metrics

### Success Criteria
- Total loss < 2.0
- Alignment error < 0.1
- Stopnet loss < 0.5
- No NaN values in any loss
- Generated audio < 5 seconds for short text

### Evaluation Process
1. Automatic evaluation every 25 epochs
2. Generate test sentences
3. Manual quality check of outputs
4. Document results in run README

## Backup and Recovery

### Critical Files
- Source audio: `/ssd/tts_project/voice_data/`
- Best models: `training_runs/{RUN_NAME}/best_model.pth`
- Configs: `/ssd/tts_project/configs/`

### Backup Schedule
- Weekly: Copy best models to external storage
- Monthly: Full project backup
- Before major changes: Snapshot current state

## Troubleshooting

### Common Issues
1. **SSIM NaN errors**: Check `decoder_ssim_alpha: 0.0`
2. **KeyError avg_loss_1**: Use stable config template
3. **High alignment error**: Increase guided attention alpha
4. **Stopnet not learning**: Increase stopnet_pos_weight

### Emergency Procedures
1. **Training stuck**: Check GPU/CPU usage, restart if needed
2. **Disk full**: Run cleanup scripts, archive old runs
3. **Config errors**: Validate JSON, check required fields
4. **Environment issues**: Reload TTS environment

## Examples

### Start New Stable Training
```bash
cd /ssd/tts_project
source tts_arm_env/bin/activate
python3 scripts/train_henry_v2_stable.py
```

### Monitor Training
```bash
# Follow logs
tail -f training_runs/henry_v2_stable_*/training_v2.log

# Check TensorBoard
tensorboard --logdir training_runs/henry_v2_stable_*/
```

### Archive Completed Run
```bash
# Successful run - keep in place
echo "Run completed successfully" > training_runs/{RUN_NAME}/SUCCESS

# Failed run - archive
mv training_runs/{RUN_NAME} training_runs/archive/failed/
```

This version control system ensures every training run is properly tracked, logged, and organized for maximum clarity and reproducibility.