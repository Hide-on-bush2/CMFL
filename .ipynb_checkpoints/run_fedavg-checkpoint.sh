#!/usr/bin/env bash
python3  -u main.py --dataset='sent140' --optimizer='fedavg'  \
            --learning_rate=0.01 --num_rounds=1000 --clients_per_round=10 \
            --eval_every=1 --batch_size=32 \
            --num_epochs=1 \
            --model='stacked_lstm' \
            --drop_percent=0 \

