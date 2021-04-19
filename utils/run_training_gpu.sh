#!/bin/bash
echo 'Python path:'
which python
python ./anodeclstmgru/models/train_model.py \
  --learning_rate=0.001 \
  --batch_size=64 \
  --window_size=500 \
  --sample_size=10000 \
  --sample_freq="10s"\
  --validation_split=0.05 \
  --test_set_step_size=100 \
  --hidden_size=512 \
  --embedding_size=1024 \
  --num_lstm_layer=1 \
  --max_epochs=10000 \
  --num_workers=12 \
  --gpu=1
