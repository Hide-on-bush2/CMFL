#!/usr/bin/env bash
#CMFL1
python3  -u main.py --dataset='sent140' --optimizer='cmfl'  \
            --learning_rate=0.005 --num_rounds=2000 --clients_per_round=10 \
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
            --attack_method=2 \
            --record_log='learningRate_0.005_attack2_2000round.txt'
            
#CMFL2            
python3  -u main.py --dataset='sent140' --optimizer='cmfl'  \
            --learning_rate=0.005 --num_rounds=2000 --clients_per_round=10 \
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
            --attack_method=2 \
            --record_log='learningRate_0.005_attack2_2000round.txt'
            
#normal-attack
python3  -u main.py --dataset='sent140' --optimizer='fedavg_attack'  \
            --learning_rate=0.005 --num_rounds=2000 --clients_per_round=10 \
            --eval_every=1 --batch_size=32 \
            --num_epochs=1 \
            --model='stacked_lstm' \
            --drop_percent=0 \
            --active_rate=0.1 \
            --attack_rate=0.1 \
            --aggregation_rate=0.4 \
            --attack_range=0 \
            --attack_method=2 \
            --merge_method=0 \
            --record_log='learningRate_0.005_attack2_2000round.txt'
            
#median-attack
python3  -u main.py --dataset='sent140' --optimizer='fedavg_attack'  \
            --learning_rate=0.005 --num_rounds=2000 --clients_per_round=10 \
            --eval_every=1 --batch_size=32 \
            --num_epochs=1 \
            --model='stacked_lstm' \
            --drop_percent=0 \
            --active_rate=0.1 \
            --attack_rate=0.1 \
            --aggregation_rate=0.4 \
            --attack_range=0 \
            --attack_method=2 \
            --merge_method=1 \
            --record_log='learningRate_0.005_attack2_2000round.txt'
            
#trimmed-attack
python3  -u main.py --dataset='sent140' --optimizer='fedavg_attack'  \
            --learning_rate=0.005 --num_rounds=2000 --clients_per_round=10 \
            --eval_every=1 --batch_size=32 \
            --num_epochs=1 \
            --model='stacked_lstm' \
            --drop_percent=0 \
            --active_rate=0.1 \
            --attack_rate=0.1 \
            --aggregation_rate=0.4 \
            --attack_range=0 \
            --attack_method=2 \
            --merge_method=2 \
            --record_log='learningRate_0.005_attack2_2000round.txt'
            
#krum-attack
python3  -u main.py --dataset='sent140' --optimizer='fedavg_attack'  \
            --learning_rate=0.005 --num_rounds=2000 --clients_per_round=10 \
            --eval_every=1 --batch_size=32 \
            --num_epochs=1 \
            --model='stacked_lstm' \
            --drop_percent=0 \
            --active_rate=0.1 \
            --attack_rate=0.1 \
            --aggregation_rate=0.4 \
            --attack_range=0 \
            --attack_method=2 \
            --merge_method=3 \
            --record_log='learningRate_0.005_attack2_2000round.txt'

#multi-krum-attack
python3  -u main.py --dataset='sent140' --optimizer='fedavg_attack'  \
            --learning_rate=0.005 --num_rounds=2000 --clients_per_round=10 \
            --eval_every=1 --batch_size=32 \
            --num_epochs=1 \
            --model='stacked_lstm' \
            --drop_percent=0 \
            --active_rate=0.1 \
            --attack_rate=0.1 \
            --aggregation_rate=0.4 \
            --attack_range=0 \
            --attack_method=2 \
            --merge_method=4 \
            --record_log='learningRate_0.005_attack2_2000round.txt'
            
            