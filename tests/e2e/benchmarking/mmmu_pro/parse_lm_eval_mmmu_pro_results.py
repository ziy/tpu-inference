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

import json
import os
import sys


def parse_results(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found", file=sys.stderr)
        sys.exit(1)

    with open(file_path, 'r') as f:
        data = json.load(f)

    # Extract the task results
    task_results = data['results'].get('mmmu_pro', {})

    # We want the 'mmmu_pro_acc' metric (ignoring stderr)
    acc = task_results.get('mmmu_pro_acc,none', 0.0)

    # Print the specific JSON structure the infra expects
    print(json.dumps({"mmmu_pro_acc": acc}))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_results.py <path_to_json>")
        sys.exit(1)
    parse_results(sys.argv[1])
