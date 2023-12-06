#!/usr/bin/env bash
#CMFL with selection strategy 1
cd src
python3  -u main.py --dataset='sent140' --optimizer='cmfl'  \
            --learning_rate=0.005 --num_rounds=100 --clients_per_round=10 \
            --eval_every=1 --batch_size=32 \
            --num_epochs=1 \
            --model='stacked_lstm' \
            --drop_percent=0 \
            --active_rate=0.1 \
            --attack_rate=0.1 \
            --committee_rate=0.4 \
            --aggregation_rate=0.4 \
            --attack_range=0 \
            --selection_strategy=1 \
            --attack_method=1 \
            --record_log='demo_selection_1.txt'
            
#CMFL2 with selection strategy 2           
python3  -u main.py --dataset='sent140' --optimizer='cmfl'  \
            --learning_rate=0.005 --num_rounds=100 --clients_per_round=10 \
            --eval_every=1 --batch_size=32 \
            --num_epochs=1 \
            --model='stacked_lstm' \
            --drop_percent=0 \
            --active_rate=0.1 \
            --attack_rate=0.1 \
            --committee_rate=0.4 \
            --aggregation_rate=0.4 \
            --attack_range=0 \
            --selection_strategy=2 \
            --attack_method=1 \
            --record_log='demo_selection_2.txt'