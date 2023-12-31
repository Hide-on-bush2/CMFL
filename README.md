# (Published in TPDS) A Decentralized Federated Learning Framework via Committee Mechanism With Convergence Guarantee

This repository contains the code and experiments for the paper:

> [CMFL](https://ieeexplore.ieee.org/abstract/document/9870745?casa_token=gEqc81UzNrsAAAAA:PtMEuUuYXi68Vz2A2NxECkyIqdpo9tdfktLn94bzbfauc15zpck4HJblFD0EpUK5UNOazobOFJ6U)
>
> [TPDS](https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=71)

and it is based on the implementation of [FedProx](https://github.com/litian96/FedProx) for the paper:

> [Fed](https://arxiv.org/abs/1812.06127)
>
> [MLSys 2020](https://mlsys.org/)

CMFL aims to provide a robust and efficient gradient aggregation strategies with committee mechanisms in a decentralized way. We evaluate CMFL in a testbed where decentralized behaviours are simulated in one machine.

## Preparation

### Dataset generation

We **already provide four synthetic datasets** that are used in the paper under corresponding folders. For all datasets, see the `README` files in separate `data/$dataset` folders for instructions on preprocessing and/or sampling data.

The statistics of real federated datasets are summarized as follows.

<center>

| Dataset     | Devices | Samples | Samples/device <br> mean (stdev) |
| ----------- | ------- | ------- | -------------------------------- |
| MNIST       | 1,000   | 69,035  | 69 (106)                         |
| FEMNIST     | 200     | 18,345  | 92 (159)                         |
| Shakespeare | 143     | 517,106 | 3,616 (6,808)                    |
| Sent140     | 772     | 40,783  | 53 (32)                          |

</center>

### Downloading dependencies

```
pip3 install -r requirements.txt
```

## Parameter

### GPU Options

(1) You don't need a GPU to run the synthetic data experiments:

```
export CUDA_VISIBLE_DEVICES=
```

(2) Specify a GPU id if needed:

```
export CUDA_VISIBLE_DEVICES=available_gpu_id
```

Otherwise just run to CPUs [might be slow if testing on Neural Network models]:

```
export CUDA_VISIBLE_DEVICES=
```

### Dataset & Model

We have provided multiple datasets for evaluation::

- sent140
- nist
- shakespeare
- mnist
- synthetic_iid
- synthetic_0_0
- synthetic_0.5_0.5
- synthetic_1_1

Basically, you can specify the corresponding model of that dataset (choose from `flearn/models/$DATASET/$MODEL.py` and use `$MODEL` as the model name), available models are as follows:

- sent140.bag_dnn
- sent140.stacked_lstm
- sent140.stacked_lstm_no_embeddings
- nist.mclr
- mnist.mclr
- mnist.cnn
- shakespeare.stacked_lstm
- synthetic.mclr': (10, )

### Committee-related Parameters

We implement the training algorithm of CMFL in `src/flearn/trainers/cmfl.py`, and you can specify the committee-related parameters:

- `selection_strategy`: you can choose which selection strategy you want to use by specifying 1 or 2.
- `committee_rate`: the percentage of commitee members
- `aggregation_rate`: the percentage of gradients used for aggregation per round

### Attacker-related Parameters

We implement some possible attack logics of the adversary, which can be specified by the following parameters:

- `attack_rate`: the percentage of the mallicious nodes
- `attack_method`: the attack strategies the mallicious nodes adpot
- `attack_range`: specify how powerful the attack is, its value depends on individual attack strategy

### Other Parameters

There are some other parameters related to the FL itself as follows:

- `learning_rate`
- `num_rounds`: number of the total rounds
- `batch_size`
- `active_rate`: the percentage of activated clients per round
- `num_epochs`: the number of training epochs per round
- `record_log`: the location of the log

## Start the Experiment

After determing all the parameters, you can simply start the experiment by runing `main.py` under `src`. For instance:

```
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
```

and you would get two logs generated by this trial. The first log `demo_selection_1.txt` locates at `log/log_file_log/`. This log records the name of the exact log containing the experimental results in `log/log_file/`. This design enables you to run multiple experiments in sequence and store the names of logs in `log/log_file_log`.

## Demo

Run `./demo.sh` for testing.

## Hints

As some files are larger than GitHub's recommended maximum file size of 50.00 MB, we put them into the .gitignore:

```
src/data/sent140/data/*
src/flearn/models/sent140/glove.6B/glove.6B.50d.txt
```

Before you run the demo, you may need to clone [FedProx](https://github.com/litian96/FedProx) and copy the corresponding files to this repository.
