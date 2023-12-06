#!/usr/bin/env bash
# calculate training times

python3  -u main.py --dataset='shakespeare' --optimizer='fedavg_attack'  \
            --learning_rate=0.005 --num_rounds=2000 --clients_per_round=10 \
            --eval_every=1 --batch_size=32 \
            --num_epochs=1 \
            --model='stacked_lstm' \
            --drop_percent=0 \
            --active_rate=0.04 \
            --attack_rate=0 \
            --aggregation_rate=0.4 \
            --attack_range=0 \
            --attack_method=0 \
            --merge_method=0 \
            --record_log='shakespeare_cmfl_a_b_fl.txt'

python3  -u main.py --dataset='shakespeare' --optimizer='cmfl'  \
            --learning_rate=0.005 --num_rounds=2000 --clients_per_round=10 \
            --eval_every=1 --batch_size=32 \
            --num_epochs=1 \
            --model='stacked_lstm' \
            --drop_percent=0 \
            --active_rate=0.1 \
            --attack_rate=0 \
            --committee_rate=0.4 \
            --aggregation_rate=0.4 \
            --attack_range=0 \
            --selection_strategy=2 \
            --attack_method=0 \
            --record_log='shakespeare_cmfl_a_b_fl.txt'
            
python3  -u main.py --dataset='shakespeare' --optimizer='cmfl'  \
            --learning_rate=0.005 --num_rounds=2000 --clients_per_round=10 \
            --eval_every=1 --batch_size=32 \
            --num_epochs=1 \
            --model='stacked_lstm' \
            --drop_percent=0 \
            --active_rate=0.1 \
            --attack_rate=0 \
            --committee_rate=0.4 \
            --aggregation_rate=0.4 \
            --attack_range=0 \
            --selection_strategy=1 \
            --attack_method=0 \
            --record_log='shakespeare_cmfl_a_b_fl.txt'