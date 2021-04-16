#!/bin/bash
echo 'Python path:'
which python
python ./anodeclstmgru/models/train_model.py \
  --learning_rate=0.001 \
  --batch_size=64 \
  --window_size=300 \
  --sample_size=10000 \
  --sample_faaaareq="10s"\
  --validation_split=0.05 \
  --hidden_size=128 \
  --embedding_size=456 \
  --max_epochs=1000 \
  --num_workers=2
