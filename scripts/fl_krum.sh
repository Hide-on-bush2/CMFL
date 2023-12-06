#krum-attack
python3  -u main.py --dataset='sent140' --optimizer='fedavg_attack'  \
            --learning_rate=0.005 --num_rounds=1000 --clients_per_round=10 \
            --eval_every=1 --batch_size=32 \
            --num_epochs=1 \
            --model='stacked_lstm' \
            --drop_percent=0 \
            --active_rate=0.1 \
            --attack_rate=0.1 \
            --aggregation_rate=0.4 \
            --attack_range=0.5 \
            --attack_method=1 \
            --merge_method=3 \
            --record_log='debug.txt'
            
python3  -u main.py --dataset='sent140' --optimizer='fedavg_attack'  \
            --learning_rate=0.005 --num_rounds=1000 --clients_per_round=10 \
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
            --record_log='debug.txt'
            
            
python3  -u main.py --dataset='sent140' --optimizer='fedavg_attack'  \
            --learning_rate=0.005 --num_rounds=1000 --clients_per_round=10 \
            --eval_every=1 --batch_size=32 \
            --num_epochs=1 \
            --model='stacked_lstm' \
            --drop_percent=0 \
            --active_rate=0.1 \
            --attack_rate=0.1 \
            --aggregation_rate=0.4 \
            --attack_range=0 \
            --attack_method=6 \
            --merge_method=3 \
            --record_log='debug.txt'