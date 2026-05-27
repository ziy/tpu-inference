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

import ast
import re


def doc_to_visual_mmmu(doc):
    """
    Extracts the image using the capitalized 'Image' key.
    """
    image = doc.get("Image") or doc.get("image")
    if image is None:
        return []
    return [image]


def doc_to_text_mmmu(doc):
    """
    Formats the prompt with Qwen-specific vision placeholders.
    """
    question = doc.get("Question") or doc.get("question")
    options = doc.get("Options") or doc.get("options")

    if isinstance(options, str):
        try:
            options = ast.literal_eval(options)
        except Exception:
            pass

    labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    choices_str = "\n".join(
        [f"({labels[i]}) {opt}" for i, opt in enumerate(options)])

    # REQUIRED for Qwen2.5-VL: The vision placeholder tags
    # These tell vLLM where to insert the image tokens in the sequence.
    vision_placeholder = "<|vision_start|><|image_pad|><|vision_end|>"

    prompt = f"{vision_placeholder}{question}\n{choices_str}\nAnswer with the option letter from the given choices directly.\nAnswer:"
    return prompt


def process_docs_mmmu(dataset):
    return dataset


def process_results_mmmu(doc, results):
    """
    Parses the model output and compares it to the capitalized 'Answer' key.
    """
    prediction = results[0].strip()
    # Handle both capitalized and lowercase keys
    gold = (doc.get("Answer") or doc.get("answer")).strip()

    # Look for the first single letter (A-J) in the response
    match = re.search(r'\b([A-J])\b', prediction)
    parsed_pred = match.group(1) if match else prediction

    return {"mmmu_pro_acc": 1 if parsed_pred == gold else 0}
