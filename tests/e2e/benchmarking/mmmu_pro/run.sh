#!/bin/bash
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -ex

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
cd "$SCRIPT_DIR"

export LOG_DIR=./results
export MODEL_NAME="$MODEL"
export TASK_NAME=mmmu_pro
MODEL_NAME_CLEAN=$(echo "$MODEL_NAME" | sed 's/\//-/g')
export OUTPUT_PREFIX="${TASK_NAME}_${MODEL_NAME_CLEAN}"
export ACCURACY_JSON_PATH=/workspace/mmmu_pro_accuracy.json

mkdir -p "$LOG_DIR"

CMD=(
    lm_eval
    --model vllm-vlm
    --model_args "pretrained=$MODEL_NAME,tensor_parallel_size=${TP_SIZE:-8},dtype=auto,max_model_len=4096,trust_remote_code=True,max_num_batched_tokens=16384"
    --tasks "$TASK_NAME"
    --include_path "$SCRIPT_DIR"
    --batch_size 1
    --output_path "$LOG_DIR/$OUTPUT_PREFIX.json"
    --apply_chat_template
)

"${CMD[@]}"

LATEST_FILE=$(find "$LOG_DIR" -type f -name "${OUTPUT_PREFIX}_*.json" -printf "%T@ %p\n" | sort -nr | head -n 1 | cut -d' ' -f2-)
python parse_lm_eval_mmmu_pro_results.py "$LATEST_FILE" > "$ACCURACY_JSON_PATH"