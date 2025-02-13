# WITH TMP ACCESS, REMOVE MOST OF THESE
export TMPDIR=/data1/joey/tmp
export TMP=/data1/joey/tmp
export TEMP=/data1/joey/tmp
export TEMPDIR=/data1/joey/tmp
export GCC_TMPDIR=/data1/joey/tmp
export NVCC_TMPDIR=/data1/joey/tmp
export TORCH_EXTENSIONS_DIR=/tmp/torch_extensions
export HOME=/data1/joey
export DS_BUILD_TEMP_DIR=/data1/joey/tmp
export CCACHE_TEMPDIR=/data1/joey/tmp
export HF_HOME=/data1/joey/hf_cache

source .env

set -x

uv run ray job submit --address="http://127.0.0.1:8265" \
  --working-dir . \
  --runtime-env-json='{
    "setup_commands": ["pip install openrlhf[vllm_latest]"],
    "env_vars": {
      "working_dir": "/data1/joey/rl_apps_simple",
      "TMPDIR": "/data1/joey/tmp",
      "TMP": "/data1/joey/tmp",
      "TEMP": "/data1/joey/tmp",
      "TEMPDIR": "/data1/joey/tmp",
      "GCC_TMPDIR": "/data1/joey/tmp",
      "NVCC_TMPDIR": "/data1/joey/tmp",
      "TORCH_EXTENSIONS_DIR": "/tmp/torch_extensions",
      "HOME": "/data1/joey",
      "DS_BUILD_TEMP_DIR": "/data1/joey/tmp",
      "CCACHE_TEMPDIR": "/data1/joey/tmp",
      "HF_HOME": "/data1/joey/hf_cache",
      "OPENAI_API_KEY": "'$OPENAI_API_KEY'"

    }
  }' \
  -- python -m openrlhf.cli.train_ppo_ray \
  --ref_num_nodes 1 \
  --ref_num_gpus_per_node 1 \
  --actor_num_nodes 1 \
  --actor_num_gpus_per_node 1 \
  --vllm_num_engines 1 \
  --vllm_tensor_parallel_size 1 \
  --pretrain Qwen/Qwen2.5-7B-Instruct \
  --save_path checkpoint/apps_attack \
  --micro_train_batch_size 2 \
  --train_batch_size 32 \
  --micro_rollout_batch_size 4 \
  --rollout_batch_size 8 \
  --n_samples_per_prompt 4 \
  --max_samples 64 \
  --max_epochs 2 \
  --generate_max_len 20000 \
  --prompt_max_len 6400 \
  --zero_stage 3 \
  --bf16 \
  --actor_learning_rate 2e-7 \
  --critic_learning_rate 5e-6 \
  --init_kl_coef 0.01 \
  --prompt_data codeparrot/apps \
  --input_key difficulty \
  --packing_samples \
  --flash_attn \
  --gradient_checkpointing \
  --use_wandb $WANDB_API_KEY \
  --wandb_project apps_attack \
  --advantage_estimator grpo \
  --remote_rm_url http://localhost:5000/get_reward \
  --env_file APPS_rl_env \
  --env_class AppsBackdoors \
  --adam_offload \
  --eval_steps 1 \
  #--overlap_comm \
  #--colocate_actor_ref \


      # "PATH": "/data1/joey/.local/bin:$PATH",
      # "PYTHONPATH": "/data1/joey/your_project_path:$PYTHONPATH",
      # "USER": "joey",
      # "UVENV_DIR": "/data1/joey/.uv",
      # "UV_CACHE_DIR": "/data1/joey/uv_cache",
      # "UV_SYSTEM_PYTHON": "/data1/joey/.pyenv/versions/3.10.0/bin/python",
      # "VIRTUAL_ENV": "/data1/joey/rl_apps_simple/.venv"