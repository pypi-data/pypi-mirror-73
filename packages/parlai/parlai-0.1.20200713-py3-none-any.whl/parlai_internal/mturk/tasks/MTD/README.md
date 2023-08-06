## Deploy Dragon

### Environment

```
wget https://repo.continuum.io/archive/Anaconda3-4.4.0-Linux-x86_64.sh
bash Anaconda3-4.4.0-Linux-x86_64.sh
sudo apt-get install -y python-setuptools
pip install spacy
python -m spacy.en.download all
```

### Get code
```
git clone https://github.com/kimiyoung/ParlAI.git
git clone https://github.com/fairinternal/ParlAI-Internal.git ParlAI/parlai_internal
cd ParlAI
git checkout mturk_v7
python setup.py develop
cd parlai_internal
git checkout zy-dev
```

### Get data

Suppose you are in the `ParlAI` directory on a devfair machine.
```
mkdir data
cd data
scp -r /private/home/zhiliny/ParlAI/data/chat_log .
scp -r /private/home/zhiliny/ParlAI/data/graph_world2_v11* .
scp -r /private/home/zhiliny/ParlAI/data/graph_world2_v12* .
scp -r /private/home/zhiliny/ParlAI/data/graph_world2_v13* .
scp -r /private/home/zhiliny/ParlAI/data/graph_world2_vBASELIN* .
scp -r /private/home/zhiliny/ParlAI/data/graph_world2/ .
cd ../parlai_internal/mturk/tasks/MTD
mkdir tmp
cd tmp
scp /private/home/zhiliny/ParlAI/parlai_internal/mturk/tasks/MTD/tmp/0_final* .
```

### Run GPU placeholder

#### Generate SRUN scripts

Suppose you are in the `ParlAI` directory on a devfair machine.
```
cd parlai_internal/projects/graph_world2
python gen_sbatch_script.py
```

#### Launch jobs

First cancel all the current jobs.
```
scancel -u <username>
```

Then run the scripts in the directory `parlai_internal/projects/graph_world2`,
```
./batch_holder.sh
```

This will launch a placeholder for 80 GPUs. Use `squeue -u <username>` to make sure all jobs are running (not waiting) before proceeding to the next steps.

#### Relaunch

Note that the above jobs get expired after 72 hours, so we need to relaunch the jobs when it is close to expiration. Just repeat the steps above: first cancel all existing jobs and then run the `batch_holder.sh` script.

### Run MTD

#### Parameters

Suppose you are in the `parlai_internal/mturk/tasks/MTD` directory.

Before running MTD, we need to set the `VERSION_NUM` in `task_config.py`, and the arguments of `run.py`.

#### Commands

Live mode:
```
python run.py -r <reward> --live --nc 20 --start_round <start_round> --end_round <end_round>
```

Sandbox mode:
```
python run.py -nc 1
```

#### Resume training

Sometimes training in MTD could fail due to various reasons. In this case, we will get stuck at
```
Please manually do the training, and press enter later...
```

In this case, we will leave the current program as it is (do not Ctrl-C it!), start another screen, and go to the `parlai_internal/mturk/tasks/MTD` directory, and then resume training by
```
python run.py --resume --start_round <the_round_we_are_stuck_in>
```

When training is finished, we can go back to the main program, and press enter to proceed.

#### Manually sending bonus

Sometimes we need to manually send the bonus.

Go to the `parlai_internal/mturk/tasks/MTD` directory, and then do
```
python run.py --bonus --start_round <the_round_for_bonus>
```

#### Manually sending emails

Go to the `parlai_internal/mturk/tasks/MTD` directory, and do
```
python run.py --email --start_round <the_round_for_email>
```

#### Get experimental results

This part is not automated yet. We need to tweak `parlai_internal/mturk/tasks/MTD/run.py` and run `python run.py`.
