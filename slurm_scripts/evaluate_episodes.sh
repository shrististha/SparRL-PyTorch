#!/bin/bash                                                                                                       
#SBATCH --job-name=evaluate_episodes       # Job name                                                           
#SBATCH --output=output.txt               # Output log file (%j will be replaced by the job ID)                
#SBATCH --error=error.txt                 # Error log file                                                     
#SBATCH --ntasks=1                           # Number of tasks (typically 1 for a single Python script)           
#SBATCH --cpus-per-task=4                    # Number of CPU cores per task                                       
#SBATCH --gres=gpu:1                         # Request 1 GPU (adjust based on the available resources)            
#SBATCH --mem=16G                            # Memory allocation                                                  
#SBATCH --time=12:00:00                      # Maximum run time (HH:MM:SS)                                        
#SBATCH --partition=bigTiger                 # Partition to submit to (adjust based on availability)             

#conda env create -f environment.yml
conda activate spaRL
python --version
python code/main.py --edge_list graphs/karate.edgelist --episodes 8 --T_max 17 --save_dir karate_spearman_models/ --subgraph_len 32 --obj spearman --load --eval --eval_batch_size 1
