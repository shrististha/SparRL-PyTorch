# SparRL-PyTorch


## Pre-requisite packages:

### Install using Conda
* Miniconda:
  * Install Conda:
  ```bash
    mkdir -p ~/miniconda3
    curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o ~/miniconda3/miniconda.sh
    bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
    rm ~/miniconda3/miniconda.sh
  ```
  * Refresh bash to get Conda: `source ~/miniconda3/bin/activate`
* networkit https://networkit.github.io/dev-docs/notebooks/Sparsification.html, https://networkit.github.io/get_started.html#macos

  ```bash
    xcode-select --install
    arch -arm64 brew install libomp
    export LDFLAGS="-L/opt/homebrew/opt/libomp/lib"
    export CPPFLAGS="-I/opt/homebrew/opt/libomp/include"
  ```
* Install using Conda:
  * `conda env create -f environment.yml`
  * Activate conda environment: ` conda activate spaRL      `

### Install individually
* networkx, https://networkx.org, https://github.com/networkx/networkx
  * `pip install networkx`
* community https://github.com/taynaud/python-louvain
  * `pip install python-louvain`
* pytorch https://pytorch.org/get-started/locally/
  * `pip install torch torchvision`
* networkit https://networkit.github.io/dev-docs/notebooks/Sparsification.html
  * ```commandline 
    # Install xcode command line tools 
    xcode-select --install
    # Install NetworKit via brew 
    arch -arm64 brew install libomp
    export LDFLAGS="-L/opt/homebrew/opt/libomp/lib"
    export CPPFLAGS="-I/opt/homebrew/opt/libomp/include"
    ```
  * Install networkit `pip install networkit`
* sklearn https://scikit-learn.org/1.6/install.html
  * `conda install conda-forge::scikit-learn`
* matplotlib https://anaconda.org/conda-forge/matplotlib
  * `conda install conda-forge::matplotlib`
* tqdm https://tqdm.github.io
  * `pip install tqdm`
* pandas https://anaconda.org/anaconda/pandas
  * `conda install anaconda::pandas`

## sbatch commands
Ref:
https://curc.readthedocs.io/en/latest/running-jobs/running-apps-with-jobs.html, https://curc.readthedocs.io/en/latest/running-jobs/slurm-commands.html

* `sbatch $SCRIPT`
* `squeue -u $USERNAME`

### Example
To run training on the karate graph over spearman using sbatch, use: 
```commandline
sbatch scripts/run.sh
```

## To train a model on the karate graph over spearman:
```code
python3 code/main.py --edge_list graphs/karate.edgelist --episodes 500 --T_max 17 --save_dir karate_spearman_models/ --subgraph_len 32 --obj spearman --T_eval 32 --eval_batch_size 1 --decay_episodes 200
```

## Evalute over 8 episodes
```code
python3 code/main.py --edge_list graphs/karate.edgelist --episodes 8 --T_max 17 --save_dir karate_spearman_models/ --subgraph_len 32 --obj spearman --load --eval --eval_batch_size 1
```

## Show training graphs
```code
python3 code/util/plot_rewards.py --save_dir karate_spearman_models --reward_smooth_w 64
```


