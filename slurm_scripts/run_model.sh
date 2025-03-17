#!/bin/bash
#SBATCH --job-name=run_training                # Job name
#SBATCH --output=output_%j.txt        # Output log file (%j = job ID, %x = job name, %A = job array ID, %a = task ID)
#SBATCH --error=error_%j.txt          # Error log file
#SBATCH --ntasks=1                             # Number of tasks (typically 1 for a single Python script)
#SBATCH --cpus-per-task=4                      # Number of CPU cores per task
#SBATCH --gres=gpu:1                           # Request 1 GPU (adjust based on available resources)
#SBATCH --mem=16G                              # Memory allocation
#SBATCH --time=12:00:00                        # Maximum run time (HH:MM:SS)
#SBATCH --partition=bigTiger                   # Partition to submit to (adjust based on availability)

# Generate timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Default values for parameters
EDGE_LIST="graphs/karate.edgelist"
EPISODES=500
T_MAX=17
SUBGRAPH_LEN=32
SAVE_DIR="karate_spearman_models/"
OBJ_NAME="spearman"
T_EVAL=32
EVAL_BATCH_SIZE=1
DECAY_EPISODES=200
ETA=0.2
# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --edge_list) EDGE_LIST="$2"; shift ;;
        --episodes) EPISODES="$2"; shift ;;
        --T_max) T_MAX="$2"; shift ;;
        --subgraph_len) SUBGRAPH_LEN="$2"; shift ;;
        --save_dir) SAVE_DIR="$2"; shift ;;
        --obj) OBJ_NAME="$2"; shift ;;
        --T_eval) T_EVAL="$2"; shift ;;
        --eval_batch_size) EVAL_BATCH_SIZE="$2"; shift ;;
        --decay_episodes) DECAY_EPISODES="$2"; shift ;;
	--eta) ETA="$2"; shift ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Run the Python script with the parsed arguments
python code/main.py \
    --edge_list "$EDGE_LIST" \
    --episodes "$EPISODES" \
    --T_max "$T_MAX" \
    --save_dir "$SAVE_DIR" \
    --subgraph_len "$SUBGRAPH_LEN" \
    --obj "$OBJ_NAME" \
    --T_eval "$T_EVAL" \
    --eval_batch_size "$EVAL_BATCH_SIZE" \
    --decay_episodes "$DECAY_EPISODES" \
    --eta "$ETA"